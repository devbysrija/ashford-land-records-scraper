from bs4 import BeautifulSoup
import pandas as pd
import os

files = ["page1.html", "page2.html"]
records = []

for file in files:
    if not os.path.exists(file):
        print(f"{file} not found")
        continue

    print("Reading", file)

    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find every table
    for table in soup.find_all("table"):

        rows = table.find_all("tr")
        if not rows:
            continue

        # SearchIQS uses TD instead of TH
        header = [c.get_text(" ", strip=True) for c in rows[0].find_all(["td","th"])]

        if "Party 1" not in header:
            continue

        # Data rows
        for tr in rows[1:]:
            td = [x.get_text(" ", strip=True) for x in tr.find_all("td")]

            if len(td) < 10:
                continue

            records.append({
                "Party 1": td[2],
                "Party 2": td[3],
                "Type": td[4],
                "Book-Page": td[5],
                "Date": td[6],
                "Description": td[7],
                "Additional Description": td[8],
                "Related": td[9]
            })

df = pd.DataFrame(records)

df.to_csv("ashford_land_records.csv", index=False)

print(df.head())
print("TOTAL RECORDS:", len(df))
print("CSV Saved")