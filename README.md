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