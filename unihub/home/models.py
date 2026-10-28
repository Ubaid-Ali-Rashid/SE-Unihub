from django.db import models


# ──────────────────────────────────────────────
# Standalone / Root Entities
# ──────────────────────────────────────────────

class Department(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    hod_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name or ""


class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    kind = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name or ""


class ChecklistItem(models.Model):
    list_type = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title or ""


class Society(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    how_to_join = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Societies"

    def __str__(self):
        return self.name or ""


# ──────────────────────────────────────────────
# Entities with FK → Department
# ──────────────────────────────────────────────

class User(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    batch_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name or ""


class Location(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    directions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name or ""


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


# ──────────────────────────────────────────────
# Entities with FK → Category (and Department)
# ──────────────────────────────────────────────

class Guideline(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title or ""


class Deadline(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title or ""


class FAQ(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=500, null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question or ""


# ──────────────────────────────────────────────
# Entities with FK → User
# ──────────────────────────────────────────────

class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title or ""


class UserChecklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE, null=True, blank=True)
    is_done = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.item}"


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title or ""


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"Answer to: {self.question}"


# ──────────────────────────────────────────────
# Entities with FK → Location / Society
# ──────────────────────────────────────────────

class Faculty(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    office = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return self.name or ""


class Event(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    starts_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title or ""

# ──────────────────────────────────────────────
# Front Page Configuration Model
# ──────────────────────────────────────────────

class Home(models.Model):
    # Meta / Page Settings
    page_title = models.CharField(max_length=255, default="UniHub - Freshman Student Portal", null=True, blank=True)
    
    # Navigation Bar
    nav_logo = models.CharField(max_length=255, default="", null=True, blank=True)
    nav_heading = models.CharField(max_length=255, default="UniHub", null=True, blank=True)
    nav_home = models.CharField(max_length=100, default="Home", null=True, blank=True)
    nav_about = models.CharField(max_length=100, default="About", null=True, blank=True)
    nav_departments = models.CharField(max_length=100, default="Departments", null=True, blank=True)
    nav_guidelines = models.CharField(max_length=100, default="Guidelines", null=True, blank=True)
    nav_courses = models.CharField(max_length=100, default="Courses", null=True, blank=True)
    nav_societies = models.CharField(max_length=100, default="Societies", null=True, blank=True)
    nav_events = models.CharField(max_length=100, default="Events", null=True, blank=True)
    nav_faqs = models.CharField(max_length=100, default="FAQs", null=True, blank=True)
    nav_qa = models.CharField(max_length=100, default="Q&A Forum", null=True, blank=True)
    nav_checklist = models.CharField(max_length=100, default="Checklist", null=True, blank=True)
    nav_button_text = models.CharField(max_length=100, default="Join UniHub", null=True, blank=True)
    nav_button_url = models.CharField(max_length=255, default="#", null=True, blank=True)

    # Hero / Description Section
    desc_heading = models.CharField(max_length=255, default="Welcome to UniHub", null=True, blank=True)
    description = models.TextField(default="UniHub exists to guide freshers from day one. It replaces the senior you don't have yet — giving you instant access to department locations, faculty rooms, academic guidelines, deadlines, courses, societies, and a moderated Q&A forum.", null=True, blank=True)
    hero_image = models.CharField(max_length=255, default="", null=True, blank=True)
    hero_video_url = models.CharField(max_length=255, default="", null=True, blank=True)
    hero_button_text = models.CharField(max_length=100, default="Explore Campus", null=True, blank=True)
    hero_button_url = models.CharField(max_length=255, default="#features", null=True, blank=True)
    secondary_button_text = models.CharField(max_length=100, default="Browse FAQs", null=True, blank=True)
    secondary_button_url = models.CharField(max_length=255, default="#faqs", null=True, blank=True)

    # Announcement Banner
    announcement = models.TextField(default="Welcome Class of 2026! Orientation session begins this week. Please check your department guidelines.", null=True, blank=True)
    show_announcement = models.BooleanField(default=True, null=True, blank=True)

    # Services / Features Section
    features_heading = models.CharField(max_length=255, default="Features & Services", null=True, blank=True)
    features_description = models.TextField(default="Discover all tools tailored to make your university transition smooth and stress-free.", null=True, blank=True)
    feature1_title = models.CharField(max_length=255, default="Campus Locations", null=True, blank=True)
    feature1_desc = models.TextField(default="Easily locate departments, faculty offices, and classroom floors.", null=True, blank=True)
    feature2_title = models.CharField(max_length=255, default="Guidelines & Rules", null=True, blank=True)
    feature2_desc = models.TextField(default="Read department-specific regulations, exam policies, and guidelines.", null=True, blank=True)
    feature3_title = models.CharField(max_length=255, default="Community Q&A", null=True, blank=True)
    feature3_desc = models.TextField(default="Ask questions and receive reliable answers moderated by faculty.", null=True, blank=True)
    feature4_title = models.CharField(max_length=255, default="Fresher Checklist", null=True, blank=True)
    feature4_desc = models.TextField(default="Follow your personal checklist to complete all essential tasks on time.", null=True, blank=True)

    # Events / Societies Section
    event_heading = models.CharField(max_length=255, default="Societies & Events", null=True, blank=True)
    event_description = models.TextField(default="Connect with student societies, explore workshops, and participate in campus activities.", null=True, blank=True)
    event_button_text = models.CharField(max_length=100, default="View All Events", null=True, blank=True)

    # FAQs Section
    faq_heading = models.CharField(max_length=255, default="Frequently Asked Questions", null=True, blank=True)
    faq_description = models.TextField(default="Got questions? Find immediate answers to what freshers ask the most.", null=True, blank=True)

    # Subscribe / Newsletter Section
    subscribe_heading = models.CharField(max_length=255, default="Stay Connected With UniHub", null=True, blank=True)
    subscribe_subheading = models.CharField(max_length=255, default="Get alerts for upcoming deadlines, society events, and important university notices.", null=True, blank=True)
    subscribe_button = models.CharField(max_length=100, default="Subscribe Now", null=True, blank=True)

    # Footer
    footer_text = models.CharField(max_length=255, default="UniHub — Designed for University Freshers", null=True, blank=True)
    footer_description = models.TextField(default="A student software engineering initiative built to help every fresher navigate campus life with clarity and confidence.", null=True, blank=True)

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"

    def __str__(self):
        return f"Home Page Configuration ({self.desc_heading or 'Default'})"
