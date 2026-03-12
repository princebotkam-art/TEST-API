#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ POWER MODZ OTP BOT - WITH ADMIN PANEL ⚡
Complete Solution with 4 Buttons + Full Control
"""

import requests
import time
import re
import random
from datetime import datetime
import json
import os
import sys
import threading

# Try importing telegram bot library
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ python-telegram-bot not installed!")
    print("💡 Install it: pip install python-telegram-bot")
    print()

# ==================== CONFIGURATION ====================
API_URL = "http://147.135.212.197/crapi/st/viewstats"
API_TOKEN = "R1BTQ0hBUzSAild8c2aWV3eYa1NpjVNIUpBzY1qCaWFHh5JUUpWIXQ=="
TELEGRAM_BOT_TOKEN = "8073903913:AAEzVlCNlr-fnjQfOukl3sBdwvnJqepjYAY"
TELEGRAM_CHANNEL_ID = "-1003868394296"
OWNER_ID = 7
CHECK_INTERVAL = 15        # ⏱️ Har 15 sec baad fetch (jaldi OTP mile)
BATCH_SIZE = 20            # 📦 Ek baar mein 20 records process
MAX_RECORDS_PER_FETCH = 1000000000

# ==================== SMART ANTI-BAN DELAYS ====================
# Telegram rules: channel/group ke liye 20 msg/min safe limit
# Is liye 1 msg har 3-4 sec = ~15-20 msg/min = SAFE zone
MSG_DELAY = 3.5            # ⏳ Har message ke baad 3.5 sec (safe & fast)
BATCH_DELAY = 8            # ⏳ Har batch ke baad 8 sec (pehle 15 tha - kam kiya)
RATE_LIMIT_DELAY = 30      # ⏳ Rate limit par 30 sec (same rahega)

# Smart delay: thoda random delay add karo takay pattern na bane
def smart_delay(base_delay):
    """Random +/- 1 sec add karo - Telegram spam detection se bachao"""
    jitter = random.uniform(-0.8, 1.2)
    actual = max(2.0, base_delay + jitter)
    time.sleep(actual)

processed_messages = set()

# ⚡ POWER MODZ - 4 BUTTONS ⚡
BUTTON_CONFIG = {
    "btn1": {"text": "☎️ NUMBERS", "url": "https://t.me/dp_numbers"},
    "btn2": {"text": "😈 DEVELOPER", "url": "https://t.me/powermodzzz"},
    "btn3": {"text": "📁 FOLDER", "url": "https://t.me/addlist/j1oWFpRCPE9mNmFk"},
    "btn4": {"text": "🟢 WhatsApp", "url": "https://whatsapp.com/channel/0029Vb6oQ4CIN9ip6RfTmT0c"}
}

# OTP sending control
otp_sending_enabled = True

# Global app reference
telegram_app = None

# ==================== COUNTRY MAPPING ====================
COUNTRY_DATA = {
    "1": {"flag": "🇺🇸", "name": "USA/Canada"},
    "52": {"flag": "🇲🇽", "name": "Mexico"},
    "54": {"flag": "🇦🇷", "name": "Argentina"},
    "55": {"flag": "🇧🇷", "name": "Brazil"},
    "56": {"flag": "🇨🇱", "name": "Chile"},
    "57": {"flag": "🇨🇴", "name": "Colombia"},
    "58": {"flag": "🇻🇪", "name": "Venezuela"},
    "51": {"flag": "🇵🇪", "name": "Peru"},
    "53": {"flag": "🇨🇺", "name": "Cuba"},
    "591": {"flag": "🇧🇴", "name": "Bolivia"},
    "593": {"flag": "🇪🇨", "name": "Ecuador"},
    "595": {"flag": "🇵🇾", "name": "Paraguay"},
    "598": {"flag": "🇺🇾", "name": "Uruguay"},
    "44": {"flag": "🇬🇧", "name": "United Kingdom"},
    "33": {"flag": "🇫🇷", "name": "France"},
    "49": {"flag": "🇩🇪", "name": "Germany"},
    "39": {"flag": "🇮🇹", "name": "Italy"},
    "34": {"flag": "🇪🇸", "name": "Spain"},
    "7": {"flag": "🇷🇺", "name": "Russia"},
    "48": {"flag": "🇵🇱", "name": "Poland"},
    "31": {"flag": "🇳🇱", "name": "Netherlands"},
    "32": {"flag": "🇧🇪", "name": "Belgium"},
    "41": {"flag": "🇨🇭", "name": "Switzerland"},
    "43": {"flag": "🇦🇹", "name": "Austria"},
    "45": {"flag": "🇩🇰", "name": "Denmark"},
    "46": {"flag": "🇸🇪", "name": "Sweden"},
    "47": {"flag": "🇳🇴", "name": "Norway"},
    "358": {"flag": "🇫🇮", "name": "Finland"},
    "30": {"flag": "🇬🇷", "name": "Greece"},
    "351": {"flag": "🇵🇹", "name": "Portugal"},
    "353": {"flag": "🇮🇪", "name": "Ireland"},
    "420": {"flag": "🇨🇿", "name": "Czech Republic"},
    "36": {"flag": "🇭🇺", "name": "Hungary"},
    "40": {"flag": "🇷🇴", "name": "Romania"},
    "380": {"flag": "🇺🇦", "name": "Ukraine"},
    "90": {"flag": "🇹🇷", "name": "Turkey"},
    "86": {"flag": "🇨🇳", "name": "China"},
    "91": {"flag": "🇮🇳", "name": "India"},
    "92": {"flag": "🇵🇰", "name": "Pakistan"},
    "81": {"flag": "🇯🇵", "name": "Japan"},
    "82": {"flag": "🇰🇷", "name": "South Korea"},
    "84": {"flag": "🇻🇳", "name": "Vietnam"},
    "66": {"flag": "🇹🇭", "name": "Thailand"},
    "62": {"flag": "🇮🇩", "name": "Indonesia"},
    "60": {"flag": "🇲🇾", "name": "Malaysia"},
    "63": {"flag": "🇵🇭", "name": "Philippines"},
    "65": {"flag": "🇸🇬", "name": "Singapore"},
    "880": {"flag": "🇧🇩", "name": "Bangladesh"},
    "94": {"flag": "🇱🇰", "name": "Sri Lanka"},
    "95": {"flag": "🇲🇲", "name": "Myanmar"},
    "855": {"flag": "🇰🇭", "name": "Cambodia"},
    "856": {"flag": "🇱🇦", "name": "Laos"},
    "93": {"flag": "🇦🇫", "name": "Afghanistan"},
    "98": {"flag": "🇮🇷", "name": "Iran"},
    "964": {"flag": "🇮🇶", "name": "Iraq"},
    "972": {"flag": "🇮🇱", "name": "Israel"},
    "966": {"flag": "🇸🇦", "name": "Saudi Arabia"},
    "971": {"flag": "🇦🇪", "name": "UAE"},
    "974": {"flag": "🇶🇦", "name": "Qatar"},
    "965": {"flag": "🇰🇼", "name": "Kuwait"},
    "968": {"flag": "🇴🇲", "name": "Oman"},
    "973": {"flag": "🇧🇭", "name": "Bahrain"},
    "962": {"flag": "🇯🇴", "name": "Jordan"},
    "961": {"flag": "🇱🇧", "name": "Lebanon"},
    "963": {"flag": "🇸🇾", "name": "Syria"},
    "967": {"flag": "🇾🇪", "name": "Yemen"},
    "996": {"flag": "🇰🇬", "name": "Kyrgyzstan"},
    "998": {"flag": "🇺🇿", "name": "Uzbekistan"},
    "992": {"flag": "🇹🇯", "name": "Tajikistan"},
    "993": {"flag": "🇹🇲", "name": "Turkmenistan"},
    "994": {"flag": "🇦🇿", "name": "Azerbaijan"},
    "995": {"flag": "🇬🇪", "name": "Georgia"},
    "374": {"flag": "🇦🇲", "name": "Armenia"},
    "977": {"flag": "🇳🇵", "name": "Nepal"},
    "20": {"flag": "🇪🇬", "name": "Egypt"},
    "27": {"flag": "🇿🇦", "name": "South Africa"},
    "234": {"flag": "🇳🇬", "name": "Nigeria"},
    "233": {"flag": "🇬🇭", "name": "Ghana"},
    "254": {"flag": "🇰🇪", "name": "Kenya"},
    "255": {"flag": "🇹🇿", "name": "Tanzania"},
    "256": {"flag": "🇺🇬", "name": "Uganda"},
    "251": {"flag": "🇪🇹", "name": "Ethiopia"},
    "212": {"flag": "🇲🇦", "name": "Morocco"},
    "213": {"flag": "🇩🇿", "name": "Algeria"},
    "216": {"flag": "🇹🇳", "name": "Tunisia"},
    "218": {"flag": "🇱🇾", "name": "Libya"},
    "221": {"flag": "🇸🇳", "name": "Senegal"},
    "225": {"flag": "🇨🇮", "name": "Ivory Coast"},
    "237": {"flag": "🇨🇲", "name": "Cameroon"},
    "243": {"flag": "🇨🇩", "name": "DR Congo"},
    "244": {"flag": "🇦🇴", "name": "Angola"},
    "258": {"flag": "🇲🇿", "name": "Mozambique"},
    "260": {"flag": "🇿🇲", "name": "Zambia"},
    "263": {"flag": "🇿🇼", "name": "Zimbabwe"},
    "61": {"flag": "🇦🇺", "name": "Australia"},
    "64": {"flag": "🇳🇿", "name": "New Zealand"},
    "679": {"flag": "🇫🇯", "name": "Fiji"},
}

SERVICE_NAMES = {
    "whatsapp": "WhatsApp", "facebook": "Facebook", "instagram": "Instagram",
    "snapchat": "Snapchat", "twitter": "Twitter", "tiktok": "TikTok",
    "telegram": "Telegram", "linkedin": "LinkedIn", "discord": "Discord",
    "viber": "Viber", "wechat": "WeChat", "line": "LINE", "kakaotalk": "KakaoTalk",
    "google": "Google", "microsoft": "Microsoft", "apple": "Apple",
    "yahoo": "Yahoo", "amazon": "Amazon", "uber": "Uber", "netflix": "Netflix",
    "paypal": "PayPal", "grab": "Grab", "gojek": "GoJek", "olx": "OLX",
    "steam": "Steam", "roblox": "Roblox", "naver": "Naver",
    "verify": "Verification Service", "otp": "OTP Service",
}

def get_country_info(phone_number):
    phone_str = str(phone_number).strip()
    for code in ["880", "420", "855", "856", "591", "593", "595", "598", "358", "351", "353", "380", "374", "234", "233", "254", "255", "256", "251", "212", "213", "216", "218", "221", "225", "237", "243", "244", "258", "260", "263", "961", "962", "963", "964", "965", "966", "967", "968", "971", "972", "973", "974", "992", "993", "994", "995", "996", "998", "977", "679"]:
        if phone_str.startswith(code):
            return COUNTRY_DATA[code]["flag"], COUNTRY_DATA[code]["name"]
    prefix = phone_str[:2]
    if prefix in COUNTRY_DATA:
        return COUNTRY_DATA[prefix]["flag"], COUNTRY_DATA[prefix]["name"]
    prefix = phone_str[:1]
    if prefix in COUNTRY_DATA:
        return COUNTRY_DATA[prefix]["flag"], COUNTRY_DATA[prefix]["name"]
    return "🌍", "Unknown"

def get_service_name(cli):
    if not cli:
        return "Unknown Service"
    cli_lower = str(cli).lower().strip()
    for key, value in SERVICE_NAMES.items():
        if key in cli_lower:
            return value
    return str(cli).title()

def extract_otp(message):
    """Extract OTP code"""
    if not message:
        return "N/A"
    
    message_str = str(message)
    
    # PRIORITY 1: 6-digit numeric OTP
    match = re.search(r'\b(\d{6})\b', message_str)
    if match:
        return match.group(1)
    
    # PRIORITY 2: Formats like 101-390, 123-456
    match = re.search(r'(\d{3}-\d{3})', message_str)
    if match:
        return match.group(1)
    
    # PRIORITY 3: 4-5 digit codes
    match = re.search(r'\b(\d{4,5})\b', message_str)
    if match:
        return match.group(1)
    
    return "N/A"

def mask_phone_number(phone):
    phone_str = str(phone)
    if len(phone_str) <= 4:
        return phone_str
    return f"{phone_str[:4]}****{phone_str[-3:]}"

def format_telegram_message(data):
    if isinstance(data, dict):
        dt = data.get('dt', '')
        num = data.get('num', '')
        cli = data.get('cli', 'Unknown')
        message = data.get('message', '')
    elif isinstance(data, list) and len(data) >= 4:
        cli = str(data[0]) if len(data) > 0 else 'Unknown'
        num = str(data[1]) if len(data) > 1 else ''
        message = str(data[2]) if len(data) > 2 else ''
        dt = str(data[3]) if len(data) > 3 else ''
    else:
        return None, "N/A"
    
    if not num or not message:
        return None, "N/A"
    
    message = message.strip().replace('\\n', '\n')
    
    flag, country = get_country_info(num)
    service = get_service_name(cli)
    otp = extract_otp(message)
    masked_num = mask_phone_number(num)
    
    # ⚡ POWER MODZ FORMAT ⚡
    telegram_msg = f"""<b>✨𝐍𝐄𝐖 𝐎𝐓𝐏 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃✨</b>
━━━━━━━━━━━━━━━━
<blockquote>🕐 <b>Time:</b> <code>{dt}</code></blockquote>
<blockquote>{flag} <b>Country:</b> <i>{country}</i></blockquote>
<blockquote>🟢 <b>Service:</b> <i>{service}</i></blockquote>
<blockquote>📞 <b>Number:</b> <code>+{masked_num}</code></blockquote>
<blockquote>🔑 <b>OTP:</b> <code>{otp}</code></blockquote>
<blockquote>📧 <b>Full Message:</b></blockquote>
<pre>{message}</pre>
<b>𝐏𝐎𝐖𝐄𝐑 𝐌𝐎𝐃𝐙 𝐊𝐈𝐍𝐆</b>
━━━━━━━━━━━━━━━━━"""
    
    return telegram_msg, otp

def send_telegram_message(message, otp_code):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # ⚡ POWER MODZ - 4 BUTTONS IN 2x2 GRID ⚡
    keyboard = {
        "inline_keyboard": [
            [
                {"text": BUTTON_CONFIG['btn1']['text'], "url": BUTTON_CONFIG['btn1']['url']},
                {"text": BUTTON_CONFIG['btn2']['text'], "url": BUTTON_CONFIG['btn2']['url']}
            ],
            [
                {"text": BUTTON_CONFIG['btn3']['text'], "url": BUTTON_CONFIG['btn3']['url']},
                {"text": BUTTON_CONFIG['btn4']['text'], "url": BUTTON_CONFIG['btn4']['url']}
            ]
        ]
    }
    
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(keyboard)
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return True
            elif response.status_code == 429:
                retry_after = int(response.json().get('parameters', {}).get('retry_after', RATE_LIMIT_DELAY))
                print(f"🚫 Rate limited! Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            else:
                if attempt < max_retries - 1:
                    time.sleep(2)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
    return False

def fetch_api_data():
    params = {"token": API_TOKEN, "records": MAX_RECORDS_PER_FETCH}
    try:
        print(f"📡 Fetching data from API...")
        response = requests.get(API_URL, params=params, timeout=60)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"✅ Fetched {len(data)} records")
                return data
            elif isinstance(data, dict):
                if data.get('status') == 'success':
                    records = data.get('data', [])
                    print(f"✅ Fetched {len(records)} records")
                    return records
                else:
                    print(f"⚠️ API Error: {data.get('msg', 'Unknown')}")
                    return []
            else:
                return []
        else:
            print(f"⚠️ HTTP Error: {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        print(f"⚠️ API timeout")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def create_message_id(data):
    if isinstance(data, dict):
        dt = data.get('dt', '')
        num = data.get('num', '')
        cli = data.get('cli', '')
        message = data.get('message', '')[:50]
    elif isinstance(data, list) and len(data) >= 4:
        cli = str(data[0]) if len(data) > 0 else ''
        num = str(data[1]) if len(data) > 1 else ''
        message = (str(data[2]) if len(data) > 2 else '')[:50]
        dt = str(data[3]) if len(data) > 3 else ''
    else:
        return str(data)[:100]
    return f"{dt}_{num}_{cli}_{message}"

def process_records_in_batches(records):
    total_records = len(records)
    new_count = 0
    duplicate_count = 0
    error_count = 0
    print(f"📦 Processing {total_records} records in batches of {BATCH_SIZE}...")
    for i in range(0, total_records, BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (total_records + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"🔄 Batch {batch_num}/{total_batches} ({len(batch)} records)...")
        for record in batch:
            try:
                if not record or (isinstance(record, list) and len(record) < 4):
                    error_count += 1
                    continue
                msg_id = create_message_id(record)
                if msg_id not in processed_messages:
                    result = format_telegram_message(record)
                    if result[0] is None:
                        error_count += 1
                        continue
                    telegram_msg, otp = result
                    if send_telegram_message(telegram_msg, otp):
                        processed_messages.add(msg_id)
                        new_count += 1
                        print(f"  ✅ Sent OTP: {otp} ({new_count})")
                    else:
                        error_count += 1
                    if len(processed_messages) > 5000:
                        oldest_entries = list(processed_messages)[:1000]
                        for entry in oldest_entries:
                            processed_messages.discard(entry)
                    # ✅ SMART ANTI-BAN: Random jitter delay (spam pattern se bachao)
                    print(f"  ⏳ Smart delay ~{MSG_DELAY}s...")
                    smart_delay(MSG_DELAY)
                else:
                    duplicate_count += 1
            except Exception as e:
                error_count += 1
                print(f"  ❌ Error: {e}")
        if i + BATCH_SIZE < total_records:
            # ✅ SMART ANTI-BAN: Batch ke baad random delay
            print(f"⏳ Batch done. Smart anti-ban wait ~{BATCH_DELAY}s...")
            smart_delay(BATCH_DELAY)
    return new_count, duplicate_count, error_count

def health_check():
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Bot connected: @{bot_info['result']['username']}")
            return True
        return False
    except:
        return False

def otp_checker_thread():
    """Background thread for OTP checking"""
    print("🔍 OTP Checker Thread Started!")
    time.sleep(3)
    
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    while True:
        try:
            if not otp_sending_enabled:
                print("⏸️ OTP sending is DISABLED")
                time.sleep(CHECK_INTERVAL)
                continue
            
            print(f"\n{'='*70}")
            print(f"🔍 Fetch cycle: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*70}\n")
            
            records = fetch_api_data()
            
            if records:
                new_count, duplicate_count, error_count = process_records_in_batches(records)
                print(f"\n{'='*70}")
                print(f"📊 SUMMARY:")
                print(f"  📥 Total fetched: {len(records)}")
                print(f"  ✨ New sent: {new_count}")
                print(f"  ⏭️  Duplicates: {duplicate_count}")
                print(f"  ❌ Errors: {error_count}")
                print(f"{'='*70}\n")
                consecutive_errors = 0
            else:
                print("📭 No records\n")
                consecutive_errors += 1
            
            if consecutive_errors >= max_consecutive_errors:
                print(f"⚠️ Too many errors. Taking longer break...")
                time.sleep(CHECK_INTERVAL * 5)
                consecutive_errors = 0
            else:
                print(f"⏳ Waiting {CHECK_INTERVAL} seconds...\n")
                time.sleep(CHECK_INTERVAL)
                
        except Exception as e:
            consecutive_errors += 1
            print(f"❌ Error in checker thread: {e}")
            time.sleep(CHECK_INTERVAL)

# ==================== ADMIN PANEL HANDLERS ====================
if TELEGRAM_AVAILABLE:
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Admin panel - /start command"""
        user_id = update.effective_user.id
        
        if user_id != OWNER_ID:
            await update.message.reply_text("⛔ Unauthorized! You are not the bot owner.")
            return
        
        keyboard = [
            [InlineKeyboardButton("📨 Manage OTPs", callback_data="manage_otps")],
            [InlineKeyboardButton("🔘 Manage Buttons", callback_data="manage_buttons")],
            [InlineKeyboardButton("👑 Owner Panel", callback_data="owner_panel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚡ *POWER MODZ OTP BOT* ⚡\n\n"
            "Welcome to the Admin Panel!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle admin panel button clicks"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        if user_id != OWNER_ID:
            await query.edit_message_text("⛔ Unauthorized!")
            return
        
        if query.data == "manage_otps":
            global otp_sending_enabled
            status = "✅ Enabled" if otp_sending_enabled else "❌ Disabled"
            keyboard = [
                [InlineKeyboardButton("✅ Enable OTP", callback_data="enable_otp")],
                [InlineKeyboardButton("❌ Disable OTP", callback_data="disable_otp")],
                [InlineKeyboardButton("📊 Check Status", callback_data="check_status")],
                [InlineKeyboardButton("« Back", callback_data="back_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"📨 *OTP Management*\n\n"
                f"Current Status: {status}\n"
                f"Processed: {len(processed_messages)} messages",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif query.data == "enable_otp":
            otp_sending_enabled = True
            keyboard = [
                [InlineKeyboardButton("✅ Enable OTP", callback_data="enable_otp")],
                [InlineKeyboardButton("❌ Disable OTP", callback_data="disable_otp")],
                [InlineKeyboardButton("📊 Check Status", callback_data="check_status")],
                [InlineKeyboardButton("« Back", callback_data="back_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"✅ *OTP Sending ENABLED!*\n\n"
                f"Bot will now send OTPs to channel\n"
                f"Processed: {len(processed_messages)} messages",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif query.data == "disable_otp":
            otp_sending_enabled = False
            keyboard = [
                [InlineKeyboardButton("✅ Enable OTP", callback_data="enable_otp")],
                [InlineKeyboardButton("❌ Disable OTP", callback_data="disable_otp")],
                [InlineKeyboardButton("📊 Check Status", callback_data="check_status")],
                [InlineKeyboardButton("« Back", callback_data="back_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"❌ *OTP Sending DISABLED!*\n\n"
                f"Bot will NOT send OTPs\n"
                f"Processed: {len(processed_messages)} messages",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif query.data == "check_status":
            status = "✅ Enabled" if otp_sending_enabled else "❌ Disabled"
            keyboard = [
                [InlineKeyboardButton("✅ Enable OTP", callback_data="enable_otp")],
                [InlineKeyboardButton("❌ Disable OTP", callback_data="disable_otp")],
                [InlineKeyboardButton("📊 Check Status", callback_data="check_status")],
                [InlineKeyboardButton("« Back", callback_data="back_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"📊 *Current Status*\n\n"
                f"OTP Sending: {status}\n"
                f"Processed: {len(processed_messages)} messages\n"
                f"Check Interval: {CHECK_INTERVAL}s\n"
                f"Batch Size: {BATCH_SIZE}",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif query.data == "manage_buttons":
            keyboard = [
                [InlineKeyboardButton("Edit Button 1", callback_data="edit_btn1")],
                [InlineKeyboardButton("Edit Button 2", callback_data="edit_btn2")],
                [InlineKeyboardButton("Edit Button 3", callback_data="edit_btn3")],
                [InlineKeyboardButton("Edit Button 4", callback_data="edit_btn4")],
                [InlineKeyboardButton("« Back", callback_data="back_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            buttons_info = f"""🔘 *Current Buttons*

1️⃣ {BUTTON_CONFIG['btn1']['text']}
   `{BUTTON_CONFIG['btn1']['url']}`

2️⃣ {BUTTON_CONFIG['btn2']['text']}
   `{BUTTON_CONFIG['btn2']['url']}`

3️⃣ {BUTTON_CONFIG['btn3']['text']}
   `{BUTTON_CONFIG['btn3']['url']}`

4️⃣ {BUTTON_CONFIG['btn4']['text']}
   `{BUTTON_CONFIG['btn4']['url']}`

Click a button below to edit it."""
            
            await query.edit_message_text(buttons_info, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif query.data.startswith("edit_btn"):
            btn_num = query.data[-1]
            context.user_data['editing_button'] = btn_num
            context.user_data['edit_step'] = 'text'
            current_text = BUTTON_CONFIG[f'btn{btn_num}']['text']
            current_url = BUTTON_CONFIG[f'btn{btn_num}']['url']
            
            await query.edit_message_text(
                f"✏️ *Editing Button {btn_num}*\n\n"
                f"📝 Current Text: `{current_text}`\n"
                f"🔗 Current URL: `{current_url}`\n\n"
                f"Send the *NEW button text*:",
                parse_mode='Markdown'
            )
        
        elif query.data == "owner_panel":
            keyboard = [
                [InlineKeyboardButton("📊 Statistics", callback_data="stats")],
                [InlineKeyboardButton("🔄 Refresh", callback_data="owner_panel")],
                [InlineKeyboardButton("« Back", callback_data="back_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            panel_info = f"""👑 *Owner Control Panel*

🟢 Status: Running
📡 API: Connected
📢 Channel: `{TELEGRAM_CHANNEL_ID}`
👤 Owner: `{OWNER_ID}`
📨 OTP Sending: {"✅ Enabled" if otp_sending_enabled else "❌ Disabled"}
⏱️ Check Interval: {CHECK_INTERVAL}s
📦 Batch Size: {BATCH_SIZE}
💾 Processed: {len(processed_messages)}"""
            
            await query.edit_message_text(panel_info, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif query.data == "stats":
            keyboard = [
                [InlineKeyboardButton("🔄 Refresh Stats", callback_data="stats")],
                [InlineKeyboardButton("« Back", callback_data="owner_panel")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            stats_msg = f"""📊 *Bot Statistics*

📨 Total Processed: {len(processed_messages)}
📮 OTP Status: {"✅ Enabled" if otp_sending_enabled else "❌ Disabled"}
⏱️ Check Interval: {CHECK_INTERVAL} seconds
📦 Batch Size: {BATCH_SIZE}
📡 API Status: Connected
🔄 Bot: Running"""
            
            await query.edit_message_text(stats_msg, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif query.data == "back_main":
            keyboard = [
                [InlineKeyboardButton("📨 Manage OTPs", callback_data="manage_otps")],
                [InlineKeyboardButton("🔘 Manage Buttons", callback_data="manage_buttons")],
                [InlineKeyboardButton("👑 Owner Panel", callback_data="owner_panel")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            status_text = "✅ Enabled" if otp_sending_enabled else "❌ Disabled"
            await query.edit_message_text(
                f"⚡ *POWER MODZ OTP BOT* ⚡\n\n"
                f"Welcome to the Admin Panel!\n\n"
                f"OTP Status: {status_text}",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )

    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages for button editing"""
        user_id = update.effective_user.id
        if user_id != OWNER_ID:
            return
        
        if 'editing_button' in context.user_data:
            btn_num = context.user_data['editing_button']
            btn_key = f"btn{btn_num}"
            
            if context.user_data.get('edit_step') == 'text':
                BUTTON_CONFIG[btn_key]['text'] = update.message.text
                context.user_data['edit_step'] = 'url'
                await update.message.reply_text(
                    f"✅ Button text saved!\n\n"
                    f"Now send the *NEW URL* for button {btn_num}:",
                    parse_mode='Markdown'
                )
            
            elif context.user_data.get('edit_step') == 'url':
                BUTTON_CONFIG[btn_key]['url'] = update.message.text
                await update.message.reply_text(
                    f"✅ *Button {btn_num} updated!*\n\n"
                    f"📝 Text: {BUTTON_CONFIG[btn_key]['text']}\n"
                    f"🔗 URL: `{BUTTON_CONFIG[btn_key]['url']}`",
                    parse_mode='Markdown'
                )
                del context.user_data['editing_button']
                del context.user_data['edit_step']

def main():
    print("=" * 70)
    print("⚡ POWER MODZ OTP BOT - WITH ADMIN PANEL ⚡")
    print("=" * 70)
    print(f"📡 API URL: {API_URL}")
    print(f"📢 Channel ID: {TELEGRAM_CHANNEL_ID}")
    print(f"👑 Owner ID: {OWNER_ID}")
    print(f"⏱️  Check Interval: {CHECK_INTERVAL} seconds")
    print(f"📦 Batch Size: {BATCH_SIZE}")
    print(f"🔘 4 Buttons: Enabled")
    print("=" * 70)
    
    if health_check():
        print("✅ Telegram verified!")
    print()
    
    if not TELEGRAM_AVAILABLE:
        print("⚠️ Admin panel disabled (python-telegram-bot not installed)")
        print("💡 Install: pip install python-telegram-bot")
        print()
        # Run without admin panel
        consecutive_errors = 0
        max_consecutive_errors = 5
        while True:
            try:
                print(f"\n{'='*70}")
                print(f"🔍 Fetch cycle: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*70}\n")
                records = fetch_api_data()
                if records:
                    new_count, duplicate_count, error_count = process_records_in_batches(records)
                    print(f"\n{'='*70}")
                    print(f"📊 SUMMARY:")
                    print(f"  📥 Total: {len(records)}")
                    print(f"  ✨ New: {new_count}")
                    print(f"  ⏭️  Duplicates: {duplicate_count}")
                    print(f"  ❌ Errors: {error_count}")
                    print(f"{'='*70}\n")
                    consecutive_errors = 0
                else:
                    print("📭 No records\n")
                    consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    print(f"⚠️ Too many errors. Longer break...")
                    time.sleep(CHECK_INTERVAL * 5)
                    consecutive_errors = 0
                else:
                    print(f"⏳ Waiting {CHECK_INTERVAL} seconds...\n")
                    time.sleep(CHECK_INTERVAL)
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped")
                break
            except Exception as e:
                consecutive_errors += 1
                print(f"❌ Error: {e}")
                time.sleep(CHECK_INTERVAL)
    else:
        # Start OTP checker in background thread
        print("🔍 Starting OTP checker thread...")
        checker = threading.Thread(target=otp_checker_thread, daemon=True)
        checker.start()
        
        # Create Telegram bot application for admin panel
        global telegram_app
        print("🤖 Creating admin panel...")
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        telegram_app = app
        
        # Add admin panel handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        print("✅ Admin Panel is ready!")
        print("💡 Send /start to the bot to access control panel")
        print("=" * 70)
        print()
        
        # Start polling for admin commands
        try:
            app.run_polling(allowed_updates=Update.ALL_TYPES)
        except KeyboardInterrupt:
            print("\n" + "=" * 70)
            print("🛑 Bot stopped by user")
            print("=" * 70)

if __name__ == "__main__":
    main()
