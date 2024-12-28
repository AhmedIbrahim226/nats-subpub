import asyncio
import json

import nats


async def main():
    nc = await nats.connect()

    async def subscriber_handler(msg):
        data = json.loads(msg.data.decode())
        search_id = str(data["search_id"])

        print(data["word"])
        print(search_id)

        await nc.publish(f"search_output.{search_id}", payload=b"Search Result" + search_id.encode())

    main_sub = await nc.subscribe("contentgrep", cb=subscriber_handler)

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.close()


if __name__ == '__main__':
    """
    Sub-server
    """
    asyncio.run(main())
