# Systematic Mapping Meets Topic Modelling
SMTM is a framework developed with the goal of aiding systematic mapping studies. By leveraging machine learning techniques, specifically Latent Dirichlet Allocation (LDA) for topic modeling, this framework aims to automate the process of systematic mapping and enhance the efficiency and comprehensiveness of literature reviews.



## Getting Started

Clone the repository to your local machine for development and testing purposes.

## Prerequisites

Ensure you have Python 3.8+ installed. All Python dependencies are listed in the `requirements.txt` file. Install them using:

```
pip install -r requirements.txt
```

## Project Structure

The project is modular and structured as follows:

- `data/`: This directory is where all the project data is stored, including raw data, preprocessed data, trained models, and final results.

- `src/`: This directory contains all the source code for the project, divided into specific submodules based on their role in the pipeline.

- `tests/`: Contains unit tests for all the modules.

- `docs/`: Documentation related to the project.

- `setup.py`: The setup script for distributing the project.

- `README.md`: Contains general information about the project, how to set it up, and how to use it.

### Modules

1. `data_extraction/`: Collects the data from the unArXive dataset.

2. `preprocessing/`: Cleans the text data and prepares it for topic modeling, including steps like removing stop words, lemmatization, tokenization, etc.

3. `topic_modeling/`: Implements the Latent Dirichlet Allocation (LDA) model used for topic modeling.

4. `selection/`: Implements a matching algorithm that matches research questions with relevant documents based on the topics inferred by the LDA model.

5. `mapping/`: Produces maps of the selected data for further analysis

## Running the tests

Each module comes with its own set of tests. Run these to ensure the correct functioning of the module's features. Make sure you're in the root directory of the project and use the following command:

```
python -m unittest discover -s tests
```

## Contributing

We welcome contributions to the project! Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## Authors

- **Philip Ngare**

See also the list of [contributors](https://github.com/tipu-254/SMTM/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Acknowledgments

I would like to thank...

*The remainder of this section will acknowledge any significant influences or resources used during the project development.*
