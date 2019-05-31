from django.contrib import admin
from certificate.models import Cert

# Register your models here.


@admin.register(Cert)
class CertAdmin(admin.ModelAdmin):
    fields = ('cert_id', 'user_name', 'user_id', 'issue_date', 'program')
    list_display = ('cert_id', 'user_name', 'user_id', 'issue_date', 'program', 'created')
    search_fields = ('cert_id', 'user_name', 'user_id', 'program')
    ordering = ('-issue_date',)
    list_per_page = 20