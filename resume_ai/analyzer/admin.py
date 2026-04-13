from django.contrib import admin
from .models import Resume, ExtarctedData, Job, MatchResult


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at')
    search_fields = ('file',)
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)


@admin.register(ExtarctedData)
class ExtractedDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'resume', 'skills_preview', 'experience_preview')
    search_fields = ('skills', 'experience', 'education')
    list_filter = ('resume__uploaded_at',)
    
    def skills_preview(self, obj):
        """Show preview of skills."""
        return obj.skills[:50] + '...' if len(obj.skills) > 50 else obj.skills
    skills_preview.short_description = 'Skills'
    
    def experience_preview(self, obj):
        """Show preview of experience."""
        return obj.experience[:50] + '...' if len(obj.experience) > 50 else obj.experience
    experience_preview.short_description = 'Experience'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'skills_preview')
    search_fields = ('title', 'description', 'required_skills')
    list_filter = ('title',)
    
    def skills_preview(self, obj):
        """Show preview of required skills."""
        return obj.required_skills[:50] + '...' if len(obj.required_skills) > 50 else obj.required_skills
    skills_preview.short_description = 'Required Skills'


@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'resume', 'job', 'score')
    search_fields = ('resume__file', 'job__title')
    list_filter = ('score', 'resume__uploaded_at')
    readonly_fields = ('resume', 'job', 'score')
