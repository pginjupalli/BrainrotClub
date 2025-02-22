from django.contrib import admin

from . import models

# Register your models here.
for model in models:
    admin.site.register(model)
