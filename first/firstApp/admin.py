from django.contrib import admin

from .models import PortfolioProfile, Qualification


@admin.register(PortfolioProfile)
class PortfolioProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'updated_at')
    fieldsets = (
        ('Profile', {'fields': ('full_name', 'headline', 'bio')}),
        ('Contact', {'fields': ('email', 'phone', 'location', 'github_url', 'linkedin_url')}),
        ('Resume', {'fields': ('resume',)}),
    )

    def has_add_permission(self, request):
        return not PortfolioProfile.objects.exists()


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = (
        'qualification',
        'institution',
        'status',
        'marks_or_grade',
        'end_year',
        'display_order',
    )
    list_filter = ('status',)
    search_fields = ('qualification', 'institution', 'field_of_study')
    ordering = ('display_order', '-end_year')
