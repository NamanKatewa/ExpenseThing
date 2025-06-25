import os
from typing import List, Dict

from core.models import Expense, Payment
from core.data_manager import JSONDataManager
from core.calculator import ExpenseCalculator


class ExpenseService:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        project_root_data = os.path.join(base_path, "..", "data")

        self.expense_data_manager = JSONDataManager(
            os.path.join(project_root_data, "expenses.json")
        )
        self.payment_data_manager = JSONDataManager(
            os.path.join(project_root_data, "payments.json")
        )
        self.people_data_manager = JSONDataManager(
            os.path.join(project_root_data, "people.json")
        )
        self.calculator = ExpenseCalculator()

    # --- Expense Methods ---
    def get_all_expenses(self) -> List[Expense]:
        return self.expense_data_manager.load_items(Expense)

    def add_new_expense(
        self, description: str, amount: float, paid_by: str, involved_people: List[str]
    ) -> Expense:
        expenses = self.get_all_expenses()
        next_id = (max(exp.id for exp in expenses) + 1) if expenses else 1

        involved_set = set(p.strip() for p in involved_people if p.strip())
        final_involved_people = sorted(list(involved_set))

        if not final_involved_people:
            raise ValueError("No people selected for splitting.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if not description:
            raise ValueError("Description cannot be empty.")
        if not paid_by:
            raise ValueError("Payer name cannot be empty.")

        split_amount = amount / len(final_involved_people)

        new_expense = Expense(
            id=next_id,
            description=description,
            amount=amount,
            paid_by=paid_by,
            involved_people=final_involved_people,
            split_amount_per_person=round(split_amount, 2),
        )
        expenses.append(new_expense)
        self.expense_data_manager.save_items(expenses)

        # Register all people involved
        self._add_people_from_list(final_involved_people)
        self._add_people_from_list(
            [paid_by]
        )  # Still ensure payer is known, just not split-involved

        return new_expense

    # --- Payment Methods ---
    def get_all_payments(self) -> List[Payment]:
        return self.payment_data_manager.load_items(Payment)

    def add_new_payment(
        self, payer: str, payee: str, amount: float, description: str = "Direct Payment"
    ) -> Payment:
        payments = self.get_all_payments()
        next_id = (max(p.id for p in payments) + 1) if payments else 1

        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
        if not payer:
            raise ValueError("Payer name cannot be empty.")
        if not payee:
            raise ValueError("Payee name cannot be empty.")
        if payer == payee:
            raise ValueError("Payer and payee cannot be the same person.")

        new_payment = Payment(
            id=next_id,
            payer=payer,
            payee=payee,
            amount=round(amount, 2),
            description=description,
        )
        payments.append(new_payment)
        self.payment_data_manager.save_items(payments)

        # Automatically add payer/payee to the registered list
        self._add_people_from_list([payer, payee])

        return new_payment

    # --- People Management Methods (NEW) ---
    def _get_registered_people_raw(self) -> List[str]:
        # Helper to load raw list of strings
        data = self.people_data_manager.load_raw_data()
        return data if isinstance(data, list) else []

    def _save_registered_people_raw(self, people: List[str]):
        # Helper to save raw list of strings
        self.people_data_manager.save_raw_data(people)

    def add_person(self, name: str) -> bool:
        """Adds a single person to the registered list if they don't exist."""
        name = name.strip()
        if not name:
            raise ValueError("Person name cannot be empty.")

        people = self._get_registered_people_raw()
        if name not in people:
            people.append(name)
            people.sort()  # Keep it sorted
            self._save_registered_people_raw(people)
            return True  # Person was added
        return False  # Person already exists

    def _add_people_from_list(self, names: List[str]):
        """Internal helper to add multiple names without raising errors."""
        people = self._get_registered_people_raw()
        added_any = False
        for name in names:
            name = name.strip()
            if name and name not in people:
                people.append(name)
                added_any = True
        if added_any:
            people.sort()
            self._save_registered_people_raw(people)

    # --- Combined Reporting Methods ---
    def get_all_people(self) -> List[str]:
        """Gets all people from registered list, expenses, and payments."""
        all_people_set = set(
            self._get_registered_people_raw()
        )  # Start with explicitly registered

        expenses = self.get_all_expenses()
        for exp in expenses:
            all_people_set.add(exp.paid_by)
            for p in exp.involved_people:
                all_people_set.add(p)

        payments = self.get_all_payments()
        for pay in payments:
            all_people_set.add(pay.payer)
            all_people_set.add(pay.payee)

        return sorted(list(all_people_set))

    def get_current_balances(self) -> Dict[str, float]:
        expenses = self.get_all_expenses()
        payments = self.get_all_payments()
        return self.calculator.calculate_balances(expenses, payments)

    def get_suggested_settlements(self) -> List[Dict]:
        balances = self.get_current_balances()
        settlements = self.calculator.simplify_debts(balances)
        return [{"from": s[0], "to": s[1], "amount": s[2]} for s in settlements]
