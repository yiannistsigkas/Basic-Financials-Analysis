"""
input_module.py

Handles all data input: loading from CSV and manual interactive entry.

Expected CSV header (order doesn't matter, but names must match):

    company_name,year,revenue,cogs,ebit,net_income,total_assets,
    total_equity,total_debt,shares_outstanding,share_price,ebitda

Example row:

    ACME Corp,2024,1000000,600000,200000,150000,800000,400000,200000,100000,25,220000
"""

import csv


NUMERIC_FIELDS = [
    "revenue",
    "cogs",
    "ebit",
    "net_income",
    "total_assets",
    "total_equity",
    "total_debt",
    "shares_outstanding",
    "share_price",
    "ebitda",  # optional
]


def _safe_float(value):
    """
    Convert a string to float, returning None if empty or invalid.
    """
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _safe_int(value):
    """
    Convert a string to int, returning None if empty or invalid.
    """
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    try:
        return int(text)
    except ValueError:
        return None


def load_from_csv(file_path):
    """
    Load financial records from a CSV file.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    list of dict
        Each dict is a company-year record.
        Numeric parsing errors result in None values.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    records = []

    with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_name = (row.get("company_name") or "").strip()
            year = _safe_int(row.get("year"))

            # If company name or year is missing, skip this row.
            if not company_name or year is None:
                continue

            record = {
                "company_name": company_name,
                "year": year,
            }

            for field in NUMERIC_FIELDS:
                record[field] = _safe_float(row.get(field))

            records.append(record)

    return records


def _prompt_int(prompt_text):
    """
    Prompt the user for an integer, re-asking until valid.
    """
    while True:
        raw = input(prompt_text).strip()
        try:
            return int(raw)
        except ValueError:
            print("Invalid integer. Please try again.")


def _prompt_float(prompt_text, allow_empty=False):
    """
    Prompt the user for a float, re-asking until valid.

    If allow_empty is True, pressing Enter returns None.
    """
    while True:
        raw = input(prompt_text).strip()
        if allow_empty and raw == "":
            return None
        try:
            return float(raw)
        except ValueError:
            print("Invalid number. Please try again.")


def manual_input():
    """
    Interactively collect one or more company-year records from the user.

    Returns
    -------
    list of dict
        Records entered by the user.
    """
    records = []

    print("\nManual data entry. Please provide the requested fields.")
    print("Values are typically in your reporting currency (e.g., EUR, USD).")
    print("You can enter multiple company-year records.\n")

    while True:
        print("=== New company-year record ===")
        company_name = input("Company name: ").strip()
        while not company_name:
            print("Company name cannot be empty.")
            company_name = input("Company name: ").strip()

        year = _prompt_int("Year (e.g. 2024): ")

        revenue = _prompt_float("Revenue: ")
        cogs = _prompt_float("Cost of Goods Sold (COGS): ")
        ebit = _prompt_float("EBIT: ")
        net_income = _prompt_float("Net income: ")
        total_assets = _prompt_float("Total assets: ")
        total_equity = _prompt_float("Total equity: ")
        total_debt = _prompt_float("Total debt: ")
        shares_outstanding = _prompt_float("Shares outstanding: ")
        share_price = _prompt_float("Share price: ")
        ebitda = _prompt_float("EBITDA (optional, press Enter to skip): ", allow_empty=True)

        record = {
            "company_name": company_name,
            "year": year,
            "revenue": revenue,
            "cogs": cogs,
            "ebit": ebit,
            "net_income": net_income,
            "total_assets": total_assets,
            "total_equity": total_equity,
            "total_debt": total_debt,
            "shares_outstanding": shares_outstanding,
            "share_price": share_price,
            "ebitda": ebitda,
        }

        records.append(record)

        cont = input("Add another record? (y/n): ").strip().lower()
        if cont != "y":
            break

    return records
