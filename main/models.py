import uuid

from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(
        max_length=255,
        help_text="Comma-separated list of technologies used, e.g. 'Django, PostgreSQL, React'",
    )
    link = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def tech_stack_list(self):
        return [tech.strip() for tech in self.tech_stack.split(",") if tech.strip()]


class Education(models.Model):
    LEVEL_CHOICES = [
        ("elementary", "Elementary School"),
        ("junior_high", "Junior High School"),
        ("senior_high", "Senior High School"),
        ("diploma", "Diploma"),
        ("bachelor", "Bachelor's Degree"),
        ("master", "Master's Degree"),
        ("doctorate", "Doctorate"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution_name = models.CharField(max_length=255)
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="bachelor",
    )
    field_of_study = models.CharField(max_length=255, blank=True, null=True)
    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="e.g. 3.75",
    )
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_year"]

    def __str__(self):
        return f"{self.institution_name} - {self.get_level_display()}"

    @property
    def is_ongoing(self):
        return self.end_year is None
