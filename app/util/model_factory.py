from faker import Faker

from app.models import Company, Job

fake = Faker()


def get_company():
    data = {
        "name": fake.name(),
        "logo": fake.file_name(category="image"),
        "color": fake.color(),
        "website": fake.url()
    }

    return Company(**data)


def get_job():
    company = get_company()
    company.save()

    data = {
        "company": company,
        "title": fake.bs(),
        "description": fake.paragraph(),
        "location": fake.city(),
        "contract_type": Job.CONTRACT_TYPES[0][0],
    }

    return Job(**data)
