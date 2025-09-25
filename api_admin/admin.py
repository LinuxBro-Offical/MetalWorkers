from django.contrib import admin
from .models import Lead, Service, Newsletter, SiteVisitor

# Register your models here.
admin.site.register(Lead)
admin.site.register(Service)
admin.site.register(Newsletter)
admin.site.register(SiteVisitor)
