"""منطق خواندن فایل اکسل؛ جدا از view تا خوانا و قابل تست بماند."""
from openpyxl import load_workbook

from .models import Product

# ستون‌های لازم در ردیف اول فایل اکسل
REQUIRED_HEADERS = ["کد کالا", "نام کالا", "موجودی"]


class ExcelImportError(Exception):
    """خطایی که پیامش را مستقیم به کاربر نشان می‌دهیم."""


def import_products(file):
    """فایل اکسل را می‌خواند و کالاها را اضافه یا بروزرسانی می‌کند.

    خروجی: (تعداد جدید، تعداد بروزرسانی‌شده، لیست هشدارها)
    """
    try:
        wb = load_workbook(file, read_only=True, data_only=True)
    except Exception:
        raise ExcelImportError("فایل خوانده نشد. مطمئن شوید فایل xlsx سالم است.")

    rows = wb.active.iter_rows(values_only=True)
    header = next(rows, None)
    if not header:
        raise ExcelImportError("فایل خالی است.")

    header = [str(h).strip() if h is not None else "" for h in header]
    missing = [h for h in REQUIRED_HEADERS if h not in header]
    if missing:
        raise ExcelImportError(
            "ستون‌های لازم پیدا نشد: " + "، ".join(missing)
            + ". ردیف اول فایل باید شامل «کد کالا»، «نام کالا» و «موجودی» باشد."
        )
    idx = {h: header.index(h) for h in REQUIRED_HEADERS}

    created = updated = 0
    warnings = []
    for line, row in enumerate(rows, start=2):
        code, name, qty = (row[idx[h]] for h in REQUIRED_HEADERS)
        if code is None and name is None and qty is None:
            continue  # ردیف خالی
        code = str(code).strip() if code is not None else ""
        if not code or not name:
            warnings.append(f"ردیف {line}: کد یا نام کالا خالی است و رد شد.")
            continue
        try:
            qty = int(float(qty))
        except (TypeError, ValueError):
            warnings.append(f"ردیف {line}: موجودی «{qty}» عدد نیست و رد شد.")
            continue

        _, was_created = Product.objects.update_or_create(
            code=code, defaults={"name": str(name).strip(), "quantity": qty}
        )
        created += was_created
        updated += not was_created
    return created, updated, warnings
