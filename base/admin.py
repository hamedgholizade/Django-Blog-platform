from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    date_hierarchy = "last_update"
    list_per_page = 15
    readonly_fields = ['created_at', 'last_update']

    @admin.action(description="Soft delete selected")
    def soft_delete_admin(modeladmin, request, queryset):
        for obj in queryset:
            obj.soft_delete()
        
    @admin.action(description="Hard delete selected")
    def hard_delete_admin(modeladmin, request, queryset):
        for obj in queryset:
            obj.hard_delete()

    actions = [soft_delete_admin, hard_delete_admin]
