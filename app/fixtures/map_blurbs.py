import json
from datetime import datetime, timezone
from pathlib import Path

path = Path('raw.json')
contents = path.read_text()
data = json.loads(contents)

dt = datetime.now(timezone.utc)
time = dt.strftime("%Y-%m-%dT%H:%M%z")

blurb_i = 1
blurb_list_i = 1
blurb_list_item_i = 1

blurbs = []

headings = [
    {
        "key": "requirements",
        "title": "Requirements",
        "type": "UL"
    },
    {
        "key": "role",
        "title": "Role",
        "type": "OL"
    }
]

for job in data:
    for heading in headings:
        key = heading["key"]

        blurbs.append({
            "model": "app.Blurb",
            "pk": blurb_i,
            "fields": {
                "job": job["id"],
                "heading": heading["title"],
                "body": job[key]["content"]
            }
        })

        blurbs.append({
            "model": "app.BlurbList",
            "pk": blurb_list_i,
            "fields": {
                "blurb": blurb_i,
                "type": heading["type"],
            }
        })

        blurb_i += 1

        for item in job[key]["items"]:
            blurbs.append({
                "model": "app.BlurbListItem",
                "pk": blurb_list_item_i,
                "fields": {
                    "blurb_list": blurb_list_i,
                    "text": item
                }
            })

            blurb_list_item_i += 1

        blurb_list_i += 1

dump = json.dumps(blurbs)
dumpPath = Path('blurbs.json')
dumpPath.write_text(dump)
