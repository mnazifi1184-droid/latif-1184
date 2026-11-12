from io import BytesIO

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from openpyxl import Workbook

from .models import Product


def make_xlsx(rows):
    wb = Workbook()
    for r in rows:
        wb.active.append(r)
    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    buf.name = "test.xlsx"
    return buf


class AuthTests(TestCase):
    def test_dashboard_requires_login(self):
        r = self.client.get(reverse("dashboard"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login/", r["Location"])

    def test_login_redirects_to_dashboard(self):
        User.objects.create_user("ali", password="pass12345")
        r = self.client.post(reverse("login"), {"username": "ali", "password": "pass12345"})
        self.assertRedirects(r, reverse("dashboard"))

    def test_wrong_password(self):
        User.objects.create_user("ali", password="pass12345")
        r = self.client.post(reverse("login"), {"username": "ali", "password": "bad"})
        self.assertContains(r, "اشتباه است")


class ImportTests(TestCase):
    def setUp(self):
        User.objects.create_user("ali", password="pass12345")
        self.client.login(username="ali", password="pass12345")

    def upload(self, rows):
        return self.client.post(reverse("import_excel"), {"file": make_xlsx(rows)})

    def test_import_creates_and_updates(self):
        header = ["کد کالا", "نام کالا", "موجودی"]
        self.upload([header, ["A1", "قلم", 10]])
        self.assertEqual(Product.objects.get(code="A1").quantity, 10)
        self.upload([header, ["A1", "قلم", 25]])
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get(code="A1").quantity, 25)

    def test_missing_columns(self):
        r = self.upload([["x", "y"], [1, 2]])
        self.assertContains(r, "ستون‌های لازم")
        self.assertEqual(Product.objects.count(), 0)

    def test_bad_quantity_skipped(self):
        self.upload([["کد کالا", "نام کالا", "موجودی"], ["A1", "قلم", "abc"]])
        self.assertEqual(Product.objects.count(), 0)
