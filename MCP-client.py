# client.py
import asyncio
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from fastmcp.client.logging import LogMessage

async def main():
    # Configure STDIO transport for local Python server
    transport = StdioTransport(
        command="python",
        args=["MCP-server.py"],
        env={},        # pass env vars explicitly if needed :contentReference[oaicite:1]{index=1}
        keep_alive=True
    )
    client = Client(
        transport,
    )

    async with client:
        # Ping & list endpoints
        alive = await client.ping()
        print("Server alive:", alive)

        tools = await client.list_tools()
        print("Tools:", [t.name for t in tools])

        resources = await client.list_resources()
        print("Resources:", [r.uri for r in resources])

        prompts = await client.list_prompts()
        print("Prompts:", [p.name for p in prompts])

        # Example: call append tool
        append_res = await client.call_tool("append_to_doc", {
            "filename": "notes.txt",
            "content": "Hello from MCP client!\n"
        })
        print("append_to_doc:", append_res.data)

        # Example: search keyword
        search_res = await client.call_tool("search_in_doc", {
            "filename": "notes.txt",
            "keyword": "Hello"
        })
        print("search_in_doc:\n", "\n".join(search_res.data))

        # Example: read full doc resource
        content = await client.read_resource("docs://notes.txt")
        print("Content of notes.txt:\n", content)

        # Example: use prompt template
        prompt_msg = await client.get_prompt("append_prompt", {
            "filename": "notes.txt",
            "content": "Another line from client."
        })
        print("Generated prompt:", prompt_msg)

if __name__ == "__main__":
    asyncio.run(main())
