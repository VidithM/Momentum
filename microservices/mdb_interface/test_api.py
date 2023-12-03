# import requests

# data = {"rid": "656bd3244a2df2291eec37d2", "users": [4, 5]}

# r = requests.post("http://localhost:8005/deletecommunity", json=data)
# print("status:", r.status_code)
# print("json:", r.json())

import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        data = {}
        url = "http://localhost:8005/getcommunity"
        response = await session.get(url, json=data)
        print(await response.json(content_type="application/json"))


asyncio.run(main())
