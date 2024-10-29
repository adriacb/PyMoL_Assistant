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

### Step 2: Start the Server
The server is responsible for handling requests and processing them using the LLM and RAG system.

To start the server, run:
```bash
fastapi dev src/server_lg.py
```

### Step 3: Start the Client in PyMOL
With the server running, you can start the client in PyMOL to interact with the assistant:
```bash
pymol src/pymol_run.py
```

### Step 4: Start the Client in PyMOL
Inside PyMOL, you can interact with the assistant using the `question` command.

```PyMoL
PyMoL> question("fetch the 6axg protein")
PyMoL> question("color by chain")
```