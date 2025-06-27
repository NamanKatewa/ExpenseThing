<<<<<<< HEAD
# PayPaladin

PayPaladin is a command-line interface (CLI) tool to track, split, and settle shared expenses. It is suitable for group expenses, shared living costs, or any scenario involving shared finances.

## Features

-   **Add Expenses:** Record new expenses with descriptions, amounts, payer, and involved participants.
-   **Record Payments:** Track direct payments between individuals.
-   **Manage People:** Add and list participants.
-   **View Balances:** Display current debts and credits.
-   **Settle Debts:** Suggest transactions to settle outstanding balances.
-   **Export to PDF:** Generate a PDF summary of expenses, payments, balances, and settlements.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/PayPaladin.git
    cd PayPaladin
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the CLI using `python cli.py <command> [options]`.

-   **Add an expense:**
    ```bash
    python cli.py add
    ```
-   **Record a direct payment:**
    ```bash
    python cli.py pay
    ```
-   **View all expenses:**
    ```bash
    python cli.py view
    ```
-   **View all payments:**
    ```bash
    python cli.py view-payments
    ```
-   **Add a person:**
    ```bash
    python cli.py add-person
    ```
-   **List all people:**
    ```bash
    python cli.py list-people
    ```
-   **Show current balances:**
    ```bash
    python cli.py balances
    ```
-   **Suggest settlements:**
    ```bash
    python cli.py settle
    ```
-   **Export summary to PDF:**
    ```bash
    python cli.py export-pdf
    ```

## Portfolio Highlight

PayPaladin demonstrates skills in:

-   **CLI Development:** Building applications with `Click`.
-   **Data Management:** Handling and persisting structured data.
-   **Algorithm Design:** Implementing balance calculation and debt settlement.
-   **PDF Generation:** Using `ReportLab` for document export.
-   **Modular Design:** Organizing codebase.

This project shows the ability to develop a functional application.
=======
-----

# PayPaladin: Your Command-Line Expense Splitter

PayPaladin is a simple yet effective command-line interface (CLI) tool designed to help you split expenses and settle debts among friends, family, or housemates. Forget the hassle of manual calculations; PayPaladin keeps track of who paid what, who owes whom, and suggests the simplest ways to settle up.

## Features

  * **Add Expenses:** Easily record shared expenses with descriptions, total amounts, who paid, and who was involved in the split.
  * **Record Payments:** Log direct payments between individuals to accurately reflect money exchanged outside of shared expenses.
  * **Manage People:** Add new people and list all individuals known to the system.
  * **View Expenses & Payments:** See a clear history of all recorded expenses and direct payments.
  * **Current Balances:** Get an instant overview of who owes whom.
  * **Settle Debts:** Receive intelligent suggestions for the minimum number of transactions needed to clear all outstanding balances.
  * **Export to PDF:** Generate a PDF report of all expenses, payments, balances, and settlement suggestions for easy sharing or record-keeping.

## Getting Started

Follow these steps to set up and run PayPaladin on your local machine.

### Prerequisites

  * Python 3.6+
  * `click` library for the CLI (will be installed in setup)
  * `reportlab` library for PDF generation (will be installed in setup)

### Installation

1.  **Clone the repository (or download the files):**

    ```bash
    git clone <your-repository-url>
    cd paypaladin
    ```

    (Replace `<your-repository-url>` with the actual URL if this is in a Git repo.)

2.  **Install dependencies:**
    It's highly recommended to use a virtual environment.

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

    pip install click reportlab
    ```

### Running the Application

After installation, you can run PayPaladin using the `python cli.py` command followed by the desired command.

```bash
python cli.py --help
```

## Usage

Here's how to use the different commands in PayPaladin:

-----

### `add-person` - Add a new person

Add individuals to your system. This is useful if you want to explicitly list people before adding expenses involving them.

```bash
python cli.py add-person
```

You'll be prompted to enter the person's name.

-----

### `list-people` - List all known people

See everyone currently recognized by PayPaladin (either explicitly added or included in previous transactions).

```bash
python cli.py list-people
```

-----

### `add` - Add a new expense

Record a new shared expense.

```bash
python cli.py add
```

You'll be prompted for:

  * **Description:** A brief note about the expense (e.g., "Dinner at Joe's," "Groceries," "Rent").
  * **Amount:** The total cost of the expense.
  * **Paid By:** The name of the person who paid the total amount.
  * **People Involved in Splitting:** You'll be presented with a list of known people. You can:
      * Enter numbers separated by commas (e.g., `1,3`) to select specific individuals.
      * Press **Enter** to include ALL known people.
      * Type `new` to manually enter names (comma-separated) for people not yet on the list.
      * **Crucially, the person who paid (`--paid-by`) is ONLY included in the split if you explicitly select them.**

**Example:**

```bash
python cli.py add
Enter expense description: Movie Tickets
Enter total amount: 30.00
Who paid for this (enter name): Alice
--- Select People Involved in Splitting ---
  1. Alice
  2. Bob
  3. Charlie
------------------------------------------
Enter the numbers of people involved, separated by commas (e.g., 1,3,4).
Press Enter without input to include ALL known people.
Type 'new' to manually enter names not on the list.
Your selection: 2,3
Selected people: Bob, Charlie

Expense 'Movie Tickets' added successfully!
  Total: $30.00, Paid by: Alice
  Split among 2 people: Bob, Charlie
  Each owes: $15.00
```

In this example, Alice paid for Bob and Charlie. Alice does not owe herself, so she is not included in the split unless you explicitly select her.

-----

### `view` - View all recorded expenses

See a detailed list of every expense added.

```bash
python cli.py view
```

-----

### `pay` - Record a direct payment

Log a one-off payment between two individuals outside of a specific expense. This helps keep balances accurate for settlement.

```bash
python cli.py pay
```

You'll be prompted for:

  * **Payer:** The person who made the payment.
  * **Payee:** The person who received the payment.
  * **Amount:** The amount of the payment.
  * **Description (optional):** A short note about the payment (defaults to "Direct Payment").

-----

### `view-payments` - View all recorded direct payments

See a history of all direct payments that have been recorded.

```bash
python cli.py view-payments
```

-----

### `balances` - Show current balances

Get a summary of who owes whom, taking into account all expenses and direct payments.

```bash
python cli.py balances
```

-----

### `settle` - Suggest settlement transactions

PayPaladin will calculate and display the most efficient way to settle all outstanding debts with the fewest possible transactions.

```bash
python cli.py settle
```

-----

### `export-pdf` - Export data to PDF

Generate a comprehensive PDF report containing all expenses, payments, current balances, and suggested settlements.

```bash
python cli.py export-pdf
```

A PDF file named `paypaladin_report_<timestamp>.pdf` will be created in the current directory.

-----

Feel free to contribute, report issues, or suggest new features\!
>>>>>>> 5ae5c74095dbc8c8d05194523605c261b6ec4a9f
