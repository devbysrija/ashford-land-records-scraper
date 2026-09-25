import requests
import browser_cookie3
import shutil
import tempfile
import os
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

GOOGLE_SCRIPT = "https://script.google.com/macros/s/AKfycbynyzdWQvHTxvH7SLnlvBmvapV6wGZZtXkZlFKWlhOUiou75Uc5aG9UMmafrGw87LjZ/exec"
BASE = "https://searchiqs.com/CTASH/SearchAdvancedMP.aspx"

# -----------------------
# Use browser cookies
# -----------------------
# ---------- Read Edge cookies without Admin ----------
edge_cookie = os.path.join(
    os.environ["LOCALAPPDATA"],
    r"Microsoft\Edge\User Data\Default\Network\Cookies"
)

temp_cookie = os.path.join(tempfile.gettempdir(), "edge_cookies.db")
shutil.copy2(edge_cookie, temp_cookie)

cookies = browser_cookie3.edge(
    cookie_file=temp_cookie,
    domain_name="searchiqs.com"
)

session = requests.Session()
session.cookies.update(cookies)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": BASE
}

# -----------------------
# Dynamic dates
# -----------------------
today = datetime.today()
from_date = (today - timedelta(days=80)).strftime("%m/%d/%Y")
to_date = today.strftime("%m/%d/%Y")

print("FROM :", from_date)
print("TO   :", to_date)

# -----------------------
# Open search page
# -----------------------
r = session.get(BASE, headers=headers)
r.raise_for_status()

soup = BeautifulSoup(r.text, "lxml")

# Hidden ASP.NET fields
payload = {}

for h in soup.select("input[type=hidden]"):
    payload[h["name"]] = h.get("value", "")

# Required fields
payload.update({
    "ctl00$ContentPlaceHolder1$txtFromDate": from_date,
    "ctl00$ContentPlaceHolder1$txtThruDate": to_date,
    "ctl00$ContentPlaceHolder1$cboDocGroup": "LR",
    "ctl00$ContentPlaceHolder1$cboDocType": "(ALL)",
    "ctl00$ContentPlaceHolder1$cmdSearch": "Search"
})

# -----------------------
# Submit search
# -----------------------
r = session.post(BASE, data=payload, headers=headers)
soup = BeautifulSoup(r.text, "lxml")

records = []

def scrape_table(soup):
    tables = soup.find_all("table")

    for table in tables:
        heads = [x.get_text(strip=True) for x in table.find_all("th")]

        if "Party 1" in heads:
            for tr in table.find_all("tr")[1:]:
                td = [x.get_text(" ", strip=True) for x in tr.find_all("td")]

                if len(td) >= 8:
                    records.append({
                        "Party 1": td[0],
                        "Party 2": td[1],
                        "Type": td[2],
                        "Book-Page": td[3],
                        "Date": td[4],
                        "Description": td[5],
                        "Additional Description": td[6],
                        "Related": td[7]
                    })

# First page
scrape_table(soup)

# -----------------------
# Pagination
# -----------------------
while True:

    next_link = soup.find("a", string="Next")

    if not next_link:
        break

    href = next_link["href"]
    target = href.split("'")[1]

    next_payload = {}

    for h in soup.select("input[type=hidden]"):
        next_payload[h["name"]] = h.get("value", "")

    next_payload["__EVENTTARGET"] = target

    r = session.post(BASE, data=next_payload, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    scrape_table(soup)

# -----------------------
# Save CSV
# -----------------------
df = pd.DataFrame(records)
df.to_csv("output.csv", index=False)

print("TOTAL RECORDS :", len(df))

# -----------------------
# Google Sheet
# -----------------------
if len(records):
    requests.post(GOOGLE_SCRIPT, json=records)

print("DONE")