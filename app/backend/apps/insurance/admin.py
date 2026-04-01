from django.contrib import admin

from apps.insurance.models import InsurancePlan


@admin.register(InsurancePlan)
class InsurancePlanAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

