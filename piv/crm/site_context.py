from crm.models import Company
from django.contrib.sessions.backends.db import SessionStore

"""
Site Context for current company, selected/active company"""

def site_context(request):
    user = request.user
    user_companies = Company.objects.filter(owner__exact=user.pk)
    if not request.session.get('active_company'):
        request.session['active_company'] = ''
    return {
        'user_companies': user_companies,
        'active_company': request.session['active_company']
    }
