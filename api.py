import aiohttp
import asyncio

API_URL = "http://91.213.99.122:5001/api"

API_KEY = "a51d260ab3ded6e4c4ebe035b8cc611d"

# 1. request yuboruvchi funksiya
async def send_request(phone: str):
    async with aiohttp.ClientSession() as session:
        url = f"{API_URL}/request/"
        payload = {
            "api_key": API_KEY,
            "phone": phone
        }
        async with session.post(url, json=payload) as resp:
            return await resp.json()

# 2. verify qilish uchun funksiya
async def verify_request(request_id: int, code: str):
    async with aiohttp.ClientSession() as session:
        url = f"{API_URL}/verify/"
        payload = {
            "api_key": API_KEY,
            "request_id": request_id,
            "code": code
        }
        async with session.post(url, json=payload) as resp:
            return await resp.json()

# Test qilish uchun main()
async def main():
    # 1-chi bosqich: request yuborish
    response = await send_request("94 538-74-72")
    print("Request javobi:", response)

    # Masalan, request_id serverdan qaytadi
    request_id = response.get("request_id")  # fallback 2

    # 2-chi bosqich: verify qilish
    print("Request id:", request_id)
    verify_response = await verify_request(request_id, "123456")
    print("Verify javobi:", verify_response)

if __name__ == "__main__":
    asyncio.run(main())
