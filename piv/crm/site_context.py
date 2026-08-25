from crm.models import Company
"""
Site Context for current company, selected/active company"""

def site_context(request):
    user = request.user
    user_companies = Company.objects.filter(owner__exact=user.pk)
    return {'user_companies': user_companies }
