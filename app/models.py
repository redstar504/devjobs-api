from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    join_date = models.DateTimeField(auto_now_add=True)


class JobManager(models.Manager):
    def create_job(self, **kwargs):
        job = Job(**kwargs)
        job.point = Point(119, 49)
        job.save()

        return job


class Job(models.Model):
    FULL_TIME = "FT"
    PART_TIME = "PT"
    CONTRACT = "CO"
    FREELANCE = "FR"

    CONTRACT_TYPES = [
        (FULL_TIME, "Full Time"),
        (PART_TIME, "Part Time"),
        (CONTRACT, "Contract"),
        (FREELANCE, "Freelance"),
    ]

    objects = JobManager()

    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    contract_type = models.CharField(choices=CONTRACT_TYPES, max_length=60)
    point = PointField(geography=True)
    post_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']