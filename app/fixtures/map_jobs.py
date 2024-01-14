import json
from datetime import datetime, timezone
from pathlib import Path

from app.fixtures.fixture_util import get_html_description
from app.util.geocoder import coordinates_from_city_country

CONTRACT_TYPES = [
    ("FT", "Full Time"),
    ("PT", "Part Time"),
    ("CO", "Contract"),
    ("FR", "Freelance"),
]


def get_contract_type(long):
    for contract_type in CONTRACT_TYPES:
        if contract_type[1].lower() == long.lower():
            return contract_type[0]


def run_mapping():
    path = Path(__file__).parent / 'raw.json'
    contents = path.read_text()
    data = json.loads(contents)

    jobs = []

    dt = datetime.now(timezone.utc)
    time = dt.strftime("%Y-%m-%dT%H:%M%z")

    for job in data:
        coords = coordinates_from_city_country(job["city"], job["country"])
        jobs.append({
            "model": "app.Job",
            "pk": job["id"],
            "fields": {
                "company": job["id"],
                "title": job["position"],
                "contract_type": get_contract_type(job["contract"]),
                "description": get_html_description(job),
                "city": job["city"],
                "country": job["country"],
                "point": f'POINT ({coords[1]} {coords[0]})',
                "post_date": time
            }
        })

    dump = json.dumps(jobs)
    dump_path = Path(__file__).parent / 'jobs.json'
    dump_path.write_text(dump)
