import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from gensim.corpora import Dictionary, MmCorpus
from joblib import dump, load
from ..metric_functions import timer


def load_chunk(chunk_id, directory):
    """
    Load a chunk from disk.
    """
    return load(f'{directory}/train/chunk_{chunk_id}.joblib')

def load_all_chunks(directory):
    """
    Load all chunks from disk, one at a time, and yield documents one by one.
    """
    chunk_id = 0
    while True:
        try:
            for doc in load_chunk(chunk_id, directory):
                yield doc
            chunk_id += 1
        except FileNotFoundError:
            break

def save_chunk(chunk_df, chunk_id, directory):
    """
    Transform a chunk and save it to disk separately as training and validation data.
    """
    # Drop rows containing NaN values
    chunk_df = chunk_df.dropna()

    chunk_df.loc[:, 'tokens'] = chunk_df['tokens'].str.split()
    tokens = chunk_df['tokens'].tolist() # this will be a list of lists of tokens

    # Add the paper IDs to the tracking dataframe
    tracking_df = pd.DataFrame({
        'original_paper_id': chunk_df['Unnamed: 0'].tolist(),
        'corpus_id': [np.nan]*len(chunk_df)
    })

    train, val = train_test_split(tokens, test_size=0.2)

    train_dir = os.path.join(directory, 'train')
    val_dir = os.path.join(directory, 'val')

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    dump(train, f'{train_dir}/chunk_{chunk_id}.joblib')
    dump(val, f'{val_dir}/chunk_{chunk_id}.joblib')

    # Return the tracking dataframe
    return tracking_df

@timer
def load_lda(input_csv, chunk_size, directory):
    """
    Load, transform and save chunks from a large CSV file.
    """
    # Convert chunks of the input_csv into lists of strings and save them
    tracking_dfs = []
    for chunk_id, chunk_df in enumerate(pd.read_csv(input_csv, chunksize=chunk_size)):
        tracking_df = save_chunk(chunk_df, chunk_id, directory)
        tracking_dfs.append(tracking_df)

    # Concatenate all tracking dataframes
    tracking_df = pd.concat(tracking_dfs)


    # Load the chunks of training data one by one, to create the dictionary and corpus

    processed_train_data = list(load_all_chunks(directory))
    dictionary = Dictionary(processed_train_data)
    print(f"Size of Dictionary before compression: {len(dictionary)}")

    dictionary.filter_extremes(no_below=10000, no_above=0.50)
    dictionary.compactify()
    print(f"Size of Dictionary after compression: {len(dictionary)}")
    print('Number of unique tokens in Dictionary: %d' % len(dictionary))

    # Save dictionary
    dictionary.save('dictionary.gensim')

    corpus_dir = 'corpus_parts'
    os.makedirs(corpus_dir, exist_ok=True)
    corpus_file = f'{corpus_dir}/corpus.mm'

    # Create the corpus
    corpus = [dictionary.doc2bow(text) for text in processed_train_data]

    # Assign corpus IDs to documents
    for i, doc in enumerate(corpus):
      tracking_df.loc[i, 'corpus_id'] = i

    tracking_df.head()
    # save tracking df to disk
    tracking_df.to_csv('tracking_df.csv', index=False)

    MmCorpus.serialize(corpus_file, corpus)
    print('Number of documents in Corpus: %d' % len(processed_train_data))
