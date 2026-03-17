# utils.py
# دوال مساعدة عامة

import time
import uuid
import random
import json

def xor(s: str) -> str:
    """
    تطبيق عملية XOR على النص باستخدام القيمة 5.
    تستخدم لتشفير بسيط لرقم الهاتف أو البريد قبل الإرسال.
    """
    if not s:
        return ""
    return "".join([hex(ord(c) ^ 5)[2:] for c in str(s)])


def extract_passport_ticket(verify_json: dict) -> str:
    """
    استخراج passport_ticket من استجابة safe_verify.
    """
    data = verify_json.get('data', {})
    for key in ['passport_ticket', 'ticket', 'verify_ticket']:
        val = data.get(key)
        if val:
            return val
    return None


def generate_device_params() -> dict:
    """
    توليد بيانات جهاز عشوائية محاكية لأجهزة Android حقيقية.
    تُستخدم في دوال API للحصول على device_id و iid.
    """
    brands_by_manufacturer = {
        "Samsung": ["Galaxy S21", "Galaxy S22", "Galaxy Note20"],
        "OnePlus": ["NE2211", "OnePlus 9", "OnePlus 10"],
        "Xiaomi": ["Mi 11", "Redmi Note 12", "Poco X4"],
        "Huawei": ["P50", "Mate 40", "Nova 9"],
        "Motorola": ["Moto G100", "Moto Edge", "Moto X"],
        "Nokia": ["Nokia 8.3", "Nokia 5.4", "Nokia 3.4"],
        "Sony": ["Xperia 1", "Xperia 5", "Xperia 10"],
        "LG": ["LG Velvet", "LG Wing", "LG G8"],
        "Google": ["Pixel 6", "Pixel 7", "Pixel 7a"],
        "Oppo": ["Reno 7", "Find X5", "A74"],
    }

    manufacturer = random.choice(list(brands_by_manufacturer.keys()))
    brand = random.choice(brands_by_manufacturer[manufacturer])
    os_version = str(random.choice([9, 10, 11, 12, 13]))
    os_api = random.choice([28, 29, 30, 31, 33])
    language = random.choice(["en", "ar", "fr", "es", "id", "tr"])
    device_model = f"SM-{random.randint(1000,9999)}"

    return {
        "manufacturer": manufacturer,
        "brand": brand,
        "device_model": device_model,
        "os_version": os_version,
        "os_api": os_api,
        "language": language,
    }


def generate_trace_id() -> str:
    """توليد x-tt-trace-id عشوائي"""
    return f"00-{int(time.time() * 1000000):x}{random.randint(0, 0xffffffff):x}"


def now_ms() -> int:
    """الوقت الحالي بالملي ثانية"""
    return int(time.time() * 1000)


def now_sec() -> int:
    """الوقت الحالي بالثواني"""
    return int(time.time())