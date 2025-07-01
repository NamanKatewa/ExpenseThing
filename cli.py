import click
import os
from services.expense_service import ExpenseService
from utils import display
from utils.pdf_export import export_summary_to_pdf
import datetime

expense_service = ExpenseService()


@click.group()
def cli():
    """"""
    pass


@cli.command()
@click.option(
    "--desc", prompt="Enter expense description", help="Description of the expense."
)
@click.option(
    "--amount",
    prompt="Enter total amount",
    type=float,
    help="Total amount of the expense.",
)
@click.option(
    "--paid-by",
    prompt="Who paid for this (enter name)",
    help="Name of the person who paid.",
)
def add(desc, amount, paid_by):
    """Add expense."""
    try:
        all_known_people = expense_service.get_all_people()
        involved_list_final = []

        if not all_known_people:
            click.echo(
                click.style(
                    "No people known yet. The payer will be the only person involved in splitting this expense.",
                    fg="yellow",
                )
            )
            involved_list_final = [paid_by]
        else:
            click.echo("\n--- Select People Involved in Splitting ---")
            for i, person in enumerate(all_known_people):
                click.echo(f"  {i+1}. {person}")
            click.echo("------------------------------------------")
            click.echo(
                click.style(
                    "Enter the numbers of people involved, separated by commas (e.g., 1,3,4).",
                    fg="cyan",
                )
            )
            click.echo(
                click.style(
                    "Press Enter without input to include ALL known people.", fg="cyan"
                )
            )
            click.echo(
                click.style(
                    "Type 'new' to manually enter names not on the list.", fg="cyan"
                )
            )

            temp_selected_people_for_loop = []
            while True:
                selection_input = click.prompt(
                    "Your selection", default="", show_default=False
                )
                selection_input = selection_input.strip().lower()

                if selection_input == "":
                    temp_selected_people_for_loop = all_known_people
                    click.echo(
                        click.style(
                            f"Including ALL known people: {', '.join(temp_selected_people_for_loop)}",
                            fg="blue",
                        )
                    )
                    break

                elif selection_input == "new":
                    manual_names_str = click.prompt(
                        "Enter new names (comma-separated)", type=str
                    )
                    temp_selected_people_for_loop = [
                        name.strip()
                        for name in manual_names_str.split(",")
                        if name.strip()
                    ]
                    click.echo(
                        click.style(
                            f"Manually entered people: {', '.join(temp_selected_people_for_loop)}",
                            fg="blue",
                        )
                    )
                    break

                else:
                    try:
                        current_attempt_selection = []
                        selected_indices = [
                            int(num.strip())
                            for num in selection_input.split(",")
                            if num.strip()
                        ]

                        valid_input_for_attempt = True
                        for index in selected_indices:
                            if 1 <= index <= len(all_known_people):
                                current_attempt_selection.append(
                                    all_known_people[index - 1]
                                )
                            else:
                                click.echo(
                                    click.style(
                                        f"Invalid selection: {index}. Please enter valid numbers.",
                                        fg="red",
                                    )
                                )
                                valid_input_for_attempt = False
                                break

                        if valid_input_for_attempt and current_attempt_selection:
                            temp_selected_people_for_loop = current_attempt_selection
                            click.echo(
                                click.style(
                                    f"Selected people: {', '.join(temp_selected_people_for_loop)}",
                                    fg="blue",
                                )
                            )
                            break
                        else:
                            click.echo(
                                click.style(
                                    "No valid people selected from your input. Please re-enter your selection.",
                                    fg="yellow",
                                )
                            )

                    except ValueError:
                        click.echo(
                            click.style(
                                "Invalid input format. Please enter comma-separated numbers, 'new', or press Enter.",
                                fg="red",
                            )
                        )

        involved_list_final = temp_selected_people_for_loop

        if not involved_list_final:
            click.echo(
                click.style(
                    "No valid people were ultimately selected for splitting. The payer will be the only person involved.",
                    fg="yellow",
                )
            )
            return

        involved_list_final = sorted(list(set(involved_list_final)))

        expense = expense_service.add_new_expense(
            desc, amount, paid_by, involved_list_final
        )
        click.echo(
            click.style(
                f"\nExpense '{expense.description}' added successfully!", fg="green"
            )
        )
        click.echo(f"  Total: ${expense.amount:.2f}, Paid by: {expense.paid_by}")
        click.echo(
            f"  Split among {len(expense.involved_people)} people: {', '.join(expense.involved_people)}"
        )
        click.echo(f"  Each owes: ${expense.split_amount_per_person:.2f}")

    except ValueError as e:
        click.echo(click.style(f"Error adding expense: {e}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred: {e}", fg="red"))



@cli.command()
def view():
    """View expenses."""
    expenses = expense_service.get_all_expenses()
    display.print_all_expenses(expenses)


@cli.command()
@click.option(
    "--payer",
    prompt="Who made the payment (your name)",
    help="Name of the person who paid.",
)
@click.option(
    "--payee",
    prompt="To whom was the payment made",
    help="Name of the person who received the payment.",
)
@click.option(
    "--amount",
    prompt="Enter payment amount",
    type=float,
    help="Amount of the direct payment.",
)
@click.option(
    "--desc",
    default="Direct Payment",
    help="Optional description for the payment (default: 'Direct Payment').",
)
def pay(payer, payee, amount, desc):
    """Record direct payment."""
    try:
        payment = expense_service.add_new_payment(payer, payee, amount, desc)
        click.echo(
            click.style(
                f"\nPayment recorded: '{payment.description}' from {payment.payer} to {payment.payee} for ${payment.amount:.2f}",
                fg="green",
            )
        )
    except ValueError as e:
        click.echo(click.style(f"Error recording payment: {e}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred: {e}", fg="red"))


@cli.command("view-payments")
def view_payments():
    """View payments."""
    payments = expense_service.get_all_payments()
    display.print_all_payments(payments)


@cli.command("add-person")
@click.option("--name", prompt="Enter person's name", help="Name of the person to add.")
def add_person(name):
    """Add person."""
    try:
        added = expense_service.add_person(name)
        if added:
            click.echo(click.style(f"Person '{name}' added successfully!", fg="green"))
        else:
            click.echo(click.style(f"Person '{name}' already exists.", fg="yellow"))
    except ValueError as e:
        click.echo(click.style(f"Error adding person: {e}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred: {e}", fg="red"))


@cli.command("list-people")
def list_people():
    """List people."""
    people = expense_service.get_all_people()
    display.print_all_people(people)


@cli.command()
def balances():
    """Show current balances between people (including payments)."""
    balances = expense_service.get_current_balances()
    display.print_balances(balances)


@cli.command()
def settle():
    """Show suggested transactions to settle debts (including payments)."""
    settlements = expense_service.get_suggested_settlements()
    display.print_settlements(settlements)


@cli.command("export-pdf")
@click.option(
    "--filename",
    default=f"expensething_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    help="Output PDF filename",
)
def export_pdf(filename):
    """Export all information to a nicely formatted PDF."""
    if not filename.startswith("data" + os.sep):
        filename = os.path.join("data", filename)
    people = expense_service.get_all_people()
    expenses = expense_service.get_all_expenses()
    payments = expense_service.get_all_payments()
    balances = expense_service.get_current_balances()
    settlements = expense_service.get_suggested_settlements()

    export_summary_to_pdf(filename, people, expenses, payments, balances, settlements)

    click.echo(
        click.style(f"Exported summary to {os.path.abspath(filename)}", fg="green")
    )


if __name__ == "__main__":
    cli()
