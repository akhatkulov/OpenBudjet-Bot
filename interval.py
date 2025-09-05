import requests
import re
import time
import json
from typing import Dict, List, Optional, Tuple

# Config sozlamalari
CONFIG = {
    "api_key": "dc809dd040a18579b88c962b5a01300a",
    "captcha_url": "https://openbudget.uz/api/v2/vote/mvc/captcha/720d418c-1527-457c-ba19-3f836a31440b",
    "target_url": "https://openbudget.uz/api/v2/vote/mvc/captcha",
    "otp_endpoint": "https://openbudget.uz/api/v2/vote/mvc/verify",
    "twocaptcha_create": "https://api.2captcha.com/createTask",
    "twocaptcha_result": "https://api.2captcha.com/getTaskResult",
}

# Session umumiy bo‘lsin
session = requests.Session()

def get_default_headers() -> Dict[str, str]:
    """HTTP uchun default headers"""
    return {
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Origin": "https://openbudget.uz",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "iframe",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i"
    }

def extract_base64_images(html_content: str) -> List[str]:
    """HTML ichidan base64 rasm kodlarini ajratib olish"""
    pattern = r'data:image/png;base64,([A-Za-z0-9+/=]+)'
    return re.findall(pattern, html_content)

def create_captcha_task(base64_images: List[str]) -> Optional[int]:
    """2Captcha API orqali captcha task yaratish"""
    payload = {
        "clientKey": CONFIG["api_key"],
        "task": {
            "type": "CoordinatesTask",
            "body": base64_images[1],
            "imgInstructions": base64_images[0],
            "comment": "click 2 letters at image"
        }
    }
    response = session.post(CONFIG["twocaptcha_create"], json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("taskId")

def poll_captcha_solution(task_id: int, max_attempts: int = 20, delay: float = 1.0) -> Optional[Dict]:
    """2Captcha yechimini kutish"""
    for _ in range(max_attempts):
        time.sleep(delay)
        response = session.post(CONFIG["twocaptcha_result"], json={
            "clientKey": CONFIG["api_key"],
            "taskId": task_id
        })
        response.raise_for_status()
        result = response.json()
        if result.get("status") == "ready":
            return result.get("solution", {})
    return None

def fetch_captcha() -> Tuple[Dict[str, str], List[str]]:
    """Captcha sahifasini olib kelish"""
    headers = get_default_headers()
    response = session.get(CONFIG["captcha_url"], headers=headers)
    response.raise_for_status()
    
    cookies = response.cookies.get_dict()
    base64_images = extract_base64_images(response.text)
    
    if len(base64_images) < 2:
        raise ValueError("Base64 rasmlar topilmadi")
    
    return cookies, base64_images

def solve_captcha(base64_images: List[str]) -> List[Dict[str, int]]:
    """2Captcha yordamida yechish"""
    task_id = create_captcha_task(base64_images)
    if not task_id:
        raise RuntimeError("Captcha task yaratilmagan")
    
    solution = poll_captcha_solution(task_id)
    if not solution:
        raise RuntimeError("Captcha yechimi topilmadi (timeout)")
    
    coordinates = solution.get("coordinates", [])
    if len(coordinates) < 2:
        raise ValueError("2Captcha noto‘g‘ri natija qaytardi")
    
    return coordinates

def submit_phone_number(phone_number: str, cookies: Dict[str, str], coordinates: List[Dict[str, int]]) -> requests.Response:
    """Telefon raqamni captcha bilan yuborish"""
    request_body = {
        "phoneNumber": phone_number,
        "points": json.dumps([
            {"id": f"{coordinates[0]['x']}{coordinates[0]['y']}", "x": coordinates[0]['x'], "y": coordinates[0]['y']},
            {"id": f"{coordinates[1]['x']}{coordinates[1]['y']}", "x": coordinates[1]['x'], "y": coordinates[1]['y']}
        ])
    }
    
    headers = get_default_headers()
    headers["Referer"] = CONFIG["captcha_url"]
    
    response = session.post(CONFIG["target_url"], data=request_body, cookies=cookies, headers=headers)
    return response


def submit_phone_number_for_otp(phone_number: str) -> Dict[str, any]:
    """Bitta funksiya orqali telefon raqam yuborish"""
    try:
        cookies, base64_images = fetch_captcha()
        coordinates = solve_captcha(base64_images)
        captcha_response = submit_phone_number(phone_number, cookies, coordinates)
        
        with open("sms.html", "w") as f:
            f.write(captcha_response.text)
        
        if captcha_response.status_code != 200:
            return {
                "error": f"Xatolik: {captcha_response.status_code}",
                "captcha_status": captcha_response.status_code,
                "captcha_headers": dict(captcha_response.headers),
                "cookies": None
            }
        
        return {
            "captcha_status": captcha_response.status_code,
            "captcha_headers": dict(captcha_response.headers),
            "cookies": cookies
        }
    except Exception as e:
        return {"error": str(e), "cookies": None}

def main():
    phone_number = "77 251-12-32"
    result = submit_phone_number_for_otp(phone_number)
    print(json.dumps(result, indent=2))
    
    if result.get("cookies"):
        print("Telefoningizga SMS keldi, OTP kiriting:")
        otp_code = input("OTP: ")
        otp_result = verify_otp(otp_code, result["cookies"])
        print(json.dumps(otp_result, indent=2))
    else:
        print("OTP uchun cookies olinmadi")

if __name__ == "__main__":
    main()
