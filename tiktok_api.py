# tiktok_api.py
# دوال التفاعل مع خوادم TikTok (نسخة محسنة مع توليد ديناميكي)

import requests
import time
import urllib.parse
import json
import uuid
import random
from hsopyt import Gorgon, Ladon, Argus, md5
from utils import xor, generate_device_params, generate_trace_id, now_ms, now_sec

# ثوابت عامة
AID = 567753
LICENSE_ID = 1611921764
APP_NAME = "tiktok_studio"
VERSION_CODE = "370301"
VERSION_NAME = "37.3.1"
SDK_VERSION = "6031690"
DEVICE_BRAND = "samsung"  # سيتم توليده ديناميكياً لاحقاً
DEVICE_TYPE = "SM-A035F"  # سيتم توليده ديناميكياً
OPENUDID = None  # سيتم توليده

# ملاحظة: المكتبة hsopyt يجب تثبيتها بشكل منفصل


def get_device():
    """
    تسجيل جهاز جديد لدى TikTok وإرجاع device_id و iid.
    تعتمد على توليد بيانات عشوائية.
    """
    params = generate_device_params()
    manufacturer = params["manufacturer"]
    brand = params["brand"]
    device_model = params["device_model"]
    os_version = params["os_version"]
    os_api = params["os_api"]
    language = params["language"]

    ts_ms = now_ms()
    ts_s = now_sec()

    # إنشاء معرفات عشوائية
    clientudid = str(uuid.uuid4())
    openudid = uuid.uuid4().hex
    cdid = str(uuid.uuid4())
    req_id = str(uuid.uuid4())
    sig_hash = uuid.uuid4().hex
    git_hash = uuid.uuid4().hex[:7]

    # بناء الـ payload للتسجيل
    payload = {
        "header": {
            "os": "Android",
            "os_version": os_version,
            "os_api": os_api,
            "device_model": device_model,
            "device_brand": brand,
            "device_manufacturer": manufacturer,
            "cpu_abi": "arm64-v8a",
            "density_dpi": 240,
            "display_density": "hdpi",
            "resolution": "900x1600",
            "display_density_v2": "hdpi",
            "resolution_v2": "1600x900",
            "access": "wifi",
            "language": language,
            "timezone": 3,
            "tz_name": "Asia/Baghdad",
            "tz_offset": 10800,
            "sim_region": "us",
            "carrier": random.choice(["AT&T", "Verizon", "T-Mobile"]),
            "mcc_mnc": "310410",
            "clientudid": clientudid,
            "openudid": openudid,
            "channel": "googleplay",
            "not_request_sender": 1,
            "aid": 1233,
            "release_build": f"d8db25e_{random.randint(20250000,20259999)}",
            "ab_version": "40.7.3",
            "gaid_limited": 0,
            "custom": {
                "ram_size": random.choice(["2GB", "3GB", "4GB"]),
                "dark_mode_setting_value": 1,
                "is_foldable": 0,
                "screen_height_dp": 1067,
                "apk_last_update_time": ts_ms,
                "filter_warn": 0,
                "priority_region": "US",
                "user_period": 0,
                "is_kids_mode": 0,
                "web_ua": f"Dalvik/2.1.0 (Linux; U; Android {os_version}; SM-NE2211 Build/SKQ1.220617.001)",
                "screen_width_dp": 648,
                "user_mode": -1,
            },
            "package": "com.zhiliaoapp.musically",
            "app_version": "40.7.3",
            "app_version_minor": "",
            "version_code": 400703,
            "update_version_code": 2024007030,
            "manifest_version_code": 2024007030,
            "app_name": "musical_ly",
            "tweaked_channel": "googleplay",
            "display_name": "TikTok",
            "sig_hash": sig_hash,
            "cdid": cdid,
            "device_platform": "android",
            "git_hash": git_hash,
            "sdk_version_code": 2050990,
            "sdk_target_version": 30,
            "req_id": req_id,
            "sdk_version": "2.5.9",
            "guest_mode": 0,
            "sdk_flavor": "i18nInner",
            "apk_first_install_time": ts_ms,
            "is_system_app": 0,
        },
        "magic_tag": "ss_app_log",
        "_gen_time": ts_ms,
    }

    # بناء معاملات URL
    params_url = {
        "req_id": req_id,
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "_rticket": str(ts_ms),
        "cdid": cdid,
        "channel": "googleplay",
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "400703",
        "version_name": "40.7.3",
        "manifest_version_code": "2024007030",
        "update_version_code": "2024007030",
        "ab_version": "40.7.3",
        "resolution": "1600*900",
        "dpi": "240",
        "device_type": device_model,
        "device_brand": brand,
        "language": language,
        "os_api": str(os_api),
        "os_version": os_version,
        "ac": "wifi",
        "is_pad": "0",
        "app_type": "normal",
        "sys_region": "US",
        "last_install_time": str(ts_s),
        "mcc_mnc": "310410",
        "timezone_name": "Asia/Baghdad",
        "carrier_region_v2": "310",
        "app_language": language,
        "carrier_region": "US",
        "timezone_offset": "10800",
        "host_abi": "arm64-v8a",
        "locale": language,
        "ac2": "unknown",
        "uoo": "1",
        "op_region": "US",
        "build_number": "40.7.3",
        "region": "US",
        "ts": str(ts_s),
        "openudid": openudid,
        "okhttp_version": "4.2.228.19-tiktok",
        "use_store_region_cookie": "1",
    }

    headers = {
        "User-Agent": f"com.zhiliaoapp.musically/2024007030 (Linux; U; Android {os_version}; {language}; {device_model}; Build/SKQ1.220617.001;tt-ok/3.12.13.20)",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json; charset=utf-8",
        "x-tt-app-init-region": "carrierregion=US;mccmnc=310410;sysregion=US;appregion=US",
        "x-tt-request-tag": "t=0;n=1",
        "x-tt-dm-status": "login=0;ct=0;rt=7",
        "sdk-version": "2",
        "passport-sdk-version": "-1",
        "x-vc-bdturing-sdk-version": "2.3.13.i18n",
    }

    response = requests.post(
        "https://log-boot.tiktokv.com/service/2/device_register/",
        json=payload,
        headers=headers,
        params=params_url,
    )

    data = response.json()
    device_id = data.get("device_id_str", "")
    iid = data.get("install_id_str", "")

    return device_id, iid, openudid, cdid, device_model, brand, os_version, os_api, language


def sign_number(params_str: str, payload_str: str = None, sec_device_id: str = '', cookie: str = None, aid: int = AID, license_id: int = LICENSE_ID):
    """توليد التوقيعات للطلبات المرتبطة برقم الهاتف"""
    x_ss_stub = md5(payload_str.encode('utf-8')).hexdigest() if payload_str else md5("".encode('utf-8')).hexdigest()
    unix = time.time()
    gorgon_data = Gorgon(params_str, unix, payload_str, cookie).get_value()
    ladon_value = Ladon.encrypt(int(unix), license_id, aid)
    argus_value = Argus.get_sign(
        params_str,
        x_ss_stub,
        int(unix),
        platform=0,
        aid=aid,
        license_id=license_id,
        sec_device_id=sec_device_id,
        sdk_version='v05.00.06-ov-android',
        sdk_version_int=167775296
    )
    return {
        'x-gorgon': gorgon_data['x-gorgon'],
        'x-khronos': gorgon_data['x-khronos'],
        'content-length': str(len(payload_str)) if payload_str else "0",
        'x-ss-stub': x_ss_stub.upper(),
        'x-ladon': ladon_value,
        'x-argus': argus_value
    }


def sign_email(params: str, payload: str = None, sec_device_id: str = '', cookie: str = None, aid: int = AID, license_id: int = LICENSE_ID, unix: float = None):
    """توليد التوقيعات للطلبات المرتبطة بالبريد الإلكتروني"""
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload else md5("".encode('utf-8')).hexdigest()
    if not unix:
        unix = time.time()
    gorgon_data = Gorgon(params, unix, payload, cookie).get_value()
    return {
        'x-gorgon': gorgon_data['x-gorgon'],
        'x-khronos': gorgon_data['x-khronos'],
        'content-length': str(len(payload)) if payload else "0",
        'x-ss-stub': x_ss_stub.upper(),
        'x-ladon': Ladon.encrypt(int(unix), license_id, aid),
        'x-argus': Argus.get_sign(params, x_ss_stub, int(unix),
            platform=0,
            aid=aid,
            license_id=license_id,
            sec_device_id=sec_device_id,
            sdk_version='v05.00.06-ov-android',
            sdk_version_int=167775296
        )
    }


def send_code_number(session_id: str, mobile: str, iid: str, device_id: str, openudid: str, cdid: str, device_model: str, brand: str, os_version: str, os_api: int, language: str) -> requests.Response:
    """إرسال رمز التحقق لربط رقم الهاتف"""
    mobile_encoded = xor(mobile)
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/mobile/send_code/v1/"
    ts = now_sec()
    rticket = now_ms()
    
    params = {
        'passport-sdk-version': SDK_VERSION,
        'iid': iid,
        'device_id': device_id,
        'ac': "WIFI",
        'channel': "googleplay",
        'aid': str(AID),
        'app_name': APP_NAME,
        'version_code': VERSION_CODE,
        'version_name': VERSION_NAME,
        'device_platform': "android",
        'os': "android",
        'ab_version': VERSION_NAME,
        'ssmix': "a",
        'device_type': device_model,
        'device_brand': brand,
        'language': language,
        'os_api': str(os_api),
        'os_version': os_version,
        'openudid': openudid,
        'manifest_version_code': VERSION_CODE,
        'resolution': "720*1504",
        'dpi': "320",
        'update_version_code': VERSION_CODE,
        '_rticket': str(rticket),
        'is_pad': "0",
        'current_region': "EG",
        'app_type': "normal",
        'sys_region': "EG",
        'last_install_time': str(ts - 10000),
        'mcc_mnc': "60202",
        'timezone_name': "Africa%2FCairo",
        'carrier_region_v2': "602",
        'residence': "EG",
        'app_language': language,
        'carrier_region': "EG",
        'ac2': "wifi",
        'uoo': "0",
        'op_region': "EG",
        'timezone_offset': "7200",
        'build_number': VERSION_NAME,
        'host_abi': "arm64-v8a",
        'locale': language,
        'region': "EG",
        'ts': str(ts),
        'cdid': cdid,
        'support_webview': "1",
        'reg_store_region': "EG",
        'user_selected_region': "0",
        'cronet_version': "f6248591_2024-09-11",
        'ttnet_version': "4.2.195.9-tiktok",
        'use_store_region_cookie': "1",
        'app_version': VERSION_NAME
    }
    payload_data = {
        'check_register': "1",
        'auto_read': "1",
        'account_sdk_source': "app",
        'unbind_exist': "35",
        'mix_mode': "1",
        'mobile': mobile_encoded,
        'is6Digits': "1",
        'multi_login': "1",
        'type': "3d"
    }
    params_str = urllib.parse.urlencode(params)
    payload_str = urllib.parse.urlencode(payload_data)
    m = sign_number(params_str=params_str, payload_str=payload_str, cookie=f"sessionid={session_id}")
    headers = {
        'User-Agent': f"com.ss.android.tt.creator/370301 (Linux; U; Android {os_version}; {language}; {device_model}; Build/RP1A.201005.001; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",
        'x-tt-pba-enable': "1",
        'tt-ticket-guard-public-key': "BLvf2Dh6OP6Fgfjwkztn7WhreT5zaRhpS0qld8Um1R4KXrNVWp3W1rWQ5NDxvBIhXPcOtaCAE5FJaes7RaGovSA=",
        'tt-ticket-guard-iteration-version': "0",
        'x-bd-kmsv': "0",
        'x-tt-dm-status': "login=1;ct=1;rt=1",
        'x-ss-req-ticket': str(rticket + 13),
        'sdk-version': "2",
        'tt-ticket-guard-version': "3",
        'passport-sdk-settings': "x-tt-token",
        'passport-sdk-sign': "x-tt-token",
        'passport-sdk-version': SDK_VERSION,
        'x-vc-bdturing-sdk-version': "2.3.8.i18n",
        'x-tt-request-tag': "n=0;nr=011;bg=0",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'rpc-persist-pyxis-policy-v-tnc': "1",
        'x-ss-dp': str(AID),
        'x-tt-trace-id': generate_trace_id(),
        'x-tt-dataflow-id': "671088640",
        'x-argus': m['x-argus'],
        'x-gorgon': m['x-gorgon'],
        'x-khronos': m['x-khronos'],
        'x-ladon': m['x-ladon'],
        'x-ss-stub': m['x-ss-stub'],
        'content-length': m['content-length'],
        'Cookie': f"sessionid={session_id}"
    }
    response = requests.post(url, params=params, data=payload_data, headers=headers)
    return response


def bind_mobile(session_id: str, mobile: str, code: str, iid: str, device_id: str, openudid: str, cdid: str, device_model: str, brand: str, os_version: str, os_api: int, language: str) -> requests.Response:
    """تأكيد ربط رقم الهاتف باستخدام الرمز"""
    mobile_encoded = xor(mobile)
    code_encoded = xor(code)
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/mobile/bind/v1/"
    ts = now_sec()
    rticket = now_ms()
    
    params = {
        'passport-sdk-version': SDK_VERSION,
        'iid': iid,
        'device_id': device_id,
        'ac': "WIFI",
        'channel': "googleplay",
        'aid': str(AID),
        'app_name': APP_NAME,
        'version_code': VERSION_CODE,
        'version_name': VERSION_NAME,
        'device_platform': "android",
        'os': "android",
        'ab_version': VERSION_NAME,
        'ssmix': "a",
        'device_type': device_model,
        'device_brand': brand,
        'language': language,
        'os_api': str(os_api),
        'os_version': os_version,
        'openudid': openudid,
        'manifest_version_code': VERSION_CODE,
        'resolution': "720*1504",
        'dpi': "320",
        'update_version_code': VERSION_CODE,
        '_rticket': str(rticket),
        'is_pad': "0",
        'current_region': "EG",
        'app_type': "normal",
        'sys_region': "EG",
        'last_install_time': str(ts - 10000),
        'mcc_mnc': "60202",
        'timezone_name': "Africa%2FCairo",
        'carrier_region_v2': "602",
        'residence': "EG",
        'app_language': language,
        'carrier_region': "EG",
        'ac2': "wifi",
        'uoo': "0",
        'op_region': "EG",
        'timezone_offset': "7200",
        'build_number': VERSION_NAME,
        'host_abi': "arm64-v8a",
        'locale': language,
        'region': "EG",
        'ts': str(ts),
        'cdid': cdid,
        'support_webview': "1",
        'cronet_version': "f6248591_2024-09-11",
        'ttnet_version': "4.2.195.9-tiktok",
        'use_store_region_cookie': "1",
        'app_version': VERSION_NAME
    }
    payload_data = {
        'phone_number_source': "1",
        'code': code_encoded,
        'account_sdk_source': "app",
        'unbind_exist': "35",
        'mix_mode': "1",
        'mobile': mobile_encoded,
        'multi_login': "1"
    }
    params_str = urllib.parse.urlencode(params)
    payload_str = urllib.parse.urlencode(payload_data)
    m = sign_number(params_str=params_str, payload_str=payload_str, cookie=f"sessionid={session_id}")
    headers = {
        'User-Agent': f"com.ss.android.tt.creator/370301 (Linux; U; Android {os_version}; {language}; {device_model}; Build/RP1A.201005.001; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",
        'x-tt-pba-enable': "1",
        'tt-ticket-guard-public-key': "BLvf2Dh6OP6Fgfjwkztn7WhreT5zaRhpS0qld8Um1R4KXrNVWp3W1rWQ5NDxvBIhXPcOtaCAE5FJaes7RaGovSA=",
        'tt-ticket-guard-iteration-version': "0",
        'x-bd-kmsv': "0",
        'x-tt-dm-status': "login=1;ct=1;rt=1",
        'x-ss-req-ticket': str(rticket + 19),
        'sdk-version': "2",
        'tt-ticket-guard-version': "3",
        'passport-sdk-settings': "x-tt-token",
        'passport-sdk-sign': "x-tt-token",
        'passport-sdk-version': SDK_VERSION,
        'x-vc-bdturing-sdk-version': "2.3.8.i18n",
        'x-tt-request-tag': "n=0;nr=011;bg=0",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'rpc-persist-pyxis-policy-v-tnc': "1",
        'x-ss-dp': str(AID),
        'x-tt-trace-id': generate_trace_id(),
        'x-tt-dataflow-id': "671088640",
        'x-argus': m['x-argus'],
        'x-gorgon': m['x-gorgon'],
        'x-khronos': m['x-khronos'],
        'x-ladon': m['x-ladon'],
        'x-ss-stub': m['x-ss-stub'],
        'content-length': m['content-length'],
        'Cookie': f"sessionid={session_id}"
    }
    response = requests.post(url, params=params, data=payload_data, headers=headers)
    return response


def safe_verify_email(session_id: str, iid: str, device_id: str, openudid: str, cdid: str, device_model: str, brand: str, os_version: str, os_api: int, language: str) -> requests.Response:
    """التحقق الأمني قبل ربط البريد الإلكتروني"""
    url = "https://api19-normal-c-alisg.tiktokv.com/passport/shark/safe_verify/v2/"
    ts = now_sec()
    rticket = now_ms()
    
    params = {
        'passport-sdk-version': SDK_VERSION,
        'iid': iid,
        'device_id': device_id,
        'ac': "WIFI",
        'channel': "googleplay",
        'aid': str(AID),
        'app_name': APP_NAME,
        'version_code': VERSION_CODE,
        'version_name': VERSION_NAME,
        'device_platform': "android",
        'os': "android",
        'ab_version': VERSION_NAME,
        'ssmix': "a",
        'device_type': device_model,
        'device_brand': brand,
        'language': language,
        'os_api': str(os_api),
        'os_version': os_version,
        'openudid': openudid,
        'manifest_version_code': VERSION_CODE,
        'resolution': "720*1465",
        'dpi': "300",
        'update_version_code': VERSION_CODE,
        '_rticket': str(rticket + 6),
        'is_pad': "0",
        'current_region': "SA",
        'app_type': "normal",
        'sys_region': "AE",
        'last_install_time': str(ts - 10000),
        'timezone_name': "Asia/Riyadh",
        'residence': "SA",
        'app_language': language,
        'ac2': "wifi5g",
        'uoo': "0",
        'op_region': "SA",
        'timezone_offset': "10800",
        'build_number': VERSION_NAME,
        'host_abi': "arm64-v8a",
        'locale': language,
        'region': "AE",
        'ts': str(ts),
        'cdid': cdid,
        'support_webview': "1",
        'reg_store_region': "sa",
        'cronet_version': "f6248591_2024-09-11",
        'ttnet_version': "4.2.195.9-tiktok",
        'use_store_region_cookie': "1",
        "app_version": "28.6.5"  # ملاحظة: بعض الطلبات تستخدم إصدار مختلف
    }
    payload_data = {
        'product_scene': "37",
        'mix_mode': "1"
    }
    params_str = urllib.parse.urlencode(params)
    payload_str = urllib.parse.urlencode(payload_data)
    # هنا نستخدم sign_email لأن safe_verify للبريد يستخدم توقيعات البريد
    m = sign_email(params=params_str, payload=payload_str, cookie=None)
    headers = {
        'User-Agent': f"com.ss.android.tt.creator/370301 (Linux; U; Android {os_version}; {language}; {device_model}; Build/TP1A.220624.014; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",
        'x-tt-pba-enable': "1",
        'x-bd-kmsv': "0",
        'x-tt-dm-status': "login=1;ct=1;rt=8",
        'x-ss-req-ticket': str(rticket + 53),
        'sdk-version': "2",
        'tt-ticket-guard-iteration-version': "0",
        'tt-ticket-guard-version': "3",
        'passport-sdk-version': SDK_VERSION,
        'x-ss-stub': m['x-ss-stub'],
        'x-tt-store-region': "sa",
        'x-tt-store-region-src': "uid",
        'rpc-persist-pyxis-policy-v-tnc': "1",
        'x-ss-dp': str(AID),
        'x-tt-trace-id': generate_trace_id(),
        'x-tt-dataflow-id': "671088640",
        'x-argus': m['x-argus'],
        'x-gorgon': m['x-gorgon'],
        'x-khronos': m['x-khronos'],
        'x-ladon': m['x-ladon'],
        'Cookie': f"sessionid={session_id}"
    }
    response = requests.post(url, params=params, data=payload_data, headers=headers)
    return response


def send_email_code(session_id: str, email: str, iid: str, device_id: str, openudid: str, cdid: str, device_model: str, brand: str, os_version: str, os_api: int, language: str) -> requests.Response:
    """إرسال رمز التحقق للبريد الإلكتروني"""
    email_encoded = xor(email)
    url = "https://api19-normal-c-alisg.tiktokv.com/passport/email/send_code/"
    ts = now_sec()
    rticket = now_ms()
    
    params = {
        'passport-sdk-version': SDK_VERSION,
        'iid': iid,
        'device_id': device_id,
        'ac': "WIFI",
        'channel': "googleplay",
        'aid': str(AID),
        'app_name': APP_NAME,
        'version_code': VERSION_CODE,
        'version_name': VERSION_NAME,
        'device_platform': "android",
        'os': "android",
        'ab_version': VERSION_NAME,
        'ssmix': "a",
        'device_type': device_model,
        'device_brand': brand,
        'language': language,
        'os_api': str(os_api),
        'os_version': os_version,
        'openudid': openudid,
        'manifest_version_code': VERSION_CODE,
        'resolution': "720*1465",
        'dpi': "300",
        'update_version_code': VERSION_CODE,
        '_rticket': str(rticket + 6),
        'is_pad': "0",
        'current_region': "SA",
        'app_type': "normal",
        'sys_region': "AE",
        'last_install_time': str(ts - 10000),
        'timezone_name': "Asia/Riyadh",
        'residence': "SA",
        'app_language': language,
        'ac2': "wifi5g",
        'uoo': "0",
        'op_region': "SA",
        'timezone_offset': "10800",
        'build_number': VERSION_NAME,
        'host_abi': "arm64-v8a",
        'locale': language,
        'region': "AE",
        'ts': str(ts),
        'cdid': cdid,
        'support_webview': "1",
        'reg_store_region': "sa",
        'cronet_version': "f6248591_2024-09-11",
        'ttnet_version': "4.2.195.9-tiktok",
        'use_store_region_cookie': "1",
        "app_version": "28.6.5"
    }
    payload_data = {
        'rules_version': "v2",
        'account_sdk_source': "app",
        'mix_mode': "1",
        'multi_login': "1",
        'type': "3d",
        'email': email_encoded,
        'email_theme': "0"
    }
    params_str = urllib.parse.urlencode(params)
    payload_str = urllib.parse.urlencode(payload_data)
    m = sign_email(params=params_str, payload=payload_str, cookie=None)
    headers = {
        'User-Agent': f"com.ss.android.tt.creator/370301 (Linux; U; Android {os_version}; {language}; {device_model}; Build/TP1A.220624.014; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",
        'x-tt-pba-enable': "1",
        'x-bd-kmsv': "0",
        'x-tt-dm-status': "login=1;ct=1;rt=8",
        'x-ss-req-ticket': str(rticket + 53),
        'sdk-version': "2",
        'tt-ticket-guard-iteration-version': "0",
        'tt-ticket-guard-version': "3",
        'passport-sdk-version': SDK_VERSION,
        'x-ss-stub': m['x-ss-stub'],
        'x-tt-store-region': "sa",
        'x-tt-store-region-src': "uid",
        'rpc-persist-pyxis-policy-v-tnc': "1",
        'x-ss-dp': str(AID),
        'x-tt-trace-id': generate_trace_id(),
        'x-tt-dataflow-id': "671088640",
        'x-argus': m['x-argus'],
        'x-gorgon': m['x-gorgon'],
        'x-khronos': m['x-khronos'],
        'x-ladon': m['x-ladon'],
        'Cookie': f"sessionid={session_id}"
    }
    response = requests.post(url, params=params, data=payload_data, headers=headers)
    return response


def bind_email(session_id: str, email: str, code: str, iid: str, device_id: str, openudid: str, cdid: str, device_model: str, brand: str, os_version: str, os_api: int, language: str) -> requests.Response:
    """تأكيد ربط البريد الإلكتروني"""
    email_encoded = xor(email)
    code_encoded = xor(code)
    url = "https://api19-normal-c-alisg.tiktokv.com/passport/email/bind/"
    ts = now_sec()
    rticket = now_ms()
    
    params = {
        'passport-sdk-version': SDK_VERSION,
        'iid': iid,
        'device_id': device_id,
        'ac': "WIFI",
        'channel': "googleplay",
        'aid': str(AID),
        'app_name': APP_NAME,
        'version_code': VERSION_CODE,
        'version_name': VERSION_NAME,
        'device_platform': "android",
        'os': "android",
        'ab_version': VERSION_NAME,
        'ssmix': "a",
        'device_type': device_model,
        'device_brand': brand,
        'language': language,
        'os_api': str(os_api),
        'os_version': os_version,
        'openudid': openudid,
        'manifest_version_code': VERSION_CODE,
        'resolution': "720*1465",
        'dpi': "300",
        'update_version_code': VERSION_CODE,
        '_rticket': str(rticket + 69),
        'is_pad': "0",
        'current_region': "SA",
        'app_type': "normal",
        'sys_region': "AE",
        'last_install_time': str(ts - 10000),
        'timezone_name': "Asia/Riyadh",
        'residence': "SA",
        'app_language': language,
        'ac2': "wifi5g",
        'uoo': "0",
        'op_region': "SA",
        'timezone_offset': "10800",
        'build_number': VERSION_NAME,
        'host_abi': "arm64-v8a",
        'locale': language,
        'region': "AE",
        'ts': str(ts),
        'cdid': cdid,
        'support_webview': "1",
        'cronet_version': "f6248591_2024-09-11",
        'ttnet_version': "4.2.195.9-tiktok",
        'use_store_region_cookie': "1",
        "app_version": "28.6.5"
    }
    payload_data = {
        'code': code_encoded,
        'account_sdk_source': "app",
        'email_source': "1",
        'mix_mode': "1",
        'multi_login': "1",
        'type': "3d",
        'email': email_encoded
    }
    params_str = urllib.parse.urlencode(params)
    payload_str = urllib.parse.urlencode(payload_data)
    m = sign_email(params=params_str, payload=payload_str, cookie=None)
    headers = {
        'User-Agent': f"com.ss.android.tt.creator/370301 (Linux; U; Android {os_version}; {language}; {device_model}; Build/TP1A.220624.014; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",
        'x-tt-pba-enable': "1",
        'x-bd-kmsv': "0",
        'x-tt-dm-status': "login=1;ct=1;rt=8",
        'x-ss-req-ticket': str(rticket + 79),
        'sdk-version': "2",
        'tt-ticket-guard-iteration-version': "0",
        'tt-ticket-guard-version': "3",
        'passport-sdk-version': SDK_VERSION,
        'x-ss-stub': m['x-ss-stub'],
        'x-tt-store-region': "sa",
        'x-tt-store-region-src': "uid",
        'rpc-persist-pyxis-policy-v-tnc': "1",
        'x-ss-dp': str(AID),
        'x-tt-trace-id': generate_trace_id(),
        'x-tt-dataflow-id': "671088640",
        'x-argus': m['x-argus'],
        'x-gorgon': m['x-gorgon'],
        'x-khronos': m['x-khronos'],
        'x-ladon': m['x-ladon'],
        'Cookie': f"sessionid={session_id}"
    }
    response = requests.post(url, params=params, data=payload_data, headers=headers)
    return response


def safe_verify_phone(session_id: str, iid: str, device_id: str, openudid: str, cdid: str, device_model: str, brand: str, os_version: str, os_api: int, language: str) -> requests.Response:
    """التحقق الأمني قبل فك رقم الهاتف"""
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/shark/safe_verify/v2/"
    ts = now_sec()
    rticket = now_ms()
    
    params = {
        'iid': iid,
        'device_id': device_id,
        'ac': "WIFI",
        'channel': "googleplay",
        'aid': str(AID),
        'app_name': APP_NAME,
        'version_code': VERSION_CODE,
        'version_name': VERSION_NAME,
        'device_platform': "android",
        'os': "android",
        'ab_version': VERSION_NAME,
        'ssmix': "a",
        'device_type': device_model,
        'device_brand': brand,
        'language': language,
        'os_api': str(os_api),
        'os_version': os_version,
        'openudid': openudid,
        'manifest_version_code': VERSION_CODE,
        'resolution': "720*1504",
        'dpi': "320",
        'update_version_code': VERSION_CODE,
        '_rticket': str(rticket),
        'is_pad': "0",
        'current_region': "EG",
        'app_type': "normal",
        'sys_region': "EG",
        'last_install_time': str(ts - 10000),
        'mcc_mnc': "60202",
        'timezone_name': "Africa%2FCairo",
        'carrier_region_v2': "602",
        'residence': "EG",
        'app_language': language,
        'carrier_region': "EG",
        'ac2': "wifi",
        'uoo': "0",
        'op_region': "EG",
        'timezone_offset': "7200",
        'build_number': VERSION_NAME,
        'host_abi': "arm64-v8a",
        'locale': language,
        'region': "EG",
        'ts': str(ts),
        'cdid': cdid,
        'support_webview': "1",
        'cronet_version': "f6248591_2024-09-11",
        'ttnet_version': "4.2.195.9-tiktok",
        'use_store_region_cookie': "1",
        'app_version': VERSION_NAME
    }
    payload_data = {
        'product_scene': "31",
        'mix_mode': "1"
    }
    params_str = urllib.parse.urlencode(params)
    payload_str = urllib.parse.urlencode(payload_data)
    m = sign_number(params_str=params_str, payload_str=payload_str, cookie=f"sessionid={session_id}")
    headers = {
        'User-Agent': f"com.ss.android.tt.creator/370301 (Linux; U; Android {os_version}; {language}; {device_model}; Build/RP1A.201005.001; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",
        'x-tt-pba-enable': "1",
        'tt-ticket-guard-public-key': "BLvf2Dh6OP6Fgfjwkztn7WhreT5zaRhpS0qld8Um1R4KXrNVWp3W1rWQ5NDxvBIhXPcOtaCAE5FJaes7RaGovSA=",
        'tt-ticket-guard-iteration-version': "0",
        'x-bd-kmsv': "0",
        'x-tt-dm-status': "login=1;ct=1;rt=1",
        'x-ss-req-ticket': str(rticket + 13),
        'sdk-version': "2",
        'tt-ticket-guard-version': "3",
        'passport-sdk-settings': "x-tt-token",
        'passport-sdk-sign': "x-tt-token",
        'passport-sdk-version': SDK_VERSION,
        'x-vc-bdturing-sdk-version': "2.3.8.i18n",
        'x-tt-request-tag': "n=0;nr=011;bg=0",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'rpc-persist-pyxis-policy-v-tnc': "1",
        'x-ss-dp': str(AID),
        'x-tt-trace-id': generate_trace_id(),
        'x-tt-dataflow-id': "671088640",
        'x-argus': m['x-argus'],
        'x-gorgon': m['x-gorgon'],
        'x-khronos': m['x-khronos'],
        'x-ladon': m['x-ladon'],
        'x-ss-stub': m['x-ss-stub'],
        'content-length': m['content-length'],
        'Cookie': f"sessionid={session_id}"
    }
    response = requests.post(url, params=params, data=payload_data, headers=headers)
    return response


def unbind_phone(session_id: str, passport_ticket: str, iid: str, device_id: str, openudid: str, cdid: str, device_model: str, brand: str, os_version: str, os_api: int, language: str) -> requests.Response:
    """فك رقم الهاتف"""
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/mobile/unbind/"
    ts = now_sec()
    rticket = now_ms()
    
    params = {
        'passport_ticket': passport_ticket,
        'iid': iid,
        'device_id': device_id,
        'ac': "WIFI",
        'channel': "googleplay",
        'aid': str(AID),
        'app_name': APP_NAME,
        'version_code': VERSION_CODE,
        'version_name': VERSION_NAME,
        'device_platform': "android",
        'os': "android",
        'ab_version': VERSION_NAME,
        'ssmix': "a",
        'device_type': device_model,
        'device_brand': brand,
        'language': language,
        'os_api': str(os_api),
        'os_version': os_version,
        'openudid': openudid,
        'manifest_version_code': VERSION_CODE,
        'resolution': "720*1504",
        'dpi': "320",
        'update_version_code': VERSION_CODE,
        '_rticket': str(rticket + 8),
        'is_pad': "0",
        'current_region': "EG",
        'app_type': "normal",
        'sys_region': "EG",
        'last_install_time': str(ts - 10000),
        'mcc_mnc': "60202",
        'timezone_name': "Africa%2FCairo",
        'carrier_region_v2': "602",
        'residence': "EG",
        'app_language': language,
        'carrier_region': "EG",
        'ac2': "wifi",
        'uoo': "0",
        'op_region': "EG",
        'timezone_offset': "7200",
        'build_number': VERSION_NAME,
        'host_abi': "arm64-v8a",
        'locale': language,
        'region': "EG",
        'ts': str(ts),
        'cdid': cdid,
        'support_webview': "1",
        'cronet_version': "f6248591_2024-09-11",
        'ttnet_version': "4.2.195.9-tiktok",
        'use_store_region_cookie': "1",
        'app_version': VERSION_NAME
    }
    payload_str = "null"
    params_str = urllib.parse.urlencode(params)
    m = sign_number(params_str=params_str, payload_str=payload_str, cookie=f"sessionid={session_id}")
    headers = {
        'User-Agent': f"com.ss.android.tt.creator/370301 (Linux; U; Android {os_version}; {language}; {device_model}; Build/RP1A.201005.001; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",
        'x-tt-pba-enable': "1",
        'tt-ticket-guard-public-key': "BLvf2Dh6OP6Fgfjwkztn7WhreT5zaRhpS0qld8Um1R4KXrNVWp3W1rWQ5NDxvBIhXPcOtaCAE5FJaes7RaGovSA=",
        'tt-ticket-guard-iteration-version': "0",
        'x-bd-kmsv': "0",
        'x-tt-dm-status': "login=1;ct=1;rt=1",
        'x-ss-req-ticket': str(rticket + 16),
        'sdk-version': "2",
        'tt-ticket-guard-version': "3",
        'passport-sdk-settings': "x-tt-token",
        'passport-sdk-sign': "x-tt-token",
        'passport-sdk-version': SDK_VERSION,
        'x-vc-bdturing-sdk-version': "2.3.8.i18n",
        'x-tt-request-tag': "n=0;nr=011;bg=0",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'rpc-persist-pyxis-policy-v-tnc': "1",
        'x-ss-dp': str(AID),
        'x-tt-trace-id': generate_trace_id(),
        'x-tt-dataflow-id': "671088640",
        'x-argus': m['x-argus'],
        'x-gorgon': m['x-gorgon'],
        'x-khronos': m['x-khronos'],
        'x-ladon': m['x-ladon'],
        'x-ss-stub': m['x-ss-stub'],
        'content-length': m['content-length'],
        'Cookie': f"sessionid={session_id}"
    }
    response = requests.post(url, params=params, data="null", headers=headers)
    return response


def safe_verify_for_email_unbind(session_id: str, iid: str, device_id: str, openudid: str, cdid: str, device_model: str, brand: str, os_version: str, os_api: int, language: str) -> requests.Response:
    """التحقق الأمني قبل فك البريد الإلكتروني"""
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/shark/safe_verify/v2/"
    ts = now_sec()
    rticket = now_ms()
    
    params = {
        'iid': iid,
        'device_id': device_id,
        'ac': "WIFI",
        'channel': "googleplay",
        'aid': str(AID),
        'app_name': APP_NAME,
        'version_code': VERSION_CODE,
        'version_name': VERSION_NAME,
        'device_platform': "android",
        'os': "android",
        'ab_version': VERSION_NAME,
        'ssmix': "a",
        'device_type': device_model,
        'device_brand': brand,
        'language': language,
        'os_api': str(os_api),
        'os_version': os_version,
        'openudid': openudid,
        'manifest_version_code': VERSION_CODE,
        'resolution': "720*1504",
        'dpi': "320",
        'update_version_code': VERSION_CODE,
        '_rticket': str(rticket),
        'is_pad': "0",
        'current_region': "EG",
        'app_type': "normal",
        'sys_region': "EG",
        'last_install_time': str(ts - 10000),
        'mcc_mnc': "60202",
        'timezone_name': "Africa%2FCairo",
        'carrier_region_v2': "602",
        'residence': "EG",
        'app_language': language,
        'carrier_region': "EG",
        'ac2': "wifi",
        'uoo': "0",
        'op_region': "EG",
        'timezone_offset': "7200",
        'build_number': VERSION_NAME,
        'host_abi': "arm64-v8a",
        'locale': language,
        'region': "EG",
        'ts': str(ts),
        'cdid': cdid,
        'support_webview': "1",
        'cronet_version': "f6248591_2024-09-11",
        'ttnet_version': "4.2.195.9-tiktok",
        'use_store_region_cookie': "1",
        'app_version': VERSION_NAME
    }
    payload_data = {
        'product_scene': "37",
        'mix_mode': "1"
    }
    params_str = urllib.parse.urlencode(params)
    payload_str = urllib.parse.urlencode(payload_data)
    m = sign_number(params_str=params_str, payload_str=payload_str, cookie=f"sessionid={session_id}")
    headers = {
        'User-Agent': f"com.ss.android.tt.creator/370301 (Linux; U; Android {os_version}; {language}; {device_model}; Build/RP1A.201005.001; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",
        'x-tt-pba-enable': "1",
        'tt-ticket-guard-public-key': "BLvf2Dh6OP6Fgfjwkztn7WhreT5zaRhpS0qld8Um1R4KXrNVWp3W1rWQ5NDxvBIhXPcOtaCAE5FJaes7RaGovSA=",
        'tt-ticket-guard-iteration-version': "0",
        'x-bd-kmsv': "0",
        'x-tt-dm-status': "login=1;ct=1;rt=1",
        'x-ss-req-ticket': str(rticket + 13),
        'sdk-version': "2",
        'tt-ticket-guard-version': "3",
        'passport-sdk-settings': "x-tt-token",
        'passport-sdk-sign': "x-tt-token",
        'passport-sdk-version': SDK_VERSION,
        'x-vc-bdturing-sdk-version': "2.3.8.i18n",
        'x-tt-request-tag': "n=0;nr=0;bg=0",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'rpc-persist-pyxis-policy-v-tnc': "1",
        'x-ss-dp': str(AID),
        'x-tt-trace-id': generate_trace_id(),
        'x-tt-dataflow-id': "671088640",
        'x-argus': m['x-argus'],
        'x-gorgon': m['x-gorgon'],
        'x-khronos': m['x-khronos'],
        'x-ladon': m['x-ladon'],
        'x-ss-stub': m['x-ss-stub'],
        'content-length': m['content-length'],
        'Cookie': f"sessionid={session_id}"
    }
    response = requests.post(url, params=params, data=payload_data, headers=headers)
    return response


def unbind_email(session_id: str, passport_ticket: str, iid: str, device_id: str, openudid: str, cdid: str, device_model: str, brand: str, os_version: str, os_api: int, language: str) -> requests.Response:
    """فك البريد الإلكتروني"""
    url = "https://api16-normal-c-alisg.tiktokv.com/passport/email/unbind/"
    ts = now_sec()
    rticket = now_ms()
    
    params = {
        'passport_ticket': passport_ticket,
        'iid': iid,
        'device_id': device_id,
        'ac': "WIFI",
        'channel': "googleplay",
        'aid': str(AID),
        'app_name': APP_NAME,
        'version_code': VERSION_CODE,
        'version_name': VERSION_NAME,
        'device_platform': "android",
        'os': "android",
        'ab_version': VERSION_NAME,
        'ssmix': "a",
        'device_type': device_model,
        'device_brand': brand,
        'language': language,
        'os_api': str(os_api),
        'os_version': os_version,
        'openudid': openudid,
        'manifest_version_code': VERSION_CODE,
        'resolution': "720*1504",
        'dpi': "320",
        'update_version_code': VERSION_CODE,
        '_rticket': str(rticket),
        'is_pad': "0",
        'current_region': "EG",
        'app_type': "normal",
        'sys_region': "EG",
        'last_install_time': str(ts - 10000),
        'mcc_mnc': "60202",
        'timezone_name': "Africa/Cairo",
        'carrier_region_v2': "602",
        'residence': "EG",
        'app_language': language,
        'carrier_region': "EG",
        'ac2': "wifi",
        'uoo': "0",
        'op_region': "EG",
        'timezone_offset': "7200",
        'build_number': VERSION_NAME,
        'host_abi': "arm64-v8a",
        'locale': language,
        'region': "EG",
        'ts': str(ts),
        'cdid': cdid,
        'support_webview': "1",
        'cronet_version': "f6248591_2024-09-11",
        'ttnet_version': "4.2.195.9-tiktok",
        'use_store_region_cookie': "1",
        'app_version': VERSION_NAME
    }
    params_str = urllib.parse.urlencode(params)
    payload_str = "null"
    m = sign_number(params_str=params_str, payload_str=payload_str, cookie=f"sessionid={session_id}")
    headers = {
        'User-Agent': f"com.ss.android.tt.creator/370301 (Linux; U; Android {os_version}; {language}; {device_model}; Build/RP1A.201005.001; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",
        'x-tt-pba-enable': "1",
        'tt-ticket-guard-public-key': "BLvf2Dh6OP6Fgfjwkztn7WhreT5zaRhpS0qld8Um1R4KXrNVWp3W1rWQ5NDxvBIhXPcOtaCAE5FJaes7RaGovSA=",
        'tt-ticket-guard-iteration-version': "0",
        'x-bd-kmsv': "0",
        'x-tt-dm-status': "login=1;ct=1;rt=1",
        'x-ss-req-ticket': str(rticket + 12),
        'sdk-version': "2",
        'tt-ticket-guard-version': "3",
        'passport-sdk-settings': "x-tt-token",
        'passport-sdk-sign': "x-tt-token",
        'passport-sdk-version': SDK_VERSION,
        'x-vc-bdturing-sdk-version': "2.3.8.i18n",
        'x-tt-request-tag': "n=0;nr=0;bg=0",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'rpc-persist-pyxis-policy-v-tnc': "1",
        'x-ss-dp': str(AID),
        'x-tt-trace-id': generate_trace_id(),
        'x-tt-dataflow-id': "671088640",
        'x-argus': m['x-argus'],
        'x-gorgon': m['x-gorgon'],
        'x-khronos': m['x-khronos'],
        'x-ladon': m['x-ladon'],
        'x-ss-stub': m['x-ss-stub'],
        'content-length': m['content-length'],
        'Cookie': f"sessionid={session_id}"
    }
    response = requests.post(url, params=params, data="null", headers=headers)
    return response