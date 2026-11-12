from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from .forms import ExcelUploadForm
from .models import Product
from .services import ExcelImportError, import_products


def home(request):
    # آدرس اصلی: همه را به داشبورد می‌فرستد (اگر لاگین نباشد، خودکار به ورود می‌رود)
    return redirect("dashboard")


@login_required  # بدون ورود، کاربر به صفحه‌ی لاگین هدایت می‌شود
def dashboard(request):
    stats = Product.objects.aggregate(total=Sum("quantity"))
    context = {
        "product_count": Product.objects.count(),
        "total_quantity": stats["total"] or 0,
    }
    return render(request, "core/dashboard.html", context)


@login_required
def import_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                created, updated, warnings = import_products(form.cleaned_data["file"])
            except ExcelImportError as e:
                form.add_error("file", str(e))
            else:
                messages.success(
                    request, f"ورود فایل انجام شد: {created} کالای جدید، {updated} بروزرسانی."
                )
                for w in warnings[:10]:
                    messages.warning(request, w)
                return redirect("inventory")
    else:
        form = ExcelUploadForm()
    return render(request, "core/import_excel.html", {"form": form})


@login_required
def inventory(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects.all()
    if q:
        products = products.filter(name__icontains=q) | products.filter(code__icontains=q)
    return render(request, "core/inventory.html", {"products": products, "q": q})
