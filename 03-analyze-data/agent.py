import asyncio
import os
import httpx
from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.models.anthropic import AnthropicModel
#from strands.models.openai import OpenAIModel
#from strands.models.gemini import GeminiModel
from strands.tools.mcp import MCPClient
from blaxel.core import SandboxInstance

PROMPT = """You are an expert Python developer with access to a sandbox environment. You can execute commands, manage files, and inspect processes inside the sandbox.

When given a task:
1. Think step by step about what needs to be done.
2. Use the available tools to interact with the sandbox.
3. Report results clearly and concisely.

Your task is:
Read the data file at https://github.com/vikram-blaxel/blaxel-workshop-amd-osd-2026/blob/main/03-analyze-data/data.csv. Generate a bar chart of the data. Save the bar chart in the sandbox at /blaxel/chart.png. Install whatever tools you need as you go.
"""

async def main():

    BLAXEL_API_KEY = os.getenv("BL_API_KEY")
    LLM_API_KEY = os.environ["ANTHROPIC_API_KEY"]
    #LLM_API_KEY = os.environ["OPENAI_API_KEY"]
    #LLM_API_KEY = os.environ["GOOGLE_API_KEY"]
    HEADERS = {"Authorization": f"Bearer {BLAXEL_API_KEY}"}

    # create sandbox if it doesn't exist
    sandbox = await SandboxInstance.create_if_not_exists({
      "name": "my-sandbox-03",
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
        lambda: streamable_http_client(sandbox.metadata.url + "/mcp", http_client=httpx.AsyncClient(headers=HEADERS))
    )

    # run agent loop
    with mcp_client:
        agent = Agent(
            model=model,
            system_prompt=PROMPT,
            tools=mcp_client.list_tools_sync(),
            callback_handler=None,
        )
        result = agent("Execute the task described in the system prompt.")
        print("\n=== Agent response ===")
        print(result)
        print("OK: Agent session completed")

    await sandbox.fs.download("/blaxel/chart.png", "./chart.png")

if __name__ == "__main__":
    asyncio.run(main())
