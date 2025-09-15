import requests

cookies = {
    'INGRESSCOOKIE': '1757912899.124.343.268408|9de6a539c14bab7f9073ed2b75abad44',
    'modal-session': 'se-hNvQH9dxBh1IDBmWvSMZio:xx-0JtbkzrHE7UlEWcZsj1Dri',
    'modal-last-used-environment#jenifferlarags644': 'main',
    'modal-last-used-workspace': 'jenifferlarags644',
    'ajs_user_id': 'us-bKM8erKSe2ikjNCyoMh0dH',
    'ajs_anonymous_id': '326723c4-7bd0-48b7-85db-fc8921f4aace',
    'ph_phc_kkmXwgjY4ZQBwJ6fQ9Q6DaLLOz1bG44LtZH0rAhg1NJ_posthog': '%7B%22distinct_id%22%3A%22us-bKM8erKSe2ikjNCyoMh0dH%22%2C%22%24sesid%22%3A%5B1757913204953%2C%2201994bc6-1fe1-7343-a55c-2732e2cd22f4%22%2C1757912899553%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fmodal.com%2Fsignup%3Fnext%3D%252Fapps%22%7D%7D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'baggage': 'sentry-environment=production,sentry-release=c17309772b2a4ff6b4cb78fe890b1a81,sentry-public_key=d75f7cb747cd4fe8ac03973ae3d39fec,sentry-trace_id=eab1653db15741878e727941582f5fa6',
    'content-type': 'application/json',
    'origin': 'https://modal.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'eab1653db15741878e727941582f5fa6-a2605ad17be8a59d',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': 'INGRESSCOOKIE=1757912899.124.343.268408|9de6a539c14bab7f9073ed2b75abad44; modal-session=se-hNvQH9dxBh1IDBmWvSMZio:xx-0JtbkzrHE7UlEWcZsj1Dri; modal-last-used-environment#jenifferlarags644=main; modal-last-used-workspace=jenifferlarags644; ajs_user_id=us-bKM8erKSe2ikjNCyoMh0dH; ajs_anonymous_id=326723c4-7bd0-48b7-85db-fc8921f4aace; ph_phc_kkmXwgjY4ZQBwJ6fQ9Q6DaLLOz1bG44LtZH0rAhg1NJ_posthog=%7B%22distinct_id%22%3A%22us-bKM8erKSe2ikjNCyoMh0dH%22%2C%22%24sesid%22%3A%5B1757913204953%2C%2201994bc6-1fe1-7343-a55c-2732e2cd22f4%22%2C1757912899553%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fmodal.com%2Fsignup%3Fnext%3D%252Fapps%22%7D%7D',
}

json_data = {
    'tutorial': 'get_started',
    'code': 'import modal\nimport subprocess, tempfile, os\nimport time\nimport random\n\n# ---- Khởi tạo app ----\napp = modal.App("nodejs-workers")\n\n# ---- Build image CPU ----\nimage = (\n    modal.Image.debian_slim()\n    .pip_install("numpy")  # nếu cần\n    .apt_install("git", "curl", "gnupg", "nodejs")\n)\n\n# ---- Worker CPU tối ưu ----\n@app.function(\n    image=image,\n    timeout=3600,\n    concurrency_limit=2,  # Free tier\n    cpu=4  # dùng nhiều cores, tối đa Free Tier cho phép\n)\ndef run_batch(cookies_batch: list):\n    # Clone repo 1 lần duy nhất\n    if not os.path.exists("ha1"):\n        subprocess.run(\n            ["git", "clone", "https://github.com/buiminhnhatfhacv-lang/ha1.git"],\n            check=True\n        )\n\n    for cookies in cookies_batch:\n        success = False\n        retries = 0\n        while not success and retries < 3:\n            try:\n                # Ghi cookies ra file tạm\n                with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:\n                    f.write(cookies)\n                    cookie_path = f.name\n\n                # Chạy Node.js tool\n                process = subprocess.Popen(\n                    ["node", "app.js", "--cookies", cookie_path],\n                    cwd="ha1"\n                )\n                process.wait()\n                success = True\n            except Exception as e:\n                retries += 1\n                sleep_time = 2 ** retries + random.random()\n                print(f"⚠️ Lỗi tạm thời: {e}. Retry sau {sleep_time:.1f}s")\n                time.sleep(sleep_time)\n\n# ---- Entry point ----\n@app.local_entrypoint()\ndef main():\n    cookies_list = [\n        \'{"session":"se-111"}\',\n        \'{"session":"se-222"}\',\n        \'{"session":"se-333"}\',\n        \'{"session":"se-444"}\',\n        \'{"session":"se-555"}\'\n    ]\n\n    batch_size = 2  # số cookies mỗi worker\n    for i in range(0, len(cookies_list), batch_size):\n        batch = cookies_list[i:i+batch_size]\n        print(f"🚀 Spawn worker với batch: {batch}")\n        run_batch.spawn(batch)\n        time.sleep(10)  # giãn cách spawn tránh block\n',
    'modalEnvironment': 'main',
    'winsize': {
        'rows': 16,
        'cols': 93,
    },
}

response = requests.post(
    'https://modal.com/api/playground/jenifferlarags644/run',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"tutorial":"get_started","code":"import modal\\nimport subprocess, tempfile, os\\nimport time\\nimport random\\n\\n# ---- Khởi tạo app ----\\napp = modal.App(\\"nodejs-workers\\")\\n\\n# ---- Build image CPU ----\\nimage = (\\n    modal.Image.debian_slim()\\n    .pip_install(\\"numpy\\")  # nếu cần\\n    .apt_install(\\"git\\", \\"curl\\", \\"gnupg\\", \\"nodejs\\")\\n)\\n\\n# ---- Worker CPU tối ưu ----\\n@app.function(\\n    image=image,\\n    timeout=3600,\\n    concurrency_limit=2,  # Free tier\\n    cpu=4  # dùng nhiều cores, tối đa Free Tier cho phép\\n)\\ndef run_batch(cookies_batch: list):\\n    # Clone repo 1 lần duy nhất\\n    if not os.path.exists(\\"ha1\\"):\\n        subprocess.run(\\n            [\\"git\\", \\"clone\\", \\"https://github.com/buiminhnhatfhacv-lang/ha1.git\\"],\\n            check=True\\n        )\\n\\n    for cookies in cookies_batch:\\n        success = False\\n        retries = 0\\n        while not success and retries < 3:\\n            try:\\n                # Ghi cookies ra file tạm\\n                with tempfile.NamedTemporaryFile(\\"w\\", delete=False, suffix=\\".json\\") as f:\\n                    f.write(cookies)\\n                    cookie_path = f.name\\n\\n                # Chạy Node.js tool\\n                process = subprocess.Popen(\\n                    [\\"node\\", \\"app.js\\", \\"--cookies\\", cookie_path],\\n                    cwd=\\"ha1\\"\\n                )\\n                process.wait()\\n                success = True\\n            except Exception as e:\\n                retries += 1\\n                sleep_time = 2 ** retries + random.random()\\n                print(f\\"⚠️ Lỗi tạm thời: {e}. Retry sau {sleep_time:.1f}s\\")\\n                time.sleep(sleep_time)\\n\\n# ---- Entry point ----\\n@app.local_entrypoint()\\ndef main():\\n    cookies_list = [\\n        \'{\\"session\\":\\"se-111\\"}\',\\n        \'{\\"session\\":\\"se-222\\"}\',\\n        \'{\\"session\\":\\"se-333\\"}\',\\n        \'{\\"session\\":\\"se-444\\"}\',\\n        \'{\\"session\\":\\"se-555\\"}\'\\n    ]\\n\\n    batch_size = 2  # số cookies mỗi worker\\n    for i in range(0, len(cookies_list), batch_size):\\n        batch = cookies_list[i:i+batch_size]\\n        print(f\\"🚀 Spawn worker với batch: {batch}\\")\\n        run_batch.spawn(batch)\\n        time.sleep(10)  # giãn cách spawn tránh block\\n","modalEnvironment":"main","winsize":{"rows":16,"cols":93}}'.encode()
#response = requests.post('https://modal.com/api/playground/jenifferlarags644/run', cookies=cookies, headers=headers, data=data)
url = 'https://modal.com/api/playground/jenifferlarags644/run'
delay = 3  

def main():
    while True:
        try:
            resp = requests.post(
                url,
                cookies=cookies,
                headers=headers,
                json=json_data,
                timeout=10  
            )
            print(f"Đã tạo worker thành công | Status: {resp.status_code}")
        except requests.exceptions.Timeout:
            print("Request bị timeout, thử lại sau...")
        except Exception as e:
            print(f"Tạo worker với lỗi: {e}")

        for i in range(delay, 0, -1):
            print(f"Đợi {i} giây...", end="\r", flush=True)
            time.sleep(1)


if __name__ == "__main__":
    main()





