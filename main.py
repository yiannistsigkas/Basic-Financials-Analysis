"""
main.py

Entry point for the financial statement analysis program.

Run with:
    python main.py
"""

import importlib
import os
import calculations
import input_module
import presentation


try:
    plt = importlib.import_module("matplotlib.pyplot")
except Exception:
    plt = None


def _print_main_menu():
    """
    Display the main menu.
    """
    print("=== Financial Statement Pundit ===")
    print("1. Load financial data from CSV")
    print("2. Enter financial data manually")
    print("3. Choose metrics to calculate")
    print("4. Calculate and display ratios")
    print("5. Compare two companies (one metric)")
    print("6. Export last results to CSV")
    print("7. Plot ROE over time for a company")
    print("8. Load sample data")
    print("9. Clear data")
    print("0. Exit")


def _prompt_menu_choice():
    """
    Prompt the user for a menu choice and return it as a string.
    """
    return input("Enter your choice: ").strip()


def _choose_metrics():
    """
    Let the user choose which metrics to calculate.

    Returns
    -------
    list of str
        Metric names selected by the user.
    """
    metric_info = calculations.METRICS_INFO
    print("\nAvailable metrics:")
    for idx, (name, desc, _func) in enumerate(metric_info, start=1):
        print(f"{idx}. {name} - {desc}")

    print("\nEnter metric numbers separated by commas (e.g. 1,3,5)")
    print("Or press Enter to cancel.")
    while True:
        raw = input("Your selection: ").strip()
        if raw == "":
            return []

        parts = [p.strip() for p in raw.split(",") if p.strip()]
        indices = []
        valid = True
        for part in parts:
            if not part.isdigit():
                print("Please enter only numbers separated by commas.")
                valid = False
                break
            num = int(part)
            if num < 1 or num > len(metric_info):
                print(f"Invalid metric number: {num}")
                valid = False
                break
            indices.append(num)

        if not valid:
            continue

        # Remove duplicates while preserving order
        seen = set()
        selected = []
        for idx in indices:
            if idx not in seen:
                selected.append(idx)
                seen.add(idx)

        metric_names = [metric_info[i - 1][0] for i in selected]
        print("Selected metrics:", ", ".join(metric_names))
        return metric_names


def _compute_results(records, selected_metrics):
    """
    Compute selected metrics for all records.

    Parameters
    ----------
    records : list of dict
    selected_metrics : list of str

    Returns
    -------
    list of dict
        Each dict includes 'company_name', 'year', and metric values.
    """
    results = []
    for record in records:
        metric_values = calculations.compute_multiples(record, selected_metrics)
        row = {
            "company_name": record.get("company_name"),
            "year": record.get("year"),
        }
        row.update(metric_values)
        results.append(row)
    return results


def _choose_company(records, prompt_text):
    """
    Let the user select a company from the loaded records.

    Returns
    -------
    str or None
        Selected company name, or None if no selection.
    """
    companies = sorted({r.get("company_name") for r in records if r.get("company_name")})
    if not companies:
        presentation.print_error("No companies available.")
        return None

    print(prompt_text)
    for idx, name in enumerate(companies, start=1):
        print(f"{idx}. {name}")

    while True:
        raw = input("Enter number: ").strip()
        if not raw.isdigit():
            presentation.print_error("Please enter a valid number.")
            continue
        idx = int(raw)
        if idx < 1 or idx > len(companies):
            presentation.print_error("Number out of range.")
            continue
        return companies[idx - 1]

def _clear_data(records):
    """
    Let the user choose what data to clear.

    Options:
    - Clear all records
    - Clear records for a specific company
    - Clear records for a specific company-year
    """
    if not records:
        presentation.print_message("No data to clear.")
        return

    while True:
        print("\n=== Clear data ===")
        print("1. Clear ALL records")
        print("2. Clear records for one company")
        print("3. Clear one company-year")
        print("4. Cancel")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # Clear everything
            records.clear()
            presentation.print_message("All records have been cleared.")
            return

        elif choice == "2":
            # Clear by company
            company = _choose_company(records, "\nSelect the company to clear:")
            if company is None:
                return

            before = len(records)
            # Keep only records that do NOT match this company
            records[:] = [r for r in records if r.get("company_name") != company]
            removed = before - len(records)
            presentation.print_message(
                f"Removed {removed} record(s) for company '{company}'."
            )
            return

        elif choice == "3":
            # Clear by company + year
            company = _choose_company(records, "\nSelect the company:")
            if company is None:
                return

            # Collect years available for this company
            years = sorted(
                {
                    r.get("year")
                    for r in records
                    if r.get("company_name") == company and r.get("year") is not None
                }
            )
            if not years:
                presentation.print_error("No year data available for this company.")
                return

            print(f"\nAvailable years for {company}:")
            for idx, y in enumerate(years, start=1):
                print(f"{idx}. {y}")

            while True:
                raw = input("Choose year number: ").strip()
                if not raw.isdigit():
                    presentation.print_error("Please enter a number.")
                    continue
                idx = int(raw)
                if idx < 1 or idx > len(years):
                    presentation.print_error("Number out of range.")
                    continue
                year = years[idx - 1]
                break

            before = len(records)
            # Keep only records that are NOT this company-year
            records[:] = [
                r
                for r in records
                if not (
                    r.get("company_name") == company and r.get("year") == year
                )
            ]
            removed = before - len(records)
            presentation.print_message(
                f"Removed {removed} record(s) for {company} in year {year}."
            )
            return

        elif choice == "4":
            # Cancel
            presentation.print_message("Clear data cancelled.")
            return

        else:
            presentation.print_error("Invalid choice. Please try again.")


def _choose_metric_name():
    """
    Let the user choose a single metric name.

    Returns
    -------
    str or None
    """
    metric_info = calculations.METRICS_INFO
    print("\nChoose a metric:")
    for idx, (name, desc, _func) in enumerate(metric_info, start=1):
        print(f"{idx}. {name} - {desc}")

    while True:
        raw = input("Metric number: ").strip()
        if not raw.isdigit():
            presentation.print_error("Please enter a number.")
            continue
        idx = int(raw)
        if idx < 1 or idx > len(metric_info):
            presentation.print_error("Number out of range.")
            continue
        return metric_info[idx - 1][0]

def _load_sample_data(records):
    """
    Load a bundled sample CSV from the local 'data' directory.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_path = os.path.join(base_dir, "data", "sample_financials.csv")

    if not os.path.exists(sample_path):
        presentation.print_error(f"Sample file not found at: {sample_path}")
        return

    try:
        new_records = input_module.load_from_csv(sample_path)
        if not new_records:
            presentation.print_message("Sample file was found but contained no valid records.")
            return
        records.extend(new_records)
        presentation.print_message(
            f"Loaded {len(new_records)} sample records from '{sample_path}'."
        )
    except Exception as exc:
        presentation.print_error(f"Failed to load sample data: {exc}")


def main():
    """
    Main program loop.
    """
    records = []
    selected_metrics = []
    last_results = []

    while True:
        print()
        _print_main_menu()
        choice = _prompt_menu_choice()

        if choice == "1":
            # Load from CSV
            file_path = input("Enter CSV file path: ").strip()
            if not file_path:
                presentation.print_error("File path cannot be empty.")
                continue
            try:
                new_records = input_module.load_from_csv(file_path)
                if not new_records:
                    presentation.print_message("No valid records found in the file.")
                else:
                    records.extend(new_records)
                    presentation.print_message(f"Loaded {len(new_records)} records from '{file_path}'.")
            except FileNotFoundError:
                presentation.print_error(f"File not found: {file_path}")

        elif choice == "2":
            # Manual input
            new_records = input_module.manual_input()
            if new_records:
                records.extend(new_records)
                presentation.print_message(f"Added {len(new_records)} manually entered records.")
            else:
                presentation.print_message("No records were added.")

        elif choice == "3":
            # Choose metrics
            selected_metrics = _choose_metrics()
            if not selected_metrics:
                presentation.print_message("No metrics selected.")
            else:
                presentation.print_message("Metrics selection updated.")

        elif choice == "4":
            # Calculate and display
            if not records:
                presentation.print_error("No data loaded yet. Please load data first.")
                continue
            if not selected_metrics:
                presentation.print_error("No metrics selected. Please choose metrics first.")
                continue

            last_results = _compute_results(records, selected_metrics)
            presentation.print_results_table(last_results, selected_metrics)

        elif choice == "5":
            # Compare two companies
            if not records:
                presentation.print_error("No data loaded yet. Please load data first.")
                continue

            company_a = _choose_company(records, "\nSelect first company:")
            if company_a is None:
                continue
            company_b = _choose_company(records, "\nSelect second company:")
            if company_b is None:
                continue
            if company_a == company_b:
                presentation.print_error("Please choose two different companies.")
                continue

            metric_name = _choose_metric_name()
            if not metric_name:
                continue

            # Build data: year -> metric value
            data_a = {}
            data_b = {}
            for record in records:
                if record.get("company_name") == company_a:
                    val = calculations.compute_multiples(record, [metric_name])[metric_name]
                    year = record.get("year")
                    if year is not None:
                        data_a[year] = val
                elif record.get("company_name") == company_b:
                    val = calculations.compute_multiples(record, [metric_name])[metric_name]
                    year = record.get("year")
                    if year is not None:
                        data_b[year] = val

            presentation.print_company_comparison(company_a, data_a, company_b, data_b, metric_name)

        elif choice == "6":
            # Export to CSV
            if not last_results:
                presentation.print_error("No results to export. Please calculate metrics first.")
                continue
            if not selected_metrics:
                presentation.print_error("No metrics selected.")
                continue

            filename = input("Enter output CSV filename (e.g. results.csv): ").strip()
            if not filename:
                presentation.print_error("Filename cannot be empty.")
                continue
            if not filename.lower().endswith(".csv"):
                filename += ".csv"

            # Build path: <project_folder>/exports/<filename>
            base_dir = os.path.dirname(os.path.abspath(__file__))
            export_dir = os.path.join(base_dir, "exports")
            os.makedirs(export_dir, exist_ok=True)  

            full_path = os.path.join(export_dir, filename)

            presentation.export_results_to_csv(last_results, selected_metrics, full_path)

        elif choice == "7":
            # Plot ROE over time
            if not records:
                presentation.print_error("No data loaded yet. Please load data first.")
                continue

            company = _choose_company(records, "\nSelect a company for ROE plot:")
            if company is None:
                continue

            presentation.plot_roe_over_time(records, company)

        elif choice == "8":
            _load_sample_data(records)

        elif choice == "9":
            # Clear data
            _clear_data(records)

        elif choice == "0":
            # Exit
            print("Goodbye!")
            break

        else:
            presentation.print_error("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

