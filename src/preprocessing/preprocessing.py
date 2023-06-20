#import libraries
from ..metric_functions import timer
from ..data_extraction import open_tar_file

#nltk
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import traceback

#pandas
import pandas as pd

# string
import re
import string
import ast
import time
from functools import reduce
import os

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', 100)

import nltk

#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')


# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

#def tokenize_text(texts):
 #   docs = nlp.pipe(texts, n_process=-1) # use all cores
 #   return [[token.text for token in doc if len(token.text) > 1] for doc in docs]

def tokenize_text(data): # tokenize
  tokens = nltk.word_tokenize(data)
  tokens = [token for token in tokens if len(token) > 1] #remove short/single character tokens to reduce vocabulary size
  return tokens

def lower_case(tokens_list):
  return [token.lower() for token in tokens_list]

def remove_formulas_citations(text_string):
    """ This accounts for intext fromulas and citations"""
    # Split the input string into words
    words = text_string.split()
    # Keep only words that don't contain a mix of letters and digits
    result = [word for word in words if not (re.search('[a-zA-Z]', word) and re.search('[0-9]', word))]
    # Join the words back into a string and return
    return ' '.join(result)

def remove_brackets(tokens_list):
    return [re.sub(r'\[.*?\]', '', re.sub(r'\(.*?\)', '', token)) for token in tokens_list]

def replace_whitespace(tokens_list):
  return [re.sub(r"\s+", " ", token) for token in tokens_list]

def remove_digits(tokens_list):
  return [re.sub(r'\w*\d\w*', '', token) for token in tokens_list]

def remove_ellipsis(tokens_list):
  return [re.sub(r"\w+…|…",  '', token) for token in tokens_list]

def remove_punctuation(tokens_list):
  return [re.sub(f"[{re.escape(string.punctuation)}]",  '', token) for token in tokens_list]

def remove_urls(tokens_list):
  return [re.sub(r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1', '', token) for token in tokens_list]

def remove_non_alphabetic(tokens_list):
  return [re.sub(r"[^a-zA-Z\s]",  '', token) for token in tokens_list]

def remove_stopwords(tokens_list):
  stopwords_set = set(stopwords.words("english"))
  text = [token for token in tokens_list if (token.lower() not in stopwords_set and len(token) > 1) ]
  return text

def lemmatize_text(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):

    # Use nlp.pipe method for more efficient text processing
    docs = nlp.pipe(texts)

    # Initialize an empty list to store the lemmatized sentences
    texts_out = []

    # Iterate over processed docs
    for doc in docs:
      lemmas = [token.lemma_ for token in doc if token.pos_ in allowed_postags]
      texts_out.append(lemmas)

    return texts_out

# Dictionary of functions that can be applied to the text with no particular order
func_dict = {
        'lower_case': lower_case,
        'remove_formulas_citations' :remove_formulas_citations,
        'remove_brackets' : remove_brackets,
        'replace_whitespace': replace_whitespace,
        'remove_digits': remove_digits,
        'remove_ellipsis': remove_ellipsis,
        'remove_punctuation': remove_punctuation,
        'remove_urls': remove_urls,
        'remove_non_alphabetic' : remove_non_alphabetic,
        'remove_stopwords': remove_stopwords,
        'lemmatize_text': lemmatize_text,
        'tokenize_text': tokenize_text
    }

def create_mapper(func_set):
    """Creates a mapper function that applies a set of preprocessing functions to a text."""
    def mapper(text):
        # Apply each preprocessing function in func_set to the text
        return reduce(lambda txt, func: func_dict[func](txt), func_set, text)
    return mapper

def data_optimize(df):
    """Reduce the size of the input dataframe
    Parameters
    ----------
    df: pd.DataFrame
    Returns
    -------
    df: pd.DataFrame
    data type optimized output dataframe
    """
    # Cast object columns to 'category' type if unique values < 0.5 * total rows
    df.loc[:, df.dtypes == 'object'] = \
        df.select_dtypes(['object']).apply(lambda x: x.astype('category') if len(x.value_counts()) < 0.5 * len(x) else x)
    return df

def flatten(lst):
    """Flatten a list of lists into a single list"""
    flat_list = []
    for sublist in lst:
        for subsublist in sublist:
            if isinstance(subsublist, list):
                for item in subsublist:
                    flat_list.append(item)
            else:
                flat_list.append(subsublist)
    return flat_list


# Dictionary of functions that can be applied to the text with no particular order
func_dict = {
        'lower_case': lower_case,
        'remove_formulas_citations' :remove_formulas_citations,
        'remove_brackets' : remove_brackets,
        'replace_whitespace': replace_whitespace,
        'remove_digits': remove_digits,
        'remove_ellipsis': remove_ellipsis,
        'remove_punctuation': remove_punctuation,
        'remove_urls': remove_urls,
        'remove_non_alphabetic' : remove_non_alphabetic,
        'remove_stopwords': remove_stopwords,
        'lemmatize_text': lemmatize_text,
        'tokenize_text': tokenize_text
    }


def create_mapper(func_set):
    """Creates a mapper function that applies a set of preprocessing functions to the input text."""
    def mapper(text):
        # Apply each preprocessing function in func_set to the text
        return reduce(lambda txt, func: func_dict[func](txt), func_set, text)
    return mapper

def process_body_text(text, mapper_func):
    # Check if body_text is a list of dictionaries (expected for document data) or just a string (expected for user input)
    if isinstance(text, list) and isinstance(text[0], dict):
        # Apply mapper_func to each section of body_text
        token_lists = mapper_func([para["text"] for para in text])
    elif isinstance(text, str):
        token_lists = mapper_func(text)
    else:
        raise ValueError(f'text should be a list of dictionaries or a string, but got {type(text)}')
    # Flatten the result
    flattened_tokens = flatten(token_lists)

    return ' '.join(flattened_tokens)

@timer
def check_data(df):
    null_tokens = df['tokens'].isna()
    null_data = df[null_tokens]
    for paper_id in null_data.index:
        print(f"Paper ID {paper_id} has null tokens.")
    return null_data

@timer
def token_selector(input_tar, null_csv, output_csv, chunk_size, func_set, max_files):
  mapper_func = create_mapper(func_set)
  # Null count variables
  null_count_before = 0
  null_count_after = 0

  # Iterate over the chunks yielded by open_tar_file
  for df_chunk in open_tar_file(input_tar, max_files= max_files, chunk_size=chunk_size):

    # Generate new DataFrame containing only the 'body_text' column, process it and rename it to 'tokens'
    token_df = df_chunk['body_text'].apply(process_body_text, mapper_func=mapper_func).to_frame('tokens')

    # Count null values after preprocessing
    null_df = check_data(token_df)

    token_df = data_optimize(token_df)
    # Write the new DataFrame to the file, preserving the original index
    token_df.to_csv(output_csv, mode="a", header=not os.path.isfile(output_csv), index=True)
    null_df.to_csv(null_csv, mode="a", header=not os.path.isfile(null_csv), index=True)

## Concurrent Multithreaded Queue Implementation


#@timer
#def token_selector(queue_dict, output_csv, chunk_size, func_set, data_ready, nan_output_csv):
#  while not data_ready.is_set():
#    time.sleep(1)  # Wait for data to be ready
#  try:
#    mapper_func = create_mapper(func_set)
#    while True:
#      items = list(queue_dict.items())  # Obtain a shallow copy of the dictionary without the lock
#      print(f"Length of queue_dict in Preprocessing: {len(queue_dict)}")
#      all_done = all(value[1]['token_selector_counter'] == 0 for key, value in items)
#      if all_done:
#        print("Done Processing JSON files...")
#        break  # All tasks done, break the while loop
#      for key, value in items:
#        df_chunk, counters = value
#        print(f"Key: {key}, Preprocessing Counter: {counters['token_selector_counter']}")  # Print the key and its counter
#        if counters['token_selector_counter'] > 0:
#          print("Processing JSON files...")
#          token_df = df_chunk['body_text'].apply(process_body_text, mapper_func=mapper_func).to_frame('tokens')
#          token_df = data_optimize(token_df)
#
#          # Save rows with NaN tokens to a separate csv file
#          nan_df = token_df[token_df['tokens'].isnull()]
#          nan_df.to_csv(nan_output_csv, mode="a", header=not os.path.isfile(nan_output_csv), index=True)
#
#          token_df.to_csv(output_csv, mode="a", header=not os.path.isfile(output_csv), index=True)
#
#          with queue_dict.lock:  # Quickly update the shared dictionary while the lock is held
#            if key in queue_dict:
#              current_value = queue_dict[key]
#              current_value[1]['token_selector_counter'] -= 1
#              queue_dict[key] = current_value
#              print(f"Decrementing counter for key {key} in token_selector. New counter: {queue_dict[key][1]['token_selector_counter']}")
#        else:
#          continue
#  except Exception as e:
#    print("An exception occurred in token_selector:")
#    print(f"Exception type: {type(e)}")
#    print(f"Exception message: {str(e)}")
#    print("Exception traceback:", traceback.format_exc())
