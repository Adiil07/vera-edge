import requests, time
while True:
    try:
        r = requests.get("https://vera-edge.onrender.com", timeout=30)
        print(f"OK {r.status_code} — {time.ctime()}")
    except: print(f"FAIL — {time.ctime()}")
    time.sleep(60)