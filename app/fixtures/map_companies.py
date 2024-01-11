from pathlib import Path
import json
from datetime import datetime, timezone

path = Path('raw.json')
contents = path.read_text()
data = json.loads(contents)

companies = []

dt = datetime.now(tz=timezone.utc)
time = dt.strftime("%Y-%m-%dT%H:%M%z")

for job in data:
    companies.append({
        "model": "app.Company",
        "pk": job["id"],
        "fields": {
            "name": job["company"],
            "logo": job["logo"],
            "color": job["logoBackground"],
            "website": job["website"],
            "join_date": time
        }
    })

dump = json.dumps(companies)
dumpPath = Path('companies.json')
dumpPath.write_text(dump)