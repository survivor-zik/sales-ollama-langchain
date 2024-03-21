# Sales Automation Chat

This project has 2 branches, the main branch has the implementation of this project over open-source LLM, where as
**agents** branch has the implementation over OpenAI gpt3.5-turbo

## Description:

### This project is aiming towards sending cold emails and then continuing the conversation till forwarded to the admin.

## Requirements

1.First of all you must have Python=>3.11 [Install Python](https://www.python.org/downloads/)

2.Conda (for virtual environment) [How to download Ananaconda](https://www.anaconda.com/download)

3.CUDA 11.8 [Download Cuda kit](https://developer.nvidia.com/cuda-11-8-0-download-archive)

## Setting Up

To install the required dependencies, it's recommended to create a new Conda environment:

```
conda create -p venv python==3.11 -y
conda activate venv/
```

Install other dependencies

```
pip install -r requirements.txt
```

To use the OpenAI,create a .env

```commandline
OPENAI_API_KEY="your openai api key"
```

## Running the application

### 1.Using Jupyter Notebook named

```commandline
example.ipynb
```

### 2.Using Chainlit example:

```commandline
python main.py
```

