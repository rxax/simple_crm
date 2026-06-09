from django.conf import settings
from django.db import models

from crm.models import TimeStampedModel, Account, Company

"""
Add Invoicing feature 
"""

"""
    basically the Subscription model is a contract
"""
class Subscription(TimeStampedModel):

    class Meta:
        verbose_name = "subscription contract"
        verbose_name_plural = "Subscriptions and Contracts"

    class BillingCycle(models.TextChoices):
        MONTHLY = "monthly", "Monthly"
        QUARTERLY = "quarterly", "Quarterly"
        YEARLY = "yearly", "Yearly"

    account = models.ForeignKey(
        Account,
        verbose_name='Client Company',
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    name = models.CharField(max_length=255)

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    billing_cycle = models.CharField(
        max_length=20,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTHLY
    )

    monthly_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    active = models.BooleanField(default=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name


class Invoice(TimeStampedModel):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"
        PAID = "paid", "Paid"
        OVERDUE = "overdue", "Overdue"
        CANCELLED = "cancelled", "Cancelled"

    issuer = models.ForeignKey(
        Company,
        verbose_name='Issuing Company',
        on_delete=models.PROTECT,
        related_name="issued_invoices",
        null=True
    )

    account = models.ForeignKey(
        Account,
        verbose_name='Client Company',
        on_delete=models.PROTECT,
        related_name="invoices"
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices"
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    issue_date = models.DateField()

    due_date = models.DateField()

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.invoice_number


class InvoiceLine(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="lines"
    )

    description = models.CharField(max_length=255)

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.description


class Payment(TimeStampedModel):

    class Method(models.TextChoices):
        BANK = "bank", "Bank Transfer"
        STRIPE = "stripe", "Stripe"
        PAYPAL = "paypal", "PayPal"
        WISE = "wise", "Wise"
        CASH = "cash", "Cash"

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_date = models.DateField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=Method.choices
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.amount}"