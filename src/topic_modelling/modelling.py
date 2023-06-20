import os
import pandas as pd
from gensim.models import LdaModel, CoherenceModel
from gensim.corpora import Dictionary, MmCorpus
from random import sample
from ..metric_functions import timer

def train_lda(corpus, K, alpha, beta, dictionary, model_id):
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics= K,
        alpha= alpha,
        eta= beta,
        iterations=50,
        passes=2,
        random_state=42,
    )
    # Create a directory for corpus parts if it doesn't exist
    model_dir = 'lda_models'
    os.makedirs(model_dir, exist_ok=True)
    # Save the model to disk
    lda_model.save(f"{model_dir}/lda_model_{model_id}.gensim")
    return lda_model

# Objective function
@timer
def objective(params, directory):
    K, alpha, beta = params
    dictionary = Dictionary.load('dictionary.gensim')
    # Get a list of all corpus part files
    corpus = MmCorpus('corpus_parts/corpus.mm')

    # Count the number of calls to the objective function
    objective.calls += 1
    # update model_id on every run
    model_id = objective.calls

    # train model
    lda_model = train_lda(corpus, K, alpha, beta, dictionary, model_id)
    #model_dir = 'lda_models/lda_model_1.gensim'
    #lda_model = LdaModel.load(model_dir)

    # Load the texts
    raw_texts = list(load_all_chunks(directory))

    # Filter out tokens not in the dictionary to align the text with the dictionary
    texts = [[word for word in doc if word in dictionary.token2id] for doc in raw_texts]

    # Take a sample from the texts
    sample_texts = sample(texts, min(10000, len(texts))) # Consider changing the sample size according to your needs.

    # find model perplexity
    perplexity = lda_model.log_perplexity(corpus)

    # Find the coherence of the model
    coherence_model_lda = CoherenceModel(model=lda_model, texts=sample_texts, window_size=110, dictionary=dictionary, coherence='c_v', processes=-1)  # Increase processes according to your system configuration
    coherence = coherence_model_lda.get_coherence()

    # Append to results DataFrame
    global results_df
    results_df = pd.concat([results_df, pd.DataFrame([{"model_id":model_id, "K":K, "alpha": alpha, "beta": beta, "passes": 2, "iterations":50, "coherence": coherence, "perplexity": perplexity}])], ignore_index=True)

    # After the optimization process, you can save the results_df to a csv file for future use
    results_df.to_csv('lda_optimization_results.csv', index=False)
    # We are maximizing coherence, so this should be negated
    return -coherence_model_lda.get_coherence()

# Initialize the counter
objective.calls = 0
