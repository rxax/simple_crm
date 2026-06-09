from django.contrib import admin

from crm.models import Account, Contact, Task

# Register your models here.
admin.site.register(Account)
admin.site.register(Contact)
admin.site.register(Task)