from django.db import models
from django.contrib.gis.db.models import PointField


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    join_date = models.DateTimeField(auto_now_add=True)


class Job(models.Model):
    CONTRACT_TYPES = [
        ("FT", "Full Time"),
        ("PT", "Part Time"),
        ("CO", "Contract"),
        ("FR", "Freelance"),
    ]

    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    contract_type = models.CharField(choices=CONTRACT_TYPES, max_length=60)
    point = PointField()
    post_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
