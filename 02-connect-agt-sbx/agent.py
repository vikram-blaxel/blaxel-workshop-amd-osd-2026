import asyncio
import os
import httpx
from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.models.anthropic import AnthropicModel
#from strands.models.openai import OpenAIModel
#from strands.models.gemini import GeminiModel
from strands.tools.mcp import MCPClient
from blaxel.core import SandboxInstance, settings

PROMPT = """You are an expert developer with access to a sandbox environment. You can execute commands, manage files, and inspect processes inside the sandbox.

When given a task:
1. Think step by step about what needs to be done.
2. Use the available tools to interact with the sandbox.
3. Report results clearly and concisely.
"""

async def main():

    LLM_API_KEY = os.environ["ANTHROPIC_API_KEY"]
    #LLM_API_KEY = os.environ["OPENAI_API_KEY"]
    #LLM_API_KEY = os.environ["GOOGLE_API_KEY"]

    # create sandbox if it doesn't exist
    sandbox = await SandboxInstance.create_if_not_exists({
      "name": "my-sandbox-02",
      "image": "blaxel/base-image:latest",
      "memory": 4096,
      "region": "us-pdx-1"
    })
    print("OK: Sandbox created")

    # configure model
    model = AnthropicModel(
        client_args={
            "api_key": LLM_API_KEY,
        },

        max_tokens=2048,
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

    # run agent loop
    with mcp_client:
        agent = Agent(
            model=model,
            system_prompt=PROMPT,
            tools=mcp_client.list_tools_sync(),
            callback_handler=None,
        )
        result = agent("List the files in the current directory.")
        print("\n=== Agent response ===")
        print(result)
        print("OK: Agent session completed")

if __name__ == "__main__":
    asyncio.run(main())
