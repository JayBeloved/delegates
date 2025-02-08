from django.contrib import admin
from .models import Delegate, Payment, Committee, Assignment
from django.apps import apps

admin.site.register(Delegate)
admin.site.register(Payment)
admin.site.register(Committee)
admin.site.register(Assignment)