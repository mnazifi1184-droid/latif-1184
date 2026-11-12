from django import forms


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="فایل اکسل (xlsx)")

    def clean_file(self):
        f = self.cleaned_data["file"]
        if not f.name.lower().endswith(".xlsx"):
            raise forms.ValidationError("فقط فایل با پسوند xlsx قابل قبول است.")
        if f.size > 5 * 1024 * 1024:
            raise forms.ValidationError("حجم فایل نباید بیشتر از ۵ مگابایت باشد.")
        return f
