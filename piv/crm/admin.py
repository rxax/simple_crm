from django.contrib import admin

from crm.models import Account, Contact, Task, Opportunity, Company, UserProfile

# Register your models here.
admin.site.register(Company)
admin.site.register(Account)
admin.site.register(Contact)
admin.site.register(Opportunity)
admin.site.register(Task)
admin.site.register(UserProfile)