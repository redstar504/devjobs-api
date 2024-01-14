import json
from datetime import datetime, timezone
from pathlib import Path
from random import choice


def run_mapping():
    path = Path(__file__).parent / 'raw.json'
    contents = path.read_text()
    data = json.loads(contents)

    companies = []

    dt = datetime.now(tz=timezone.utc)
    time = dt.strftime("%Y-%m-%dT%H:%M%z")

    def get_fake_company_domain(job):
        return job["company"].lower().replace(' ', '') + choice(['.com', '.net', '.org', '.info'])

    for job in data:
        companies.append({
            "model": "app.Company",
            "pk": job["id"],
            "fields": {
                "name": job["company"],
                "logo": job["logo"],
                "color": job["logoBackground"],
                "website": f"https://{get_fake_company_domain(job)}",
                "join_date": time
            }
        })

    dump = json.dumps(companies)
    dump_path = Path(__file__).parent / 'companies.json'
    dump_path.write_text(dump)
