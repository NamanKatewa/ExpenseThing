from typing import List, Dict
from core.models import Expense, Payment


def print_expense_details(expense: Expense):
    """Prints formatted details of a single expense."""
    print(f"ID: {expense.id}")
    print(f"  Description: {expense.description}")
    print(f"  Amount: ${expense.amount:.2f}")
    print(f"  Paid by: {expense.paid_by}")
    print(
        f"  Involved: {', '.join(expense.involved_people)} (each owes ${expense.split_amount_per_person:.2f})"
    )
    print(f"  Date: {expense.date}")


def print_all_expenses(expenses: List[Expense]):
    """Prints formatted details of a list of expenses."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    for exp in expenses:
        print_expense_details(exp)
        print("-" * 30)


def print_payment_details(payment: Payment):
    """Prints formatted details of a single payment."""
    print(f"ID: {payment.id}")
    print(f"  Description: {payment.description}")
    print(f"  Amount: ${payment.amount:.2f}")
    print(f"  From: {payment.payer}")
    print(f"  To: {payment.payee}")
    print(f"  Date: {payment.date}")


def print_all_payments(payments: List[Payment]):
    """Prints formatted details of a list of payments."""
    if not payments:
        print("\nNo payments recorded yet.")
        return

    print("\n--- All Payments ---")
    for pay in payments:
        print_payment_details(pay)
        print("-" * 30)


def print_all_people(people: List[str]):
    """Prints a formatted list of all known people."""
    if not people:
        print("\nNo people registered yet.")
        return

    print("\n--- All People ---")
    for person in people:
        print(f"- {person}")
    print("-" * 30)


def print_balances(balances: Dict[str, float]):
    """Prints formatted current balances."""
    if not balances:
        print("No transactions to calculate balances.")
        return

    print("\n--- Net Balances ---")
    for person, balance in sorted(balances.items()):
        print(f"{person}: ${balance:.2f}")


def print_settlements(settlements: List[Dict]):
    """Prints formatted suggested settlements."""
    if not settlements:
        print("No settlements needed at this moment.")
        return

    print("\n--- Suggested Settlements ---")
    for s in settlements:
        print(f"{s['from']} owes {s['to']} ${s['amount']:.2f}")
