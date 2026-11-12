# مدیریت موجودی (Django)

## اجرا روی کامپیوتر خودتان
```bash
python -m venv .venv
source .venv/bin/activate        # ویندوز: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser # ساخت کاربر ورود
python manage.py runserver
```
بعد آدرس http://127.0.0.1:8000 را باز کنید.

## فایل اکسل
ردیف اول باید شامل «کد کالا»، «نام کالا» و «موجودی» باشد. نمونه: `sample/inventory_sample.xlsx`

## تست
```bash
python manage.py test
```
