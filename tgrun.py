import json
import requests
import time
from datetime import datetime

# Baca akun dari file
with open("accounts.json", "r", encoding='utf-8') as f:
    accounts = json.load(f)

login_url = "https://tgrun.xyz/api/auth/login"
spin_url = "https://tgrun.xyz/api/spin/case_13"

hadiah_log = []

# Mulai loop terus-menerus
while True:
    for idx, acc in enumerate(accounts):
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Akun #{idx+1}: {acc['first_name']}")

        session = requests.Session()

        # Payload login
        login_payload = {
            "initDataRaw": acc["init_data"],
            "telegramId": acc["telegram_id"],
            "firstName": acc["first_name"],
            "photoUrl": acc["photo_url"],
            "refId": "unknown"
        }

        headers = {
            "Content-Type": "application/json",
            "Origin": "https://tgrun.xyz",
            "Referer": "https://tgrun.xyz/",
            "ngrok-skip-browser-warning": "true"
        }

        try:
            login_res = session.post(login_url, json=login_payload, headers=headers)
            if login_res.status_code != 200:
                print(f"[X] Gagal login: {login_res.status_code}")
                continue
            print(f"[✅] Login sukses!")

            # Spin
            spin_payload = {
                "telegramId": acc["telegram_id"]
            }

            spin_res = session.post(spin_url, json=spin_payload, headers=headers)
            spin_data = spin_res.json()

            gift = spin_data.get("gift")
            if gift and gift.get("price", 0) > 0:
                hadiah_text = f"{acc['first_name']} {gift['name']} {gift['price']}"
                print(f"[🎁] Dapat hadiah: {hadiah_text}")
                hadiah_log.append(hadiah_text)
            else:
                print(f"[🙁] Tidak dapat hadiah.")

        except Exception as e:
            print(f"[⚠️] Error akun {acc['telegram_id']}: {e}")

        time.sleep(2) 

    
    if hadiah_log:
        tanggal = datetime.now().strftime("%Y-%m-%d")
        filename = f"hadiah_log_{tanggal}.txt"
        with open(filename, "a", encoding='utf-8') as f:
            for hadiah in hadiah_log:
                f.write(hadiah + "\n")
        print(f"\n[💾] Disimpan ke {filename} ({len(hadiah_log)} item)")
        hadiah_log.clear()

    print(f"\n[⏳] Selesai 1x putaran semua akun. Tidur 24 jam...\n")
    time.sleep(86400) 
