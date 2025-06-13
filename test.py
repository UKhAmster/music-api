import requests

try:
    r = requests.get("http://127.0.0.1:8000/search", params={"query": "Mozart"})
    print("Status:", r.status_code)
    print("Response:")
    print(r.text)
except Exception as e:
    print("❌ Ошибка:", e)