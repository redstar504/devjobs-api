import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from app.models import Company
from app.util.model_factory import get_company


class CompanyTestCase(APITestCase):
    def test_create_company(self):
        url = reverse("company-list")

        data = {
            "name": "ABC Widgets",
            "logo": "foo.jpg",
            "color": "blue",
            "website": "https://foo.example",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        company = Company.objects.get(pk=1)
        self.assertEqual(company.name, data["name"])
        self.assertEqual(company.logo, data["logo"])
        self.assertEqual(company.color, data["color"])
        self.assertEqual(company.website, data["website"])

    def test_view_company(self):
        company = get_company()
        company.save()

        url = reverse("company-detail", kwargs={"pk": company.id})

        response = self.client.get(url, format="json")
        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(data["name"], company.name)
        self.assertEqual(data["logo"], company.logo)
        self.assertEqual(data["color"], company.color)
        self.assertEqual(data["website"], company.website)
