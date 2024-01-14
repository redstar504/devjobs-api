from django.test import TransactionTestCase

from app.logger import logger
from app.util.fake_points import *
from app.util.geography import km_between_points, km_between_place_and_point


class DistanceTestCase(TransactionTestCase):
    def test_km_between_points(self):
        munich = point_of_munich()
        moscow = point_of_moscow()
        self.assertEqual(2700, km_between_points(munich, moscow))

    def test_km_between_place_id_and_point(self):
        moscow_place = place_id_of_moscow()
        munich_point = point_of_munich()
        self.assertEqual(2700, km_between_place_and_point(moscow_place, munich_point))
