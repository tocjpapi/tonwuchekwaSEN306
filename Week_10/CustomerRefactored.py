# ============================================================
# CustomerRefactored.py
# SEN306 Lecture 8 - High Quality Routines
#
# Demonstrates refactoring a bloated "god routine" into
# small, focused, high-quality routines using the principles
# from the lecture:
#   - Single responsibility / functional cohesion
#   - Descriptive names (verb + object)
#   - Few parameters (≤ 7, ideally 0–4)
#   - No magic numbers → named constants
#   - Input validation / defensive programming
#   - No global state; explicit return values
#   - Well-documented (why, not just what)
# ============================================================

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import re


# ── Constants (no magic numbers) ─────────────────────────────
LOYALTY_THRESHOLD_YEARS = 3       # years of membership before loyalty discount
LOYALTY_DISCOUNT_RATE   = 0.10    # 10 % loyalty discount
BULK_ORDER_MINIMUM      = 10      # items needed to qualify for bulk pricing
BULK_DISCOUNT_RATE      = 0.05    # 5 % bulk discount
MAX_DISCOUNT_RATE       = 0.20    # cap at 20 % total discount
EMAIL_PATTERN           = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ── Data types ────────────────────────────────────────────────
@dataclass
class Customer:
    customer_id: int
    first_name: str
    last_name: str
    email: str
    membership_years: int
    order_count: int = 0


@dataclass
class OrderItem:
    product_name: str
    unit_price: float
    quantity: int


@dataclass
class Order:
    customer: Customer
    items: list[OrderItem] = field(default_factory=list)


@dataclass
class OrderSummary:
    subtotal: float
    discount_rate: float
    discount_amount: float
    total_due: float
    is_eligible_for_loyalty: bool
    is_bulk_order: bool


# ── Validation routines ───────────────────────────────────────

def is_valid_email(email: str) -> bool:
    """Return True if email matches a basic valid pattern."""
    return bool(EMAIL_PATTERN.match(email))


def is_valid_customer(customer: Customer) -> tuple[bool, str]:
    """
    Validate all required customer fields.

    Returns (True, "") on success, or (False, reason) on failure.
    Checking each field separately makes error messages precise
    rather than a single unhelpful "invalid customer" message.
    """
    if not customer.first_name.strip():
        return False, "First name must not be blank."
    if not customer.last_name.strip():
        return False, "Last name must not be blank."
    if not is_valid_email(customer.email):
        return False, f"Email '{customer.email}' is not valid."
    if customer.membership_years < 0:
        return False, "Membership years cannot be negative."
    return True, ""


def is_valid_order_item(item: OrderItem) -> tuple[bool, str]:
    """Return (True, "") for a valid item, or (False, reason) otherwise."""
    if item.unit_price < 0:
        return False, f"Unit price for '{item.product_name}' cannot be negative."
    if item.quantity <= 0:
        return False, f"Quantity for '{item.product_name}' must be at least 1."
    return True, ""


# ── Discount calculation routines ─────────────────────────────

def is_loyalty_eligible(customer: Customer) -> bool:
    """Return True if customer has earned a loyalty discount."""
    return customer.membership_years >= LOYALTY_THRESHOLD_YEARS


def is_bulk_order(order: Order) -> bool:
    """Return True if the order meets the minimum item count for bulk pricing."""
    total_items = sum(item.quantity for item in order.items)
    return total_items >= BULK_ORDER_MINIMUM


def calculate_discount_rate(customer: Customer, order: Order) -> float:
    """
    Determine the combined discount rate for this customer and order.

    Stacking loyalty + bulk discounts is intentional product behaviour.
    The cap prevents the rate from ever exceeding MAX_DISCOUNT_RATE.
    """
    rate = 0.0
    if is_loyalty_eligible(customer):
        rate += LOYALTY_DISCOUNT_RATE
    if is_bulk_order(order):
        rate += BULK_DISCOUNT_RATE
    return min(rate, MAX_DISCOUNT_RATE)


# ── Pricing routines ──────────────────────────────────────────

def calculate_order_subtotal(order: Order) -> float:
    """Sum (price × quantity) across all items; return 0.0 for an empty order."""
    return sum(item.unit_price * item.quantity for item in order.items)


def apply_discount(subtotal: float, discount_rate: float) -> float:
    """Return the amount to subtract given a subtotal and a rate in [0, 1]."""
    return round(subtotal * discount_rate, 2)


def calculate_order_total(subtotal: float, discount_amount: float) -> float:
    """Return the final amount owed after discount."""
    return round(subtotal - discount_amount, 2)


# ── Summary builder ───────────────────────────────────────────

def build_order_summary(order: Order) -> OrderSummary:
    """
    Assemble a complete pricing summary for the given order.

    Separating this from output/display keeps the pricing logic
    pure and easy to unit-test independently.
    """
    subtotal      = calculate_order_subtotal(order)
    discount_rate = calculate_discount_rate(order.customer, order)
    discount_amt  = apply_discount(subtotal, discount_rate)
    total         = calculate_order_total(subtotal, discount_amt)

    return OrderSummary(
        subtotal=subtotal,
        discount_rate=discount_rate,
        discount_amount=discount_amt,
        total_due=total,
        is_eligible_for_loyalty=is_loyalty_eligible(order.customer),
        is_bulk_order=is_bulk_order(order),
    )


# ── Display / output routine ──────────────────────────────────

def print_order_receipt(order: Order, summary: OrderSummary) -> None:
    """
    Print a human-readable receipt to stdout.

    Display is kept separate from calculation so each can change
    independently (e.g. switching to HTML output later).
    """
    c = order.customer
    print("=" * 40)
    print(f"  RECEIPT — {c.first_name} {c.last_name}")
    print("=" * 40)
    for item in order.items:
        line_total = item.unit_price * item.quantity
        print(f"  {item.product_name:<20} ${line_total:>7.2f}")
    print("-" * 40)
    print(f"  Subtotal:            ${summary.subtotal:>7.2f}")
    if summary.discount_rate > 0:
        label = []
        if summary.is_eligible_for_loyalty:
            label.append("loyalty")
        if summary.is_bulk_order:
            label.append("bulk")
        print(f"  Discount ({', '.join(label)}): -${summary.discount_amount:>6.2f}")
    print(f"  TOTAL DUE:           ${summary.total_due:>7.2f}")
    print("=" * 40)


# ── Orchestrating routine (thin coordinator) ──────────────────

def process_customer_order(customer: Customer, order: Order) -> Optional[OrderSummary]:
    """
    Validate inputs, build a pricing summary, and print a receipt.

    Returns the OrderSummary on success, or None if validation fails.
    Keeping this routine thin — it delegates every real decision to
    a focused sub-routine rather than doing the work itself.
    """
    valid, reason = is_valid_customer(customer)
    if not valid:
        print(f"[ERROR] Customer validation failed: {reason}")
        return None

    for item in order.items:
        valid, reason = is_valid_order_item(item)
        if not valid:
            print(f"[ERROR] Item validation failed: {reason}")
            return None

    summary = build_order_summary(order)
    print_order_receipt(order, summary)
    return summary


# ── Demo ──────────────────────────────────────────────────────
if __name__ == '__main__':
    customer = Customer(
        customer_id=42,
        first_name="Ada",
        last_name="Lovelace",
        email="ada@lovelace.io",
        membership_years=5,   # qualifies for loyalty discount
    )

    order = Order(
        customer=customer,
        items=[
            OrderItem("Algorithm Textbook", 45.99, 3),
            OrderItem("USB Hub",            12.50, 8),   # total items = 11 → bulk
            OrderItem("Notebook",            3.00, 4),
        ],
    )

    result = process_customer_order(customer, order)
    if result:
        print(f"\nDiscount applied: {result.discount_rate * 100:.0f}%")