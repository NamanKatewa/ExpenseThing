import os
from collections import defaultdict
from typing import List, Dict, Tuple
from decimal import Decimal, getcontext

from core.models import Expense, Payment

getcontext().prec = 2

LOG_FILE = os.path.join(os.path.dirname("__file__"), "log.txt")

with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("==== NEW DEBUG SESSION ====\n")


def log_debug(message: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


class ExpenseCalculator:
    def calculate_balances(
        self, expenses: List[Expense], payments: List[Payment]
    ) -> Dict[str, float]:
        """Calculates net balance for each person."""
        balances = defaultdict(float)

        for exp in expenses:
            paid_by = exp.paid_by
            amount = exp.amount
            involved_people = exp.involved_people
            split_amount = exp.split_amount_per_person

            balances[paid_by] += amount
            for person in involved_people:
                balances[person] -= split_amount

        for payment in payments:
            payer = payment.payer
            payee = payment.payee
            amount = payment.amount

            balances[payer] += amount
            balances[payee] -= amount

        return dict(balances)

    def simplify_debts(
        self, balances: Dict[str, float]
    ) -> List[Tuple[str, str, float]]:
        """Calculates minimum transactions to settle debts."""
        givers = {p: bal for p, bal in balances.items() if bal > 0}
        takers = {p: bal for p, bal in balances.items() if bal < 0}

        if not givers and not takers:
            return []

        transactions = []
        givers_list = sorted(givers.items(), key=lambda item: item[1], reverse=True)
        takers_list = sorted(takers.items(), key=lambda item: item[1])

        i, j = 0, 0
        while i < len(givers_list) and j < len(takers_list):
            giver_name, giver_amount = givers_list[i]
            taker_name, taker_amount = takers_list[j]

            settle_amount = min(giver_amount, abs(taker_amount))

            if settle_amount > 0.01:
                transactions.append((taker_name, giver_name, round(settle_amount, 2)))

            givers_list[i] = (giver_name, giver_amount - settle_amount)
            takers_list[j] = (taker_name, taker_amount + settle_amount)

            if givers_list[i][1] <= 0.01:
                i += 1
            if takers_list[j][1] >= -0.01:
                j += 1

        return transactions
