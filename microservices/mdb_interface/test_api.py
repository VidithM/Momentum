# import requests

# data = {"rid": "656bd3244a2df2291eec37d2", "users": [4, 5]}

# r = requests.post("http://localhost:8005/deletecommunity", json=data)
# print("status:", r.status_code)
# print("json:", r.json())

import aiohttp
import asyncio


async def main():
    # async with aiohttp.ClientSession() as session:
    #     data = {"description": "nmcclaran"}
    #     url = "http://localhost:8011/getcommunity"
    #     response = await session.get(url, json=data)
    #     print(response)
    #     print(await response.json(content_type="application/json"))

    # async with aiohttp.ClientSession() as session:
    #     data = {
    #         "rid": "1",
    #         "username": "nmcclaran",
    #         "password": "Password",
    #         "name": "Nathan McClaran",
    #         "email": "nmcclaran@test.test",
    #     }
    #     url = "http://localhost:8080/updateuser"
    #     response = await session.post(url, json=data)
    #     print(response)

    async with aiohttp.ClientSession() as session:
        data = {
            "rid": "1",
        }
        url = "http://localhost:8080/getuser"
        response = await session.get(url, json=data)
        print(response)
        print(await response.json(content_type="application/json"))


asyncio.run(main())
