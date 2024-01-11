import json
from datetime import datetime, timezone
from pathlib import Path

CONTRACT_TYPES = [
    ("FT", "Full Time"),
    ("PT", "Part Time"),
    ("CO", "Contract"),
    ("FR", "Freelance"),
]

path = Path('raw.json')
contents = path.read_text()
data = json.loads(contents)

jobs = []

dt = datetime.now(timezone.utc)
time = dt.strftime("%Y-%m-%dT%H:%M%z")


def get_contract_type(long):
    for contract_type in CONTRACT_TYPES:
        if contract_type[1].lower() == long.lower():
            return contract_type[0]


for job in data:
    jobs.append({
        "model": "app.Job",
        "pk": job["id"],
        "fields": {
            "company": job["id"],
            "title": job["position"],
            "contract_type": get_contract_type(job["contract"]),
            "description": job["description"],
            "location": job["location"],
            "post_date": time
        }
    })

dump = json.dumps(jobs)
dumpPath = Path('jobs.json')
dumpPath.write_text(dump)
