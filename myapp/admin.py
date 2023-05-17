from django.contrib import admin
from .models import Post


from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_creator')
    list_display_links = ('title',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Apply CSRF protection to any user input used in the display fields
        # For example, sanitize user input or escape HTML tags
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Apply CSRF protection when interacting with related models
        # For example, validate the selected foreign key against the user's permissions
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Apply CSRF protection when interacting with related models
        # For example, validate the selected many-to-many relation against the user's permissions
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    