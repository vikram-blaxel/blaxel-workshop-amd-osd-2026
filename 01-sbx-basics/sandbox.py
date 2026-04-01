import asyncio
from blaxel.core import SandboxInstance

async def main():

    # create sandbox if it doesn't exist
    sandbox = await SandboxInstance.create_if_not_exists({
      "name": "my-sandbox-01",
      "image": "blaxel/base-image:latest",   # public or custom image
      "memory": 4096,   # in MB
      "region": "us-pdx-1"   # deployment region
    })
    print("OK: Sandbox created")

if __name__ == "__main__":
    asyncio.run(main())
