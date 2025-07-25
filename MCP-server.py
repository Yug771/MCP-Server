# server.py
import os
from fastmcp import FastMCP
from fastmcp.prompts.prompt import PromptMessage, TextContent

mcp = FastMCP(name="DocAssistant")

DOCS_DIR = "documents"

# Ensure the documents directory exists
os.makedirs(DOCS_DIR, exist_ok=True)

# RESOURCE: List available .txt docs
@mcp.resource("docs://list")
def list_docs():
    return [f for f in os.listdir(DOCS_DIR) if f.endswith(".txt")]

# RESOURCE TEMPLATE: Get content of a specific doc
@mcp.resource("docs://{filename}")
def get_doc(filename: str):
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path):
        return f"Error: {filename} not found."
    with open(path, encoding='utf-8') as f:
        return f.read()

# TOOL: Append text to a document
@mcp.tool()
def append_to_doc(filename: str, content: str) -> str:
    path = os.path.join(DOCS_DIR, filename)
    with open(path, "a", encoding='utf-8') as f:
        f.write(content)
    return f"✅ Appended to {filename}."

# TOOL: Search for keyword in a document
@mcp.tool()
def search_in_doc(filename: str, keyword: str) -> list[str]:
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path):
        return [f"Error: {filename} not found."]
    results = []
    with open(path, encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if keyword in line:
                results.append(f"{i}: {line.strip()}")
    return results or [f"No occurrences of '{keyword}' found."]

# PROMPT: Guide append usage
@mcp.prompt()
def append_prompt(filename: str, content: str) -> PromptMessage:
    text = (
        f"Please add the following to `{filename}`:\n\n{content}\n\n"
        "Use the append_to_doc tool."
    )
    return PromptMessage(role="user", content=TextContent(type="text", text=text))

# PROMPT: Guide search usage
@mcp.prompt()
def search_prompt(filename: str, keyword: str) -> PromptMessage:
    text = (
        f"I'm looking for occurrences of '{keyword}' in `{filename}`.\n"
        "Use the search_in_doc tool."
    )
    return PromptMessage(role="user", content=TextContent(type="text", text=text))

if __name__ == "__main__":
    mcp.run(transport="stdio")
