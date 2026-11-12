from django.shortcuts import render


def home(request):
    # view: درخواست (request) را می‌گیرد و پاسخ (response) برمی‌گرداند
    context = {"name": "مجید"}
    return render(request, "core/home.html", context)
