from django.contrib import admin

from . import models, tasks


@admin.register(models.Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ["model", "name"]
    actions = ["update"]

    @admin.action(description="Update from external API")
    def update(self, request, queryset):
        for reference in queryset:
            tasks.update.delay(reference.model)


@admin.register(models.ReferenceUpdate)
class ReferenceUpdateAdmin(admin.ModelAdmin):
    list_display = [
        "reference",
        "started_at",
        "finished_at",
        "created",
        "updated",
        "not_changed",
    ]
    list_filter = ["reference"]
