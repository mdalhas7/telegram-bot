import asyncio
import json
import re
import time
from datetime import datetime, timedelta
import pytz
import threading
import requests
import websockets
import socketio  # python-socketio client

# Telegram & IVASMS tokens / IDs

main_otp_bots = ["7656622277:AAErgH8Dw66VT8KgiHZxHvUmKoKPuHbGGiM"]

CHAT_ID1 = "7656622277"

token = "_ga=GA1.2.1223426737.1752139250; _gid=GA1.2.1102270477.1752139250; _fbp=fb.1.1752139250130.535596848407044854; XSRF-TOKEN=eyJpdiI6ImtHVktJczhHSFhpeURZcXhqeDg1Q0E9PSIsInZhbHVlIjoiSFpNUmp0ZnhuWlVuak9pWmthUW44dC9KSVVvdExndVJRWEpaZWxJRWgzeGd3UWkzZitDM3I0Zy82ejF3YURaV2xzS2htdzlybzlUYUx3RkRIWlljVjBkWFdJZmRYNnJReXRyVTd2UWhQRmtBYVl3TGJHbC9OeStTUFlxWkMzSy8iLCJtYWMiOiI5NjM3YTU3MzQyZWVlM2NkODNkYTIzMTNiNDBmYjM3ZTFkYjMyZmI1N2MwMGYwYzljYjJlMWVhMzNiMTE3YmFkIiwidGFnIjoiIn0%3D; ivas_sms_session=eyJpdiI6Ik11R2JQb2dqa09kV3hDVGU1aG5BM1E9PSIsInZhbHVlIjoiRjV6UVJtNzN3U0pYOGVFdUt5MldkV01YL3g3SlpueHB0R1lIOWFEbFZxNWJoSmNHT1lSLzBTYk5IRDFhL3dvYWg3SDRQUVFnbUV1d213WWxJTUFueW9oaElVeHl4ODR4NDRZdTlDOE1jNWI4OS9YQjRINmQzVlJEajFXSHp4bEgiLCJtYWMiOiI2MWRhZDkxNDM5N2NmODZiOWFlM2YxMWEyYzVlMzFiYzcyNWY4YzlkYzdhYTMwNDkxZDUyYzYwNWMzYzFjYjIxIiwidGFnIjoiIn0%3D; _gat_gtag_UA_191466370_1=1"  # তোমার টোকেন এখানে দাও

ws_url = f"wss://ivasms.com:2087/socket.io/?token={requests.utils.quote(token)}&EIO=4&transport=websocket"

# bot index trackers
bot_index = {
    "otp": 0
}


def escape_html(unsafe: str) -> str:
    return (unsafe.replace("&", "&amp;")
                  .replace("<", "&lt;")
                  .replace(">", "&gt;")
                  .replace('"', "&quot;")
                  .replace("'", "&#039;"))

def send_to_telegram(bot_type, chat_id, text):
    bots = main_otp_bots
    index = bot_index[bot_type]
    total = len(bots)
    tried = 0

    while tried < total:
        token = bots[index]
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            print(f"✔️ Message sent to Telegram 📩 — via {bot_type.upper()} Bot {index + 1}")
            bot_index[bot_type] = index
            return
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:
                print(f"⚠️ Bot {index + 1} rate-limited. Trying next...")
                index = (index + 1) % total
                tried += 1
                time.sleep(1.5)
            else:
                print("⚠️ HTTP error:", e)
                break
        except Exception as e:
            print("⚠️ Telegram error:", e)
            break

    print(f"🚫 All {bot_type.upper()} bots failed.")

async def connect_ws():
    while True:
        try:
            async with websockets.connect(ws_url) as ws:
                print("🖥️ Panel connected successfully ✅")
                while True:
                    data = await ws.recv()
                    if data.startswith("0"):
                        await ws.send("40/livesms,")
                        continue
                    if data == "2":
                        await ws.send("3")
                        continue
                    if "/livesms" in data:
                        try:
                            payload = json.loads(data[data.index('['):])
                            msg = payload[1]
                            bd_time = datetime.utcnow().astimezone(pytz.timezone('Asia/Dhaka')) \
                                               .strftime("%d/%m/%Y, %H:%M:%S")
                            m = re.search(r"\b\d{4,}\b|\b\d{2,}-\d{2,}\b|\d{2,} \d{2,}\b", msg['message'])
                            otp = m.group(0) if m else "N/A"
                            text = (
                                f"✨ <b> ROBIUL OTP Received</b> ✨\n\n"
                                f"⏰ <b>Time:</b> {bd_time}\n"
                                f"📞 <b>Number:</b> {msg['recipient']}\n"
                                f"🔧 <b>Service:</b> {msg['originator']}\n\n"
                                f"🔑 <b>OTP Code:</b> <code>{otp}</code>\n\n"
                                f"<blockquote>{escape_html(msg['message'])}</blockquote>"
                            )
                            send_to_telegram("otp", CHAT_ID1, text)
                        except Exception as e:
                            print("📥 Receiving OTPs from panel ✅")
        except Exception as e:
            print("🔴 Connection closed or ⚠️ error:", e)
            print("🔁 Reconnecting in 5s...")
            time.sleep(5)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [
        loop.create_task(connect_ws()),
    ]
    loop.run_until_complete(asyncio.wait(tasks))

if __name__ == "__main__":
    main()
