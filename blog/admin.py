from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from base.admin import BaseAdmin
from blog.models.user import User
from blog.models.post import Post
from blog.models.comment import Comment


class CustomUserAdmin(UserAdmin, BaseAdmin):
    # Fields to be displayed in edit form for existing user
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'user_role')}),
    )

    # Fields to be displayed in the add user form for new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'user_role', 'password1', 'password2'),}),
    )

    list_display = (
        "username", 
        "email", 
        "first_name", 
        "last_name", 
        "phone",
        "user_role",
        "is_staff" )
    
    list_filter = (
        "is_staff", 
        "is_superuser", 
        "is_active", 
        "groups",
        "user_role")

class  PostAdmin(BaseAdmin):
    list_display = [
        'id',
        'title',
        'author__username',
        'status',
        'like_count',
        'visit_count',
        'published_date'
    ]
    list_display_links = [
        'id', 'title'
    ]
    list_filter = [
        'status', 'author__username', 'tag'
    ]
    ordering = ['-created_at']

class ConfirmationStatusFilter(admin.SimpleListFilter):
    # A custom confirmation filter based on is_shown property of comment model
    title = 'confirmation status'
    parameter_name = 'is_shown'

    def lookups(self, request, model_admin):
        return(
            ('confirmed', 'Confirmed'),
            ('not_confirmed', 'Not Confirmed'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'confirmed':
            return queryset.filter(is_shown=True)
        if self.value() == 'not_confirmed':
            return queryset.filter(is_shown=False)
        return queryset

class CommentAdmin(BaseAdmin):
    list_display = [
        'id',
        'post__title',
        'user__username',
        'text',
        'is_shown'
    ]
    list_display_links = [
    'id', 'post__title'
    ]
    list_filter = [
        ConfirmationStatusFilter,
        'user__username'
    ]
    ordering = ['-created_at']

    @admin.action(description='Confirm the selected comments')
    def make_confirmed(self, request, queryset):
        confirmed_count = queryset.update(is_shown=True)
        self.message_user(
            request,
            f"{confirmed_count} comment(s) confirmed.")

    @admin.action(description='Undo the confirmation of the selected comments')
    def make_not_confirmed(self, request, queryset):
        unconfirmed_count = queryset.update(is_shown=False)
        self.message_user(
            request,
            f"{unconfirmed_count} comment(s) disconfirmed.")
    
    actions = BaseAdmin.actions + ['make_confirmed', 'make_not_confirmed']        


admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
