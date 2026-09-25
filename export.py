import pandas as pd
import requests

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbynyzdWQvHTxvH7SLnlvBmvapV6wGZZtXkZlFKWlhOUiou75Uc5aG9UMmafrGw87LjZ/exec"

# Read CSV
df = pd.read_csv("ashford_land_records.csv")

# Replace NaN with empty string
df = df.fillna("")

# Convert everything to string
df = df.astype(str)

records = df.to_dict(orient="records")

r = requests.post(WEB_APP_URL, json=records)

print("Status:", r.status_code)
print("Response:", r.text)