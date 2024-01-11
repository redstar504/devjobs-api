import json

from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from app.models import Job, Blurb, BlurbList, BlurbListItem
from app.util.model_factory import get_company, get_job

fake = Faker()


class CompanyTestCase(APITestCase):
    def test_create_job(self):
        url = reverse("job-list")

        company = get_company()
        company.save()

        data = {
            "company": company.id,
            "title": fake.company(),
            "description": fake.paragraph(5),
            "location": fake.city(),
            "contract_type": "PT",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        job = Job.objects.get(pk=1)
        self.assertEqual(job.company.id, company.id)
        self.assertEqual(job.title, data["title"])
        self.assertEqual(job.description, data["description"])
        self.assertEqual(job.location, data["location"])
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

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["company_detail"]["id"], job1.company.id)

    def test_job_details(self):
        job = get_job()
        job.save()

        blurb = Blurb(job=job)
        blurb.heading = fake.bs()
        blurb.body = fake.paragraph()
        blurb.save()

        blurb_list = BlurbList()
        blurb_list.type = "OL"
        blurb_list.blurb = blurb
        blurb_list.save()

        blurb_list_item = BlurbListItem()
        blurb_list_item.text = fake.paragraph(nb_sentences=1)
        blurb_list_item.blurb_list = blurb_list
        blurb_list_item.save()

        blurb_list_item1 = BlurbListItem()
        blurb_list_item1.text = fake.paragraph(nb_sentences=2)
        blurb_list_item1.blurb_list = blurb_list
        blurb_list_item1.save()

        blurb_list_item2 = BlurbListItem()
        blurb_list_item2.text = fake.paragraph(nb_sentences=1)
        blurb_list_item2.blurb_list = blurb_list
        blurb_list_item2.save()

        blurb_list_item3 = BlurbListItem()
        blurb_list_item3.text = fake.paragraph(nb_sentences=2)
        blurb_list_item3.blurb_list = blurb_list
        blurb_list_item3.save()

        url = reverse("job-details", kwargs={'pk': job.id})

        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(data["title"], job.title)
        self.assertEqual(len(data["blurbs"]), 1)
        self.assertEqual(len(data["blurbs"][0]["lists"]), 1)
        self.assertEqual(len(data["blurbs"][0]["lists"][0]["items"]), 4)
