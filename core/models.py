from django.db import models


class Product(models.Model):
    """هر ردیف جدول = یک کالا در انبار."""

    code = models.CharField("کد کالا", max_length=50, unique=True)
    name = models.CharField("نام کالا", max_length=200)
    quantity = models.IntegerField("موجودی", default=0)
    updated_at = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "کالا"
        verbose_name_plural = "کالاها"

    def __str__(self):
        return f"{self.code} - {self.name}"
