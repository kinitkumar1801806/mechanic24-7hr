from django.contrib import admin

# Register your models here.
from .models import Products, Contact, Orders,OrderUpdate,Payment_history

admin.site.register(Products)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(Payment_history)