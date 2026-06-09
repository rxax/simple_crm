from django.contrib import admin

from crm.models import Account, Contact, Task, Opportunity

# Register your models here.
admin.site.register(Account)
admin.site.register(Contact)
admin.site.register(Opportunity)
admin.site.register(Task)