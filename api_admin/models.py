from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api_admin'
        db_table = 'service' # Explicitly set table name to match SQLModel


class Lead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        app_label = 'api_admin'
        db_table = 'lead' # Explicitly set table name to match SQLModel


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'api_admin'
        db_table = 'newsletter' # Explicitly set table name to match SQLModel


class SiteVisitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} at {self.timestamp}"

    class Meta:
        app_label = 'api_admin'
        db_table = 'sitevisitor' # Explicitly set table name to match SQLModel
