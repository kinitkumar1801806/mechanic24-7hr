from django.contrib import admin
from .models import User_Accounts,Mechanic_Accounts,Contact
# Register your models here.
admin.site.register(User_Accounts)
admin.site.register(Mechanic_Accounts)
admin.site.register(Contact)