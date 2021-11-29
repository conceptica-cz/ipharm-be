from simple_history.admin import SimpleHistoryAdmin


class BaseHistoryAdmin(SimpleHistoryAdmin):
    """
    Base class for all history admin classes.
    """

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_list_display(self, request):
        default_list_display = ["is_deleted"]
        if self.list_display:
            return list(self.list_display) + default_list_display
        else:
            return default_list_display

    def get_list_filter(self, request):
        default_list_filter = ["is_deleted"]
        if self.list_filter:
            return list(self.list_filter) + default_list_filter
        else:
            return default_list_filter

    def get_exclude(self, request, obj=None):
        default_exclude = ["is_deleted"]
        if self.exclude:
            return list(self.exclude) + default_exclude
        else:
            return default_exclude
