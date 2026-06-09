from django.contrib import admin

from invoice.models import Subscription, Invoice, Payment

# Register your models here.
admin.site.register(Subscription)
admin.site.register(Invoice)
admin.site.register(Payment)
