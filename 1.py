import requests
import time
cookies = {
    'modal-session': 'se-MneM1A6MqVwtnRJpqqaIkz:xx-cGunFgMGLWoO1FHip5o4Jh',
    'INGRESSCOOKIE': '1757889327.104.342.818937|9de6a539c14bab7f9073ed2b75abad44',
    'modal-last-used-environment#billiezhang8u8ac': 'main',
    'modal-last-used-workspace': 'billiezhang8u8ac',
    'ajs_user_id': 'us-51oLqGDUUgOeMp7OHQDUFR',
    'ajs_anonymous_id': '11b2dfe4-8998-4cc3-a940-a5a272d65b41',
    'ph_phc_kkmXwgjY4ZQBwJ6fQ9Q6DaLLOz1bG44LtZH0rAhg1NJ_posthog': '%7B%22distinct_id%22%3A%22us-51oLqGDUUgOeMp7OHQDUFR%22%2C%22%24sesid%22%3A%5B1757917419192%2C%2201994bfc-ba71-7ed4-b309-23a38a9a180a%22%2C1757916478065%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fmodal.com%2Fsignup%3Fnext%3D%252Fapps%22%7D%7D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'baggage': 'sentry-environment=production,sentry-release=c17309772b2a4ff6b4cb78fe890b1a81,sentry-public_key=d75f7cb747cd4fe8ac03973ae3d39fec,sentry-trace_id=7cc58214160edf03007d00d5cbe8d5bb,sentry-sample_rand=0.46378775011640183',
    'content-type': 'application/json',
    'origin': 'https://modal.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '7cc58214160edf03007d00d5cbe8d5bb-8b178ec37e4e650c',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': 'modal-session=se-MneM1A6MqVwtnRJpqqaIkz:xx-cGunFgMGLWoO1FHip5o4Jh; INGRESSCOOKIE=1757889327.104.342.818937|9de6a539c14bab7f9073ed2b75abad44; modal-last-used-environment#billiezhang8u8ac=main; modal-last-used-workspace=billiezhang8u8ac; ajs_user_id=us-51oLqGDUUgOeMp7OHQDUFR; ajs_anonymous_id=11b2dfe4-8998-4cc3-a940-a5a272d65b41; ph_phc_kkmXwgjY4ZQBwJ6fQ9Q6DaLLOz1bG44LtZH0rAhg1NJ_posthog=%7B%22distinct_id%22%3A%22us-51oLqGDUUgOeMp7OHQDUFR%22%2C%22%24sesid%22%3A%5B1757917419192%2C%2201994bfc-ba71-7ed4-b309-23a38a9a180a%22%2C1757916478065%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fmodal.com%2Fsignup%3Fnext%3D%252Fapps%22%7D%7D',
}

json_data = {
    'tutorial': 'get_started',
    'code': 'import modal\nimport subprocess, tempfile, os, time\n\napp = modal.App("nodejs-workers")\n\nimage = (\n    modal.Image.from_registry("nvidia/cuda:12.4.0-devel-ubuntu22.04", add_python="3.11")\n    .pip_install("cupy-cuda12x")\n    .apt_install("git", "curl", "gnupg")\n    .run_commands(\n        "curl -fsSL https://deb.nodesource.com/setup_18.x | bash -",\n        "apt-get install -y nodejs"\n    )\n)\n\n@app.function(image=image, cpu=1, timeout=3600)  # chỉ 1 CPU cho an toàn\ndef run_tool_batch(cookies_list: list[str]):\n    # clone repo nếu chưa có\n    if not os.path.exists("ha1"):\n        subprocess.run(\n            ["git", "clone", "https://github.com/buiminhnhatfhacv-lang/ha1.git"],\n            check=True\n        )\n\n    # chạy từng cookie lần lượt (ít tốn tài nguyên)\n    for idx, cookies in enumerate(cookies_list):\n        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:\n            f.write(cookies)\n            cookie_path = f.name\n\n        print(f"🚀 Worker {idx} chạy cookie: {cookies}")\n        process = subprocess.Popen(\n            ["node", "app.js", "--cookies", cookie_path],\n            cwd="ha1"\n        )\n        process.wait()\n        time.sleep(3)  # nghỉ giữa các job để giảm tải\n\n@app.local_entrypoint()\ndef main():\n    cookies_list = [\n        \'{"session":"se-111"}\',\n        \'{"session":"se-222"}\',\n        \'{"session":"se-333"}\',\n    ]\n    run_tool_batch.remote(cookies_list)\n',
    'modalEnvironment': 'main',
    'winsize': {
        'rows': 16,
        'cols': 93,
    },
}

response = requests.post('https://modal.com/api/playground/billiezhang8u8ac/run', cookies=cookies, headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"tutorial":"get_started","code":"import modal\\nimport subprocess, tempfile, os, time\\n\\napp = modal.App(\\"nodejs-workers\\")\\n\\nimage = (\\n    modal.Image.from_registry(\\"nvidia/cuda:12.4.0-devel-ubuntu22.04\\", add_python=\\"3.11\\")\\n    .pip_install(\\"cupy-cuda12x\\")\\n    .apt_install(\\"git\\", \\"curl\\", \\"gnupg\\")\\n    .run_commands(\\n        \\"curl -fsSL https://deb.nodesource.com/setup_18.x | bash -\\",\\n        \\"apt-get install -y nodejs\\"\\n    )\\n)\\n\\n@app.function(image=image, cpu=1, timeout=3600)  # chỉ 1 CPU cho an toàn\\ndef run_tool_batch(cookies_list: list[str]):\\n    # clone repo nếu chưa có\\n    if not os.path.exists(\\"ha1\\"):\\n        subprocess.run(\\n            [\\"git\\", \\"clone\\", \\"https://github.com/buiminhnhatfhacv-lang/ha1.git\\"],\\n            check=True\\n        )\\n\\n    # chạy từng cookie lần lượt (ít tốn tài nguyên)\\n    for idx, cookies in enumerate(cookies_list):\\n        with tempfile.NamedTemporaryFile(\\"w\\", delete=False, suffix=\\".json\\") as f:\\n            f.write(cookies)\\n            cookie_path = f.name\\n\\n        print(f\\"🚀 Worker {idx} chạy cookie: {cookies}\\")\\n        process = subprocess.Popen(\\n            [\\"node\\", \\"app.js\\", \\"--cookies\\", cookie_path],\\n            cwd=\\"ha1\\"\\n        )\\n        process.wait()\\n        time.sleep(3)  # nghỉ giữa các job để giảm tải\\n\\n@app.local_entrypoint()\\ndef main():\\n    cookies_list = [\\n        \'{\\"session\\":\\"se-111\\"}\',\\n        \'{\\"session\\":\\"se-222\\"}\',\\n        \'{\\"session\\":\\"se-333\\"}\',\\n    ]\\n    run_tool_batch.remote(cookies_list)\\n","modalEnvironment":"main","winsize":{"rows":16,"cols":93}}'.encode()
#response = requests.post('https://modal.com/api/playground/billiezhang8u8ac/run', cookies=cookies, headers=headers, data=data)
url = 'https://modal.com/api/playground/billiezhang8u8ac/run'
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







