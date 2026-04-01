from django.contrib import admin

from apps.radiology.models import Modality


@admin.register(Modality)
class ModalityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

