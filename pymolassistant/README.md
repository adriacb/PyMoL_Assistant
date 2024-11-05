# PyMOL Assistant - Usage Guide

This guide explains how to set up and use the PyMOL Assistant application, including instructions for running the server and client components and using the assistant within PyMOL.

## Prerequisites
Make sure you have the necessary environment and dependencies set up before starting:

- Conda environment (make sure it's already created with the necessary packages)
- FastAPI for the server
- PyMOL for the client interface

## Getting Started

### Step 1: Activate Conda Environment
Activate your conda environment to ensure all dependencies are available:

```bash
conda activate my_env
```

### Step 2: Configure the Vector Store URL
Before starting the server, configure the vector store URL by editing the src/db/config.yaml file to point to your PyMOL documentation vector store.

In src/db/config.yaml, add:
```
qdrant:
  collection_name: pymol-assistant
  url: enter_url_here
```
Replace enter_url_here with your actual Qdrant URL.

### Step 3: Set Up API Keys
In the src directory, create a .env file to store your API keys for Qdrant, OpenAI, and Anthropic. This file will provide the required authentication keys for the assistant to function correctly.

Create src/.env and add:

```
QDRANT_API_KEY=
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
```

### Step 4: Start the Server
The server is responsible for handling requests and processing them using the LLM and RAG system.

To start the server, run:
```bash
fastapi dev server_lg.py
```

### Step 5: Start the Client in PyMOL
With the server running, you can start the client in PyMOL to interact with the assistant:
```bash
pymol pymolassistant/pymol_run.py
```

### Step 6: Start the Client in PyMOL
Inside PyMOL, you can interact with the assistant using the `question` command.

```PyMoL
PyMoL> question("fetch the 6axg protein")
PyMoL> question("color by chain")
```