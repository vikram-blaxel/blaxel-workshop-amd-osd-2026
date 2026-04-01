import asyncio
from blaxel.core import SandboxInstance

async def main():

    # create sandbox if it doesn't exist
    sandbox = await SandboxInstance.create_if_not_exists({
      "name": "my-sandbox-04",
      "image": "blaxel/nextjs:latest",
      "memory": 4096,
      "region": "us-pdx-1"
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
    # get preview URL
    url = preview.spec.url
    print(f"OK: Preview created at {url}")

    # write file
    process = await sandbox.process.exec({
      "command": "sed -i 's/To get started, edit the page.tsx file./Hello, Open Source Day!/' /blaxel/app/src/app/page.tsx"
    })
    print("OK: Command executed")

    # start server
    process = await sandbox.process.exec({
      "command": "npm start"
    })
    print("OK: Server started")

if __name__ == "__main__":
    asyncio.run(main())
