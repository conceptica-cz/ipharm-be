from django.contrib import admin

from . import models, tasks


@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ["name"]
    actions = ["update"]

    @admin.action(description="Update from external API")
    def update(self, request, queryset):
        for source in queryset:
            tasks.update.delay(source.name, full_update=True)


class ModelUpdateInline(admin.TabularInline):
    model = models.ModelUpdate
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = [
        "source",
        "update_type",
        "started_at",
        "finished_at",
        "url_parameters",
    ]
    list_filter = ["source"]
    inlines = [ModelUpdateInline]


@admin.register(models.ModelUpdate)
class ModelUpdateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created",
        "updated",
        "not_changed",
    ]
    list_filter = ["name"]
