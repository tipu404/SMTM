# Systematic Mapping Topic Modelling
SMTM attempts to automate systematic mapping studies by leveraging Latent Dirichlet Allocation (LDA) through topic modeling for efficient and comprehensive literature reviews.



## Getting Started

Clone the repository.

## Prerequisites

Python 3.8 or higher. 
Dependencies are listed in the `requirements.txt` file:

```
pip install -r requirements.txt
```

## Project Structure

The project is modular and structured as follows:

- `data/`: Data storage.

- `src/`: source code divided into submodules based on their role in the pipeline.

- `docs/`: Documentation.


### Modules

1. `data_extraction/`: Webcrawls data from the unArXive source.

2. `preprocessing/`: Sanitizes the input for topic modeling.

3. `topic_modeling/`: Implements the Latent Dirichlet Allocation (LDA) model.

4. `selection/`: Matching algorithm.

5. `mapping/`: Maps the results from topic modelling and selection.


## Authors

- **Tipu**
