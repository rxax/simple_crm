from django.conf import settings
from django.db import models
from tinymce.models import HTMLField

"""
Basic CRM: Account, Contact, Opportunity, Activity, Task
"""

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


def default_currency():
    currency, _ = Currency.objects.get_or_create(code="EUR", defaults={"name": "Euro"})
    return currency.pk


class Company(models.Model):
    class Meta:
        verbose_name_plural = "managed companies"

    name = models.CharField(max_length=255)
    vat_number = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50)
    billing_email = models.EmailField()
    address = models.TextField()
    website = models.URLField(blank=True)
    currency = models.ForeignKey(
        "Currency",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=default_currency,
        related_name="companies"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="companies"
    )

    def __str__(self):
        return self.name

class Account(TimeStampedModel):
    """
    Customer / Prospect
    """
    class Meta:
        verbose_name_plural = "client companies"


    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="accounts"
    )

    def __str__(self):
        return self.name


class Contact(TimeStampedModel):
    """
    People you're tracking
    """
    account = models.ForeignKey(
        Account,
        verbose_name='Client Company',
        on_delete=models.CASCADE,
        related_name="contacts",
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    job_title = models.CharField(max_length=100, blank=True)

    notes = models.TextField(blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="contacts"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Opportunity(TimeStampedModel):
    """
    Potential Deals
    """
    class Meta:
        verbose_name_plural = "opportunities"

    class Stage(models.TextChoices):
        LEAD = "lead", "Lead"
        QUALIFIED = "qualified", "Qualified"
        PROPOSAL = "proposal", "Proposal Sent"
        NEGOTIATION = "negotiation", "Negotiation"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    name = models.CharField(max_length=255)

    account = models.ForeignKey(
        Account,
        verbose_name='Client Company',
        on_delete=models.CASCADE,
        related_name="opportunities"
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="opportunities"
    )

    stage = models.CharField(
        max_length=20,
        choices=Stage.choices,
        default=Stage.LEAD
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    expected_close_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="opportunities"
    )

    def __str__(self):
        return self.name


class Activity(TimeStampedModel):
    """
    Calls, Emails, Meetings, Notes
    """

    class Type(models.TextChoices):
        CALL = "call", "Call"
        EMAIL = "email", "Email"
        MEETING = "meeting", "Meeting"
        NOTE = "note", "Note"

    activity_type = models.CharField(
        max_length=20,
        choices=Type.choices
    )

    subject = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True
    )

    account = models.ForeignKey(
        Account,
        verbose_name='Client Company',
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True
    )

    activity_date = models.DateTimeField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activities_created"
    )

    def __str__(self):
        return self.subject


class Task(TimeStampedModel):
    """
    Follow-ups and Reminders
    """

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    title = models.CharField(max_length=255)

    description = HTMLField(blank=True)

    due_date = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_tasks"
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )

    account = models.ForeignKey(
        Account,
        verbose_name='Company',
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name