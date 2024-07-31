from django.apps import AppConfig
from suit.apps import DjangoSuitConfig



class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # def ready(self):
    #     import accounts.models

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal' # 'vertical' ,'horizontal' 
