from django.contrib import admin
from .models import *



@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(FormChoice)
class FormChoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(SetPrinterDatabaseFields)
class PrintoutParameterFields(admin.ModelAdmin):
    pass