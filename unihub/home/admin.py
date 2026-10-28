from django.contrib import admin
from .models import (
    Department, Category, ChecklistItem, Society,
    User, Location, Course,
    Guideline, Deadline, FAQ,
    Announcement, UserChecklist, Question, Answer,
    Faculty, Event, Home,
)

admin.site.register(Department)
admin.site.register(Category)
admin.site.register(ChecklistItem)
admin.site.register(Society)
admin.site.register(User)
admin.site.register(Location)
admin.site.register(Course)
admin.site.register(Guideline)
admin.site.register(Deadline)
admin.site.register(FAQ)
admin.site.register(Announcement)
admin.site.register(UserChecklist)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Faculty)
admin.site.register(Event)


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('desc_heading', 'nav_heading', 'show_announcement')
    fieldsets = (
        ('General Page Settings', {
            'fields': ('page_title', 'desc_heading', 'description', 'hero_image', 'hero_video_url', 'hero_button_text', 'hero_button_url', 'secondary_button_text', 'secondary_button_url')
        }),
        ('Navigation Bar', {
            'fields': ('nav_heading', 'nav_logo', 'nav_home', 'nav_about', 'nav_departments', 'nav_guidelines', 'nav_courses', 'nav_societies', 'nav_events', 'nav_faqs', 'nav_qa', 'nav_checklist', 'nav_button_text', 'nav_button_url')
        }),
        ('Announcement Banner', {
            'fields': ('show_announcement', 'announcement')
        }),
        ('Features & Services Section', {
            'fields': ('features_heading', 'features_description', 'feature1_title', 'feature1_desc', 'feature2_title', 'feature2_desc', 'feature3_title', 'feature3_desc', 'feature4_title', 'feature4_desc')
        }),
        ('Societies & Events Section', {
            'fields': ('event_heading', 'event_description', 'event_button_text')
        }),
        ('FAQs Section', {
            'fields': ('faq_heading', 'faq_description')
        }),
        ('Subscribe Section', {
            'fields': ('subscribe_heading', 'subscribe_subheading', 'subscribe_button')
        }),
        ('Footer', {
            'fields': ('footer_text', 'footer_description')
        }),
    )
