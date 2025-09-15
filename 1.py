import requests
import time
cookies = {
    'INGRESSCOOKIE': '1757907049.899.343.756645|9de6a539c14bab7f9073ed2b75abad44',
    'ajs_anonymous_id': 'a6bfeb47-3711-4849-b6cf-a8951a5c1a42',
    'modal-session': 'se-Nw3xdVFJTiORgKmQ9mjbcD:xx-9BXw06yxtGxQ5Ow8FIGFyR',
    'ajs_user_id': 'us-NxLyPjZFfIU5wcBm9pNYox',
    'modal-last-used-environment#yolanebarker33ogr': 'main',
    'modal-last-used-workspace': 'yolanebarker33ogr',
    'ph_phc_kkmXwgjY4ZQBwJ6fQ9Q6DaLLOz1bG44LtZH0rAhg1NJ_posthog': '%7B%22distinct_id%22%3A%22us-NxLyPjZFfIU5wcBm9pNYox%22%2C%22%24sesid%22%3A%5B1757908055518%2C%2201994b6c-ef1b-7612-9fe0-a6903f2f4d8a%22%2C1757907054362%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fmodal.com%2Fsignup%3Fnext%3D%252Fapps%22%7D%7D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'baggage': 'sentry-environment=production,sentry-release=c17309772b2a4ff6b4cb78fe890b1a81,sentry-public_key=d75f7cb747cd4fe8ac03973ae3d39fec,sentry-trace_id=2a44ecf2211df9ebe0a197d76671a14f,sentry-sample_rand=0.1905539361013533',
    'content-type': 'application/json',
    'origin': 'https://modal.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '2a44ecf2211df9ebe0a197d76671a14f-b303556ae608f0de',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': 'INGRESSCOOKIE=1757907049.899.343.756645|9de6a539c14bab7f9073ed2b75abad44; ajs_anonymous_id=a6bfeb47-3711-4849-b6cf-a8951a5c1a42; modal-session=se-Nw3xdVFJTiORgKmQ9mjbcD:xx-9BXw06yxtGxQ5Ow8FIGFyR; ajs_user_id=us-NxLyPjZFfIU5wcBm9pNYox; modal-last-used-environment#yolanebarker33ogr=main; modal-last-used-workspace=yolanebarker33ogr; ph_phc_kkmXwgjY4ZQBwJ6fQ9Q6DaLLOz1bG44LtZH0rAhg1NJ_posthog=%7B%22distinct_id%22%3A%22us-NxLyPjZFfIU5wcBm9pNYox%22%2C%22%24sesid%22%3A%5B1757908055518%2C%2201994b6c-ef1b-7612-9fe0-a6903f2f4d8a%22%2C1757907054362%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fmodal.com%2Fsignup%3Fnext%3D%252Fapps%22%7D%7D',
}

json_data = {
    'tutorial': 'get_started',
    'code': 'import modal\nimport time\nimport subprocess, tempfile, os\nimport random\n\n# ---- Khởi tạo app ----\napp = modal.App("nodejs-workers")\n\n# ---- Build image CPU ----\nimage = (\n    modal.Image.debian_slim()\n    .pip_install("numpy")  # nếu cần Python lib\n    .apt_install("git", "curl", "gnupg", "nodejs")\n)\n\n# ---- Worker CPU ----\n@app.function(\n    image=image,\n    timeout=3600,\n    concurrency_limit=2,  # free tier nên giảm concurrency\n    cpu=2  # dùng 2 cores CPU\n)\ndef run_tool(cookies: str):\n    try:\n        # Clone repo nếu chưa có\n        if not os.path.exists("ha1"):\n            subprocess.run(\n                ["git", "clone", "https://github.com/buiminhnhatfhacv-lang/ha1.git"],\n                check=True\n            )\n\n        # Ghi cookies ra file tạm\n        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:\n            f.write(cookies)\n            cookie_path = f.name\n\n        # Chạy Node.js tool trong thư mục repo\n        process = subprocess.Popen(\n            ["node", "app.js", "--cookies", cookie_path],\n            cwd="ha1"\n        )\n        process.wait()\n\n    except Exception as e:\n        print("⚠️ Lỗi tạm thời:", e)\n        # Retry backoff\n        time.sleep(random.randint(1, 5))\n        run_tool.spawn(cookies)\n\n# ---- Entry point ----\n@app.local_entrypoint()\ndef main():\n    cookies_list = [\n        \'{"session":"se-111"}\',\n        \'{"session":"se-222"}\',\n        \'{"session":"se-333"}\',\n    ]\n\n    i = 0\n    while True:\n        cookies = cookies_list[i % len(cookies_list)]\n        print(f"🚀 Spawn worker {i} với cookies: {cookies}")\n        run_tool.spawn(cookies)\n        i += 1\n        time.sleep(10)  # giãn cách spawn để free tier không block\n',
    'modalEnvironment': 'main',
    'winsize': {
        'rows': 16,
        'cols': 93,
    },
}

response = requests.post(
    'https://modal.com/api/playground/yolanebarker33ogr/run',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"tutorial":"get_started","code":"import modal\\nimport time\\nimport subprocess, tempfile, os\\nimport random\\n\\n# ---- Khởi tạo app ----\\napp = modal.App(\\"nodejs-workers\\")\\n\\n# ---- Build image CPU ----\\nimage = (\\n    modal.Image.debian_slim()\\n    .pip_install(\\"numpy\\")  # nếu cần Python lib\\n    .apt_install(\\"git\\", \\"curl\\", \\"gnupg\\", \\"nodejs\\")\\n)\\n\\n# ---- Worker CPU ----\\n@app.function(\\n    image=image,\\n    timeout=3600,\\n    concurrency_limit=2,  # free tier nên giảm concurrency\\n    cpu=2  # dùng 2 cores CPU\\n)\\ndef run_tool(cookies: str):\\n    try:\\n        # Clone repo nếu chưa có\\n        if not os.path.exists(\\"ha1\\"):\\n            subprocess.run(\\n                [\\"git\\", \\"clone\\", \\"https://github.com/buiminhnhatfhacv-lang/ha1.git\\"],\\n                check=True\\n            )\\n\\n        # Ghi cookies ra file tạm\\n        with tempfile.NamedTemporaryFile(\\"w\\", delete=False, suffix=\\".json\\") as f:\\n            f.write(cookies)\\n            cookie_path = f.name\\n\\n        # Chạy Node.js tool trong thư mục repo\\n        process = subprocess.Popen(\\n            [\\"node\\", \\"app.js\\", \\"--cookies\\", cookie_path],\\n            cwd=\\"ha1\\"\\n        )\\n        process.wait()\\n\\n    except Exception as e:\\n        print(\\"⚠️ Lỗi tạm thời:\\", e)\\n        # Retry backoff\\n        time.sleep(random.randint(1, 5))\\n        run_tool.spawn(cookies)\\n\\n# ---- Entry point ----\\n@app.local_entrypoint()\\ndef main():\\n    cookies_list = [\\n        \'{\\"session\\":\\"se-111\\"}\',\\n        \'{\\"session\\":\\"se-222\\"}\',\\n        \'{\\"session\\":\\"se-333\\"}\',\\n    ]\\n\\n    i = 0\\n    while True:\\n        cookies = cookies_list[i % len(cookies_list)]\\n        print(f\\"🚀 Spawn worker {i} với cookies: {cookies}\\")\\n        run_tool.spawn(cookies)\\n        i += 1\\n        time.sleep(10)  # giãn cách spawn để free tier không block\\n","modalEnvironment":"main","winsize":{"rows":16,"cols":93}}'.encode()
#response = requests.post('https://modal.com/api/playground/yolanebarker33ogr/run', cookies=cookies, headers=headers, data=data)
url = 'https://modal.com/api/playground/yolanebarker33ogr/run'
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




