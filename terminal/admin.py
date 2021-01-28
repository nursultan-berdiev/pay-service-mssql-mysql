from django.contrib import admin
from .models import PayService, Customers, CheckService

admin.site.register(PayService)
admin.site.register(Customers)
admin.site.register(CheckService)

