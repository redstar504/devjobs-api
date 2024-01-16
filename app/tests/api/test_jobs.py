import json

from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from app.logger import logger
from app.models import Job
from app.util.fake_points import *
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
        content = response.content.decode("utf-8")
        data = json.loads(content)

        job = Job.objects.get(pk=data["id"])
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
        self.assertEqual(results[0]["id"], job1.id, "Job ID should match")
        self.assertEqual(results[0]["company_detail"]["id"], job1.company.id)
        self.assertIn("post_date", results[0])

    def test_job_details(self):
        job = get_job()
        job.save()

        url = reverse("job-details", kwargs={'pk': job.id})

        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(data["title"], job.title)
        self.assertIn("post_date", data)


class JobSearchTestCase(APITestCase):
    def test_search_full_time_jobs(self):
        url = f'{reverse("job-list")}?fullTimeOnly=true'

        job1 = get_job(contract_type=Job.FULL_TIME)
        job2 = get_job(contract_type=Job.FULL_TIME)
        job3 = get_job(contract_type=Job.FULL_TIME)
        job4 = get_job(contract_type=Job.CONTRACT)
        job5 = get_job(contract_type=Job.PART_TIME)

        job1.save()
        job2.save()
        job3.save()
        job4.save()
        job5.save()

        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        # Should only be 3 full time jobs returned
        self.assertEqual(3, data["count"])

    def test_search_by_place_id_in_radius(self):
        get_job(point=point_of_munich()).save()
        get_job(point=point_of_munich()).save()
        get_job(point=point_of_munich()).save()

        get_job(point=point_of_moscow()).save()
        get_job(point=point_of_moscow()).save()
        get_job(point=point_of_moscow()).save()
        get_job(point=point_of_moscow()).save()
        get_job(point=point_of_moscow()).save()

        url = f'{reverse("job-list")}?placeId={place_id_of_moscow()}&radius=1000'
        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(5, data["count"], 'Five jobs saved that are located in Moscow')

    def test_search_by_coordinates_in_radius(self):
        get_job(point=point_of_vancouver()).save()  # 253km from kamloops
        get_job(point=point_of_vancouver()).save()

        get_job(point=point_of_calgary()).save()  # 442 km from kamloops
        get_job(point=point_of_calgary()).save()

        get_job(point=point_of_moscow()).save()
        get_job(point=point_of_moscow()).save()

        sample_coords = coords_of_kamloops()

        url = f'{reverse("job-list")}?lng={sample_coords[0]}&lat={sample_coords[1]}&radius=1000'
        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(4, data["count"], 'Four jobs within 1000km of Kamloops')

        url = f'{reverse("job-list")}?lng={sample_coords[0]}&lat={sample_coords[1]}&radius=300'
        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(2, data["count"], 'Vancouver is within 300km of Kamloops')

    def test_search_job_keywords(self):
        get_job(title="Senior Software Engineer").save()
        get_job(title="Haskell and PureScript Dev").save()
        get_job(title="Midlevel Back End ENGINEER").save()  # Uppercase variant

        get_job(title="Senior Application Dev").save()
        get_job(title="Remote DevOps EnginEering").save()  # Note the suffix "ing"
        get_job(title="Desktop Support Manager").save()
        get_job(title="iOS Engineer").save()
        get_job(title="Senior EJB Developer").save()

        get_job(description="foo bar baz engineer blah blah").save()  # job description keyword inclusion

        url = f'{reverse("job-list")}?keywords=Engineering'
        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(5, data["count"], 'Five jobs mentioning engineering')

    def test_search_job_location_query(self):
        get_job(city="Eagleton").save()
        get_job(city="Eagletown").save()
        get_job(city="North Eagleton").save()
        get_job(country="Eagles").save()

        get_job(city="foo", country="bar").save()
        get_job(city="foo", country="bar").save()
        get_job(city="foo", country="bar").save()
        get_job(city="foo", country="bar").save()

        url = f'{reverse("job-list")}?locationQuery=eagle'
        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(4, data["count"], 'Four jobs with eagle locations')

    def test_search_job_location_query_portland(self):
        get_job(city="Portland", contract_type="PT").save()

        get_job(city="foo", country="bar").save()
        get_job(city="foo", country="bar").save()
        get_job(city="foo", country="bar").save()
        get_job(city="foo", country="bar").save()

        url = f'{reverse("job-list")}?locationQuery=Portland&fullTimeOnly=false'
        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(1, data["count"], 'One job in Portland')
