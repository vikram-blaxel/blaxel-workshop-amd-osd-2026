import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
import httpx
from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.models.anthropic import AnthropicModel
#from strands.models.openai import OpenAIModel
#from strands.models.gemini import GeminiModel
from strands.tools.mcp import MCPClient
from blaxel.core import SandboxInstance, settings

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8000"))
app = FastAPI()

SYSTEM_PROMPT = """You are an expert Next.js developer with access to a sandbox environment. You can execute commands, manage files, and inspect processes inside the sandbox.

When given a task:
1. Think step by step about what needs to be done.
2. Use the available tools to interact with the sandbox.
3. Report results clearly and concisely.

"""

@app.post("/develop")
async def develop(request: Request):
    LLM_API_KEY = os.environ["ANTHROPIC_API_KEY"]
    #LLM_API_KEY = os.environ["OPENAI_API_KEY"]
    #LLM_API_KEY = os.environ["GOOGLE_API_KEY"]

    if not LLM_API_KEY:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY, OPENAI_API_KEY or GOOGLE_API_KEY env var is required")

    body = await request.json()
    task = body.get("task")
    if not task:
        raise HTTPException(status_code=400, detail="Request body must include a 'task' field")

    # create sandbox if it doesn't exist
    sandbox = await SandboxInstance.create_if_not_exists({
      "name": "my-sandbox-05",
      "image": "blaxel/nextjs:latest",
      "memory": 4096,
      "region": "us-pdx-1",
      "ttl": "1h"
    })
    print("OK: Sandbox created")

    # create public preview
    preview = await sandbox.previews.create_if_not_exists({
        "metadata": {"name": "myapp-preview"},
        "spec": {
            "port": 3000,
            "public": True
        }
    })
    url = preview.spec.url
    print(f"OK: Preview created at {url}")

    # configure model
    model = AnthropicModel(
        client_args={
            "api_key": LLM_API_KEY,
        },
        max_tokens=16000,
        model_id="claude-sonnet-4-6"
    )

    """
    model = OpenAIModel(
        client_args={
            "api_key": LLM_API_KEY,
        },
        model_id="gpt-4o",
        params={
            "max_tokens": 2048
        }
    )
    """

    """
    model = GeminiModel(
        client_args={
            "api_key": LLM_API_KEY,
        },
        model_id="gemini-3.1-flash-lite-preview",
        params={
            "max_output_tokens": 2048
        }
    )
    """

    # configure sandbox MCP access
    mcp_client = MCPClient(
        lambda: streamable_http_client(sandbox.metadata.url + "/mcp", http_client=httpx.AsyncClient(headers=settings.headers))
    )

    def log_callback(**kwargs):
        if kwargs.get("current_tool_use"):
            tool = kwargs["current_tool_use"]
            print(f"[tool] {tool.get('name')} — input: {tool.get('input')}")
        elif kwargs.get("data"):
            print(kwargs["data"], end="", flush=True)

    # run agent loop
    with mcp_client:
        agent = Agent(
            model=model,
            system_prompt=SYSTEM_PROMPT,
            tools=mcp_client.list_tools_sync(),
            callback_handler=log_callback,
        )
        result = agent(task)

        print("\n=== Agent response ===")
        print(result)
        print("OK: Agent session completed")

        print("\n=== Preview URL ===")
        print(url)

    return {"preview_url": url, "result": str(result)}

if __name__ == "__main__":
    print(f"Server listening on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

"""
curl -X POST http://localhost:8000/develop \
  -H "Content-Type: application/json" \
  -d '{"task": "Add a dark mode toggle to the homepage."}'

curl -X POST "https://agt-05-develop-webapp-nb1rct.bl.run/develop" \
  -H "Content-Type: application/json" \
  -H "X-Blaxel-Workspace: $BL_WORKSPACE" \
  -H "X-Blaxel-Authorization: Bearer $BL_API_KEY" \
  -d '{"task": "Add a dark mode toggle to the homepage."}'

bl run agent 05-develop-webapp/develop --data '{"task": "Add a dark mode toggle to the homepage."}'

curl -X POST http://localhost:8000/develop \
  -H "Content-Type: application/json" \
  -d '{"task": "Build a website for a new board game of your creation. Include an interactive demo so users can see how it works."}'
"""
