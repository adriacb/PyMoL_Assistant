# PyMOL Assistant

PyMOL Assistant is a Python application designed to simplify interactions with PyMOL. Leveraging LLM agents and a Retrieval-Augmented Generation (RAG) system, this assistant helps execute PyMOL commands with ease, offering friendly feedback and guidance when needed.

## Features
- **LLM-Powered Assistance**: Uses Large Language Model agents to interpret and execute PyMOL commands.
- **RAG System**: Provides accurate and relevant responses by retrieving information from reliable sources.
- **Interactive Feedback**: Offers user-friendly feedback, guiding users through PyMOL commands and troubleshooting issues.

## Installation

### Prerequisites
- Anaconda
- Python 3.8+
- PyMoL (open-source)
- [Poetry](https://python-poetry.org/) for dependency management

### Installation
1. Clone this repository:
```bash
git clone https://github.com/adriacb/PyMoL_Assistant.git
cd PyMoL_Assistant/
```
2. Create conda environment & install PyMoL
```bash
conda create -n Pymol -c conda-forge pymol-open-source
```

3. Install dependencies
```bash
poetry install
``` 

### How to Use It
For detailed usage instructions, please refer to the [detailed usage guide](pymol-assistant/README.md).


### Project Structure
```
pymol-assistant
|── main files
├── prep                   # Preparation scripts
├── poetry.lock            # Dependency lock file
├── pyproject.toml         # Project configuration
└── README.md              # Project documentation
tests                      # Unit and integration tests
dist                       # Distribution files
``` 

### License
This project is licensed under the MIT License. See the LICENSE file for details.