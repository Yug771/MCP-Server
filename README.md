# DocAssistant: MCP Server & Client

This project demonstrates a simple client-server application for document management using the `fastmcp` library. The server provides a set of tools and resources for interacting with text files, and the client script shows how to use them. Communication between the client and server is handled over standard input/output (stdio), making it a lightweight and efficient solution for local inter-process communication.

## Project Structure

```
MCP-Server-And-Client/
├── documents/            # Stores all text documents
│   └── notes.txt         # An example document
├── MCP-client.py         # Example script to interact with the server
├── MCP-server.py         # The backend server logic
├── app.py                # Cloud-ready Streamlit app (no MCP dependencies)
├── requirements.txt      # Python dependencies for cloud deployment
├── requirements_local.txt # Full dependencies for local development
└── README.md             # This file
```

## Features

The `DocAssistant` server exposes several `fastmcp` endpoints:

### Resources

- **`docs://list`**: Lists all available `.txt` documents in the `documents` directory.
- **`docs://{filename}`**: Retrieves the full content of a specified document.

### Tools

- **`append_to_doc`**: Appends a string of content to the end of a specified file.
  - **Parameters**: `filename` (str), `content` (str)
- **`search_in_doc`**: Searches for a keyword within a document and returns the line numbers and content of all matches.
  - **Parameters**: `filename` (str), `keyword` (str)

### Prompts

- **`append_prompt`**: Generates a standardized message for appending content, intended to guide a user or another AI.
- **`search_prompt`**: Creates a standardized message for searching content.

## Setup & Installation

### 1. Prerequisites

- Python 3.8+
- An activated virtual environment (recommended)

### 2. Install Dependencies

For cloud deployment (Streamlit Cloud):
```bash
pip install -r requirements.txt
```

For local development with full MCP functionality:
```bash
# First, save the original requirements if needed
cp requirements.txt requirements_local.txt
# Then install from the local requirements
pip install fastmcp mcp
```

### 3. Running the Application

#### Option 1: Command Line Interface (Local Only)

The client and server run in a single, coordinated process. To start the application, simply run the client script from your terminal:

```bash
python MCP-client.py
```

The client will automatically start the server as a subprocess and begin interacting with it. You will see output from both the client and server in your terminal, demonstrating the various features of the `DocAssistant`.

#### Option 2: Web Interface (Works on Cloud)

For a more user-friendly experience, you can use the Streamlit web interface:

```bash
streamlit run app.py
```

This will open a beautiful web application in your browser where you can:
- List all available documents
- View document contents with syntax highlighting
- Append new content to documents
- Search for keywords within documents
- Download documents

The `app.py` version works on Streamlit Cloud as it doesn't require MCP subprocess communication.

## Cloud Deployment

### Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Deploy!

**Note**: The cloud version (`app.py`) implements document operations directly without MCP client-server architecture, making it compatible with cloud environments.

## How It Works

### Local Version (MCP-client.py + MCP-server.py)
The `MCP-client.py` script initializes a `StdioTransport` to manage communication with the `MCP-server.py` script. It then uses the `fastmcp` client to:

1.  **Ping the server** to ensure it's running.
2.  **List all available** tools, resources, and prompts.
3.  **Call the `append_to_doc` tool** to add a new line to `documents/notes.txt`.
4.  **Call the `search_in_doc` tool** to find occurrences of the word "Hello".
5.  **Read the entire content** of `documents/notes.txt` using its resource URI.
6.  **Generate a prompt message** using the `append_prompt` template.

### Cloud Version (app.py)
The cloud version directly implements file operations without requiring a separate server process, making it suitable for deployment on platforms like Streamlit Cloud where subprocess communication is restricted. 