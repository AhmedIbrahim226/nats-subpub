import asyncio
import json

import nats


async def main(search_id):
    nc = await nats.connect()

    payloads = {"word": "word", "search_id": search_id}
    subpub = payloads["search_id"]

    await nc.publish("contentgrep", json.dumps(payloads).encode())

    async def subscriber_handler(msg):
        """
        Implement the save of the received data in the database.
        Implement send websocket message for the client.
        :param msg:
        :return:
        """
        print(msg.subject)
        print(msg.data)
        print("----------------------------")

    search_sub = await nc.subscribe(f"search_output.{subpub}", cb=subscriber_handler)

    """
    Must implement code to close the nc, depends on logic that tell us the all sub-servers had done of the all (subpub).
    """
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.close()


async def run():
    x = [main(i) for i in range(20)]
    await asyncio.gather(*x)


if __name__ == '__main__':
    """
    Suppose we running the run function in as celery task, asyncio.gather simulate the behavior of celery.
    """
    asyncio.run(run())
