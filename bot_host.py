# -*- coding: utf-8 -*-
"""
XENOVA PRO — Auto-Install + Auto-Run Bot Host
Upload .py → Auto-detect imports → Auto-install → Auto-run
Python 3.10+ | Async | pyTelegramBotAPI
"""
from __future__ import annotations

import asyncio
import ast
import json
import os
import re
import shutil
import signal
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import aiofiles
from telebot.async_telebot import AsyncTeleBot
from telebot import types

# ═══════════════════════════════════════════════════════
# 【 CONFIG 】
# ═══════════════════════════════════════════════════════

BOT_TOKEN = "8835613027:AAFovsLhrmH3H6f1Sv6UyQIAXsYlH0qP-eo"
ADMIN_IDS = ["8778069153"]
ADMIN_CHANNEL = "@myanmarmovie2780"
SUPPORT_CONTACT = "@BumHkrang55"
GITHUB_LINK = "https://github.com/"

BASE_DIR = Path("./host_data").resolve()
BOTS_DIR = BASE_DIR / "bots"
USERS_FILE = BASE_DIR / "users.json"
KEYS_FILE = BASE_DIR / "keys.json"
LOGS_DIR = BASE_DIR / "logs"

BASE_DIR.mkdir(exist_ok=True)
BOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

MAX_BOTS_PER_USER = 3
MAX_BOTS_PREMIUM = 10
FREE_RUNTIME_HOURS = 24
MAX_FILE_SIZE_MB = 5

# ═══════════════════════════════════════════════════════
# ⭐ IMPORT → PIP PACKAGE MAPPING
# ═══════════════════════════════════════════════════════

IMPORT_TO_PIP = {
    # Telegram
    "telebot": "pyTelegramBotAPI",
    "telebot.async_telebot": "pyTelegramBotAPI",
    "pyrogram": "pyrogram",
    "telethon": "telethon",
    "aiogram": "aiogram",

    # HTTP
    "aiohttp": "aiohttp",
    "requests": "requests",
    "httpx": "httpx",
    "urllib3": "urllib3",

    # Files
    "aiofiles": "aiofiles",
    "dotenv": "python-dotenv",

    # Images / Vision
    "cv2": "opencv-python-headless",
    "PIL": "Pillow",
    "numpy": "numpy",
    "ddddocr": "ddddocr",
    "pytesseract": "pytesseract",

    # Crypto / Auth
    "jwt": "PyJWT",
    "cryptography": "cryptography",
    "bcrypt": "bcrypt",
    "passlib": "passlib",

    # Parsing
    "bs4": "beautifulsoup4",
    "lxml": "lxml",
    "html5lib": "html5lib",
    "yaml": "PyYAML",
    "toml": "toml",

    # DB
    "pymongo": "pymongo",
    "motor": "motor",
    "redis": "redis",
    "asyncpg": "asyncpg",
    "psycopg2": "psycopg2-binary",
    "MySQLdb": "mysqlclient",
    "sqlalchemy": "SQLAlchemy",

    # Others
    "psutil": "psutil",
    "socketio": "python-socketio",
    "websockets": "websockets",
    "flask": "Flask",
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "pydantic": "pydantic",
    "dateutil": "python-dateutil",
    "pytz": "pytz",
    "emoji": "emoji",
    "tabulate": "tabulate",
    "colorama": "colorama",
    "tqdm": "tqdm",
    "faker": "Faker",
    "qrcode": "qrcode",
    "pyzbar": "pyzbar",
    "barcode": "python-barcode",
    "cloudscraper": "cloudscraper",
    "curl_cffi": "curl_cffi",
    "playwright": "playwright",
    "selenium": "selenium",
    "nested_dict": "nested-dict",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "openpyxl": "openpyxl",
    "xlsxwriter": "XlsxWriter",
    "pyrogram": "pyrogram",
    "tgcrypto": "tgcrypto",
    "uvloop": "uvloop",
    "orjson": "orjson",
    "ujson": "ujson",
    "nanoid": "nanoid",
    "babel": "Babel",
    "user_agent": "user-agents",
}

# Standard library modules (pip မလိုတဲ့ module တွေ)
STDLIB_MODULES = {
    "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore",
    "atexit", "audioop", "base64", "bdb", "binascii", "binhex", "bisect", "builtins",
    "bz2", "calendar", "cgi", "cgitb", "chunk", "cmath", "cmd", "code", "codecs",
    "codeop", "collections", "colorsys", "compileall", "concurrent", "configparser",
    "contextlib", "contextvars", "copy", "copyreg", "cProfile", "crypt", "csv",
    "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal", "difflib",
    "dis", "distutils", "doctest", "email", "encodings", "ensurepip", "enum",
    "errno", "faulthandler", "fcntl", "filecmp", "fileinput", "fnmatch", "formatter",
    "fractions", "ftplib", "functools", "gc", "getopt", "getpass", "gettext",
    "glob", "graphlib", "gzip", "hashlib", "heapq", "hmac", "html", "http",
    "idlelib", "imaplib", "imghdr", "imp", "importlib", "inspect", "io", "ipaddress",
    "itertools", "json", "keyword", "lib2to3", "linecache", "locale", "logging",
    "lzma", "mailbox", "mailcap", "marshal", "math", "mimetypes", "mmap", "modulefinder",
    "multiprocessing", "netrc", "nis", "nntplib", "numbers", "operator", "optparse",
    "os", "ossaudiodev", "parser", "pathlib", "pdb", "pickle", "pickletools", "pipes",
    "pkgutil", "platform", "plistlib", "poplib", "posix", "pprint", "profile",
    "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc", "queue", "quopri",
    "random", "re", "readline", "reprlib", "resource", "rlcompleter", "runpy",
    "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal",
    "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd", "sqlite3",
    "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess",
    "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile",
    "telnetlib", "tempfile", "termios", "test", "textwrap", "threading", "time",
    "timeit", "tkinter", "token", "tokenize", "trace", "traceback", "tracemalloc",
    "tty", "turtle", "turtledemo", "types", "typing", "unicodedata", "unittest",
    "urllib", "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser",
    "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile",
    "zipimport", "zlib", "zoneinfo",
}

# ═══════════════════════════════════════════════════════
# 【 GLOBALS 】
# ═══════════════════════════════════════════════════════

bot = AsyncTeleBot(BOT_TOKEN, parse_mode="Markdown")

running_bots: dict[str, dict[str, Any]] = {}
user_states: dict[int, dict[str, Any]] = {}
users_data: dict[str, dict] = {}
keys_data: dict[str, dict] = {}

_lock = asyncio.Lock()
START_TIME = time.monotonic()

# ═══════════════════════════════════════════════════════
# 【 FILE I/O 】
# ═══════════════════════════════════════════════════════

async def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default.copy()
    try:
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            return json.loads(await f.read())
    except Exception:
        return default.copy()


async def save_json(path: Path, data: dict) -> None:
    async with _lock:
        try:
            async with aiofiles.open(path, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, indent=2, default=str))
        except Exception as e:
            print(f"[save] {path}: {e}")


async def load_all() -> None:
    global users_data, keys_data
    users_data = await load_json(USERS_FILE, {})
    keys_data = await load_json(KEYS_FILE, {})


async def save_users() -> None:
    await save_json(USERS_FILE, users_data)


async def save_keys() -> None:
    await save_json(KEYS_FILE, keys_data)


# ═══════════════════════════════════════════════════════
# ⭐ AUTO-DETECT IMPORTS
# ═══════════════════════════════════════════════════════

def detect_imports_from_code(code: str) -> set[str]:
    """Python code ထဲက import တွေ အားလုံး ဆွဲထုတ်"""
    imports: set[str] = set()
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    imports.add(top)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    imports.add(top)
    except SyntaxError as e:
        print(f"[detect] SyntaxError: {e}")
    except Exception as e:
        print(f"[detect] error: {e}")
    return imports


def imports_to_pip_packages(imports: set[str]) -> list[str]:
    """import တွေကို pip package နာမည် ပြောင်း"""
    packages: list[str] = []
    for imp in imports:
        if imp in STDLIB_MODULES:
            continue
        if imp.startswith("_"):
            continue
        # Mapping ရှား
        pip_name = IMPORT_TO_PIP.get(imp)
        if pip_name:
            packages.append(pip_name)
        else:
            # Unknown — import name ကို ပဲ သုံး
            # (pip package name = import name ဖြစ်တာ ၈၀% ရှိ)
            packages.append(imp)
    return list(set(packages))


def parse_requirements_txt(content: str) -> list[str]:
    """requirements.txt ဖတ်"""
    packages: list[str] = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # version specifier ဖျက်
        pkg = re.split(r"[<>=!~\[\s]", line, 1)[0].strip()
        if pkg:
            packages.append(pkg)
    return packages


async def install_packages(
    packages: list[str],
    log_file: Path,
    chat_id: Optional[int] = None,
    bot_name: str = "",
) -> tuple[bool, str]:
    """pip install packages"""
    if not packages:
        return True, "No packages to install"

    await write_log_line(log_file, f"📦 Installing {len(packages)} packages...")
    await write_log_line(log_file, f"   {', '.join(packages)}")

    if chat_id:
        try:
            await bot.send_message(
                chat_id,
                f"📦 *Auto-Installing* `{bot_name}`\n\n"
                f"```\n" + "\n".join(packages[:15]) + "\n```"
                + (f"\n... +{len(packages) - 15} more" if len(packages) > 15 else ""),
            )
        except Exception:
            pass

    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "pip", "install", "--quiet",
            *packages,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        output_lines: list[str] = []
        try:
            while True:
                line = await asyncio.wait_for(proc.stdout.readline(), timeout=600)
                if not line:
                    break
                text = line.decode("utf-8", errors="ignore").rstrip()
                if text:
                    output_lines.append(text)
                    await write_log_line(log_file, f"  pip: {text[:300]}")
        except asyncio.TimeoutError:
            await write_log_line(log_file, "⚠️ pip install timeout")
            proc.kill()
            return False, "pip install timeout"

        await proc.wait()

        if proc.returncode == 0:
            await write_log_line(log_file, "✅ Packages installed")
            return True, "OK"
        else:
            tail = "\n".join(output_lines[-10:])
            await write_log_line(log_file, f"⚠️ pip failed (code={proc.returncode})")
            return False, tail or "pip install failed"

    except Exception as e:
        await write_log_line(log_file, f"⚠️ pip error: {e}")
        return False, str(e)


async def auto_install_for_bot(
    user_id: int, bot_name: str, chat_id: Optional[int] = None
) -> tuple[bool, str]:
    """Bot ရဲ့ import တွေ auto-detect ပြီး install"""
    bot_dir = user_bot_dir(user_id, bot_name)
    py_file = bot_dir / f"{bot_name}.py"
    log_file = LOGS_DIR / f"{bot_key(user_id, bot_name)}.log"

    if not py_file.exists():
        return False, "File not found"

    # 1. Code ထဲက import တွေ ဖတ်
    try:
        async with aiofiles.open(py_file, "r", encoding="utf-8", errors="ignore") as f:
            code = await f.read()
    except Exception as e:
        return False, f"Read error: {e}"

    imports = detect_imports_from_code(code)
    packages_from_code = imports_to_pip_packages(imports)

    # 2. requirements.txt ရှိရင် ဖတ်
    packages_from_req: list[str] = []
    req_file = bot_dir / "requirements.txt"
    if req_file.exists():
        try:
            async with aiofiles.open(req_file, "r", encoding="utf-8", errors="ignore") as f:
                req_content = await f.read()
            packages_from_req = parse_requirements_txt(req_content)
        except Exception:
            pass

    # 3. ပေါင်း
    all_packages = list(set(packages_from_code + packages_from_req))

    # 4. မဖြစ်မနေ လိုတာ ထည့် (bot host ကို run ဖို့)
    essentials = ["pyTelegramBotAPI", "aiohttp", "aiofiles"]
    for e in essentials:
        if e not in all_packages:
            all_packages.append(e)

    await write_log_line(
        log_file,
        f"🔍 Detected imports: {', '.join(sorted(imports)) or '(none)'}",
    )

    # 5. Install
    ok, msg = await install_packages(all_packages, log_file, chat_id, bot_name)
    return ok, msg


# ═══════════════════════════════════════════════════════
# ⭐ DOWNLOAD HELPER
# ═══════════════════════════════════════════════════════

async def download_file_safe(file_id: str) -> bytes:
    fi = await bot.get_file(file_id)
    result = await bot.download_file(fi.file_path)
    if isinstance(result, bytes):
        return result
    if hasattr(result, "read"):
        data = result.read()
        if isinstance(data, bytes):
            return data
        return data.encode() if isinstance(data, str) else bytes(data)
    return bytes(result)


# ═══════════════════════════════════════════════════════
# 【 USER MANAGEMENT 】
# ═══════════════════════════════════════════════════════

def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMIN_IDS


def get_user(user_id: int) -> dict:
    uid = str(user_id)
    if uid not in users_data:
        users_data[uid] = {
            "user_id": user_id,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "premium": False,
            "premium_expires": None,
            "bots": [],
        }
    return users_data[uid]


def is_premium(user_id: int) -> bool:
    if is_admin(user_id):
        return True
    u = get_user(user_id)
    if not u.get("premium"):
        return False
    exp = u.get("premium_expires")
    if not exp:
        return False
    try:
        dt = datetime.fromisoformat(exp)
        return datetime.now(timezone.utc) < dt
    except Exception:
        return False


def max_bots_for(user_id: int) -> int:
    if is_admin(user_id):
        return 999
    if is_premium(user_id):
        return MAX_BOTS_PREMIUM
    return MAX_BOTS_PER_USER


def user_bots(user_id: int) -> list[dict]:
    return get_user(user_id).get("bots", [])


# ═══════════════════════════════════════════════════════
# 【 BOT PROCESS MANAGEMENT 】
# ═══════════════════════════════════════════════════════

def bot_key(user_id: int, bot_name: str) -> str:
    return f"{user_id}_{bot_name}"


def user_bot_dir(user_id: int, bot_name: str = "") -> Path:
    p = BOTS_DIR / str(user_id)
    if bot_name:
        p = p / bot_name
    return p


async def write_log_line(log_path: Path, line: str) -> None:
    try:
        async with aiofiles.open(log_path, "a", encoding="utf-8") as f:
            ts = datetime.now().strftime("%H:%M:%S")
            await f.write(f"[{ts}] {line}\n")
    except Exception:
        pass


async def start_bot_process(
    user_id: int, bot_name: str, auto_install: bool = True
) -> tuple[bool, str]:
    """Bot ကို run + Auto-install"""
    key = bot_key(user_id, bot_name)

    if key in running_bots:
        info = running_bots[key]
        if info["proc"].returncode is None:
            return False, f"⚠️ `{bot_name}` လည်ပတ်နေပြီ — Stop အရင်လုပ်ပါ"
        else:
            running_bots.pop(key, None)

    bot_dir = user_bot_dir(user_id, bot_name)
    py_file = bot_dir / f"{bot_name}.py"
    if not py_file.exists():
        return False, f"❌ File not found: {py_file.name}"

    abs_bot_dir = bot_dir.resolve()
    abs_py_file = py_file.resolve()

    log_file = LOGS_DIR / f"{key}.log"
    log_file.write_text("")

    # ⭐ AUTO-INSTALL
    if auto_install:
        await write_log_line(log_file, "🔍 Auto-detecting imports...")
        ok, msg = await auto_install_for_bot(user_id, bot_name, user_id)
        if not ok:
            await write_log_line(log_file, f"⚠️ Auto-install failed: {msg}")
            try:
                await bot.send_message(
                    user_id,
                    f"⚠️ *Auto-install warning* for `{bot_name}`:\n```\n{msg[:500]}\n```\n\n"
                    f"Bot ကို run ကြည့်ပါမယ်...",
                )
            except Exception:
                pass
        else:
            await write_log_line(log_file, "✅ Auto-install complete")

    # ─── Start bot ───
    await write_log_line(log_file, "🚀 Starting bot...")
    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-u", str(abs_py_file),
            cwd=str(abs_bot_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            start_new_session=True,
        )
    except Exception as e:
        return False, f"Failed to start: {e}"

    running_bots[key] = {
        "proc": proc,
        "started_at": time.time(),
        "log_file": log_file,
        "user_id": user_id,
        "bot_name": bot_name,
    }

    async def _pipe_output():
        err_count = 0
        err_buffer: list[str] = []
        try:
            with open(log_file, "a", encoding="utf-8", errors="ignore") as lf:
                while True:
                    line = await proc.stdout.readline()
                    if not line:
                        break
                    ts = datetime.now().strftime("%H:%M:%S")
                    text = line.decode("utf-8", errors="ignore").rstrip()
                    try:
                        lf.write(f"[{ts}] {text}\n")
                        lf.flush()
                    except Exception:
                        pass

                    low = text.lower()
                    if ("error" in low or "traceback" in low or "conflict" in low
                            or "exception" in low or "modulenotfound" in low
                            or "can't open file" in low or "syntaxerror" in low):
                        err_buffer.append(text)
                        err_count += 1
                        if err_count <= 8:
                            try:
                                await bot.send_message(
                                    user_id,
                                    f"⚠️ *{bot_name}* error:\n```\n{text[:500]}\n```"
                                )
                            except Exception:
                                pass
        except Exception:
            pass

    asyncio.create_task(_pipe_output())
    await write_log_line(log_file, "✅ Bot started successfully")
    return True, f"✅ `{bot_name}` started (auto-installed)"


async def stop_bot_process(user_id: int, bot_name: str) -> tuple[bool, str]:
    key = bot_key(user_id, bot_name)
    info = running_bots.get(key)
    if not info:
        return False, "Bot is not running"
    proc = info["proc"]
    try:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:
            proc.terminate()
        try:
            await asyncio.wait_for(proc.wait(), timeout=10)
        except asyncio.TimeoutError:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except Exception:
                proc.kill()
        await write_log_line(info["log_file"], "🛑 Bot stopped")
    except Exception as e:
        return False, f"Stop error: {e}"
    running_bots.pop(key, None)
    return True, "Bot stopped"


def is_bot_running(user_id: int, bot_name: str) -> bool:
    key = bot_key(user_id, bot_name)
    info = running_bots.get(key)
    if not info:
        return False
    if info["proc"].returncode is not None:
        running_bots.pop(key, None)
        return False
    return True


def uptime_str(seconds: float) -> str:
    s = int(seconds)
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    if h:
        return f"{h}h {m}m"
    if m:
 
