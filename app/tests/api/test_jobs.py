import json

from django.contrib.gis.geos import Point
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from app.models import Job
from app.util.model_factory import get_company, get_job

fake = Faker()


class JobTestCase(APITestCase):
    def test_create_job(self):
        url = reverse("job-list")

        company = get_company()
        company.save()

        data = {
            "company": company.id,
            "title": fake.company(),
            "description": fake.paragraph(5),
            "city": fake.city(),
            "country": fake.country(),
            "contract_type": "PT",
            "point": {"lat": "foo", "lng": "foo"}
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        job = Job.objects.get(pk=1)
        self.assertEqual(job.company.id, company.id)
        self.assertEqual(job.title, data["title"])
        self.assertEqual(job.description, data["description"])
        self.assertEqual(job.city, data["city"])
        self.assertEqual(job.country, data["country"])
        self.assertEqual(job.contract_type, data["contract_type"])

    def test_list_jobs(self):
        url = reverse("job-list")

        job1 = get_job()
        job2 = get_job()
        job3 = get_job()

        job1.save()
        job2.save()
        job3.save()

        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)
        results = data["results"]

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["company_detail"]["id"], job1.company.id)
        self.assertIn("post_date", results[0])


    def test_jobs_in_radius(self):
        job1 = get_job()
        job2 = get_job()
        job3 = get_job()

        job1.save()
        job2.save()
        job3.save()

    def test_job_details(self):
        job = get_job()
        job.save()

        url = reverse("job-details", kwargs={'pk': job.id})

        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(data["title"], job.title)
        self.assertIn("post_date", data)

