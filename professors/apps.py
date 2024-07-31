from django.apps import AppConfig

class ProfessorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'professors'

    # def ready(self):
    #     import professors.signals  # تأكد من استيراد ملف signals هنا
