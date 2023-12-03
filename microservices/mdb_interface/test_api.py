# import requests

# data = {"rid": "656bd3244a2df2291eec37d2", "users": [4, 5]}

# r = requests.post("http://localhost:8005/deletecommunity", json=data)
# print("status:", r.status_code)
# print("json:", r.json())

import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        data = {"rid": "656bd3244a2df2291eec37d2", "users": [4, 5]}
        url = "http://localhost:8005/newcommunity"
        response = await session.post(url, json=data)
        print(await response.json(content_type="text/json"))


asyncio.run(main())
