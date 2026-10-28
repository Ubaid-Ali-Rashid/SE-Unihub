from django.shortcuts import render
from .models import (
    Home, Event, Society, Announcement, FAQ,
    Department, Guideline, Deadline
)


def home_view(request):
    """
    Renders the front page of UniHub.
    Fetches all customizable content from the Home model.
    Only sections that have actual records in the database will be displayed.
    """
    home_obj = Home.objects.first()
    if not home_obj:
        home_obj = Home.objects.create()

    events = Event.objects.select_related('society', 'location').all()
    societies = Society.objects.all()
    announcements = Announcement.objects.select_related('author', 'department').all().order_by('-published_at')
    faqs = FAQ.objects.select_related('category').all()
    departments = Department.objects.all()
    guidelines = Guideline.objects.select_related('category', 'department').all()
    deadlines = Deadline.objects.select_related('category', 'department').all().order_by('due_date')

    context = {
        'home': home_obj,
        'events': events,
        'events_count': events.count(),
        'societies': societies,
        'societies_count': societies.count(),
        'announcements': announcements,
        'announcements_count': announcements.count(),
        'faqs': faqs,
        'faqs_count': faqs.count(),
        'departments': departments,
        'departments_count': departments.count(),
        'guidelines': guidelines,
        'guidelines_count': guidelines.count(),
        'deadlines': deadlines,
        'deadlines_count': deadlines.count(),
    }
    return render(request, 'index.html', context)
