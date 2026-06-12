import requests
import pandas as pd
import time

#API
URL = "https://ajmb38a8f1.execute-api.us-east-1.amazonaws.com/pub/graphql"

Headers = {
    "Content-Type": "application/json",
    "Origin": "https://trydiscs.com",
    "Referer": "https://trydiscs.com/explore",
    "User-Agent": "Mozilla/5.0"    
}

#Query
Query = """
query ($limit: Int!, $offset: Int!, $filters: JSON) {
  getDiscMatrix(limit: $limit, offset: $offset, filters: $filters) {
    id
    name
    manufacturer
    speed
    glide
    turn
    fade
  }
}
"""

#Get disc info
def get_all(filters):
    rows = []
    limit = 100
    offset = 0

    while True:
        payload = {
            "query": Query,
            "variables": {
                "limit": limit,
                "offset": offset,
                "filters": filters
            }
        }

        r = requests.post(URL, json=payload, headers=Headers)

        if r.status_code != 200:
            print("Error: ", r.status_code)
            print(r.text[:300])
            break

        data = r.json()
        batch = data.get("data", {}).get("getDiscMatrix", [])

        if not batch:
            break

        rows.extend(batch)

        offset += limit
        time.sleep(0.15)
    
    return rows

#load disc info
all_discs = get_all(filters={})

#active and discontinued discs
active_discs = get_all(filters={"include": ["active"]})

all_ids = set(d["id"] for d in all_discs)
active_ids = set(d["id"] for d in active_discs)

discontinued_ids = all_ids - active_ids

for d in all_discs:
    d["discontinued"] = d["id"] in discontinued_ids

#data clean up
df = pd.DataFrame(all_discs)

df = df.rename(columns={"name": "disc_name"})

df = df.drop(columns=["id"])

#disc stability definition
def stability(turn, fade):
    if pd.isna(turn) or pd.isna(fade):
        return "unknown"
    
    stability_score = turn + fade

    if stability_score >= 1.5:
        return "overstable"
    elif stability_score <= -1.5:
        return "understable"
    else:
        return "neutral"
    
df["stability"] = df.apply(
    lambda x: stability(x["turn"], x["fade"]),
    axis=1
)

#disc type based on speed
def disc_type(speed):
    if pd.isna(speed):
        return "unknown"
    
    if speed <= 4:
        return "putt and approach"
    elif speed <= 6:
        return "mid_range"
    elif speed <= 10:
        return "fairway driver"
    else:
        return "distance driver"
    
df["disc_type"] = df["speed"].apply(disc_type)

#order
column_order = [
    "manufacturer",
    "disc_name",
    "speed",
    "glide",
    "turn",
    "fade",
    "stability",
    "disc_type",
    "discontinued"
]

df = df[column_order]

#export to csv
df.to_csv("disc_catalog.csv", index = False)

#summary
print("\nDone")
print("Count: ", len(df))
print("File saved as disc_catalog.csv")