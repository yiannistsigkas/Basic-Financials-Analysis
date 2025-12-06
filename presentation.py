"""
presentation.py

Handles console output: aligned tables, simple messages, and optional charts.
Also contains a helper for exporting results to CSV.
"""

import csv


try:
    import importlib
    plt = importlib.import_module("matplotlib.pyplot")
except Exception:
    plt = None  # matplotlib is optional

import calculations


def _metric_is_percentage(metric_name):
    """
    Decide if a metric should be shown as a percentage.
    """
    name_lower = metric_name.lower()
    if "margin" in name_lower:
        return True
    if metric_name in ("ROA", "ROE"):
        return True
    return False


def format_value(value, metric_name=None):
    """
    Convert a numeric metric value to string for display.

    If value is None, returns "N/A".
    Percentage metrics are shown as e.g. "15.23%".
    Others are shown with 2 decimal places.
    """
    if value is None:
        return "N/A"

    if metric_name is not None and _metric_is_percentage(metric_name):
        return f"{value * 100:.2f}%"

    # Generic numeric display
    return f"{value:.2f}"


def print_results_table(results, selected_metrics):
    """
    Print a table of results.

    Parameters
    ----------
    results : list of dict
        Each dict contains at least 'company_name', 'year', and metric values.
    selected_metrics : list of str
        Metric names to display as columns.
    """
    if not results:
        print("No results to display.")
        return

    # Column names
    headers = ["Company", "Year"] + selected_metrics

    # Determine column widths
    col_widths = {
        "Company": len("Company"),
        "Year": len("Year"),
    }
    for metric in selected_metrics:
        col_widths[metric] = len(metric)

    for row in results:
        company = str(row.get("company_name", ""))
        year = str(row.get("year", ""))

        if len(company) > col_widths["Company"]:
            col_widths["Company"] = len(company)
        if len(year) > col_widths["Year"]:
            col_widths["Year"] = len(year)

        for metric in selected_metrics:
            value = row.get(metric)
            value_str = format_value(value, metric)
            if len(value_str) > col_widths[metric]:
                col_widths[metric] = len(value_str)

    # Build and print header
    header_parts = [
        "Company".ljust(col_widths["Company"]),
        "Year".rjust(col_widths["Year"]),
    ]
    for metric in selected_metrics:
        header_parts.append(metric.rjust(col_widths[metric]))
    header_line = "  ".join(header_parts)
    print(header_line)

    # Separator line
    total_width = len(header_line)
    print("-" * total_width)

    # Data rows
    for row in results:
        company = str(row.get("company_name", "")).ljust(col_widths["Company"])
        year = str(row.get("year", "")).rjust(col_widths["Year"])

        metric_cells = []
        for metric in selected_metrics:
            value = row.get(metric)
            value_str = format_value(value, metric).rjust(col_widths[metric])
            metric_cells.append(value_str)

        line = "  ".join([company, year] + metric_cells)
        print(line)

    print()  # blank line after the table


def print_message(message):
    """
    Print a simple message to the console.
    """
    print(message)


def print_error(message):
    """
    Print an error message.
    """
    print(f"Error: {message}")


def export_results_to_csv(results, selected_metrics, filename):
    """
    Export computed results to a CSV file.

    Parameters
    ----------
    results : list of dict
        Each dict contains 'company_name', 'year', and metric values.
    selected_metrics : list of str
        Metric names representing columns.
    filename : str
        Output CSV filename.
    """
    header = ["company_name", "year"] + selected_metrics

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            for row in results:
                row_values = [
                    row.get("company_name", ""),
                    row.get("year", ""),
                ]
                for metric in selected_metrics:
                    value = row.get(metric)
                    # For CSV, we keep raw numeric values; None -> empty string
                    row_values.append("" if value is None else value)
                writer.writerow(row_values)

        print_message(f"Results exported to '{filename}'.")
    except OSError as exc:
        print_error(f"Failed to write to '{filename}': {exc}")


def plot_roe_over_time(records, company_name):
    """
    Plot ROE over years for the given company using matplotlib.

    Parameters
    ----------
    records : list of dict
        All company-year records.
    company_name : str
        Name of the company to plot.
    """
    if plt is None:
        print_error("matplotlib is not installed. Plotting is unavailable.")
        return

    # Collect (year, ROE) for chosen company
    data_points = []
    for record in records:
        if record.get("company_name") == company_name:
            year = record.get("year")
            roe = calculations.return_on_equity(record)
            if year is not None and roe is not None:
                data_points.append((year, roe))

    if not data_points:
        print_error("No ROE data available for this company.")
        return

    # Sort by year
    data_points.sort(key=lambda x: x[0])
    years = [p[0] for p in data_points]
    roes = [p[1] for p in data_points]

    plt.figure()
    plt.plot(years, roes, marker="o")
    plt.title(f"ROE over time for {company_name}")
    plt.xlabel("Year")
    plt.ylabel("ROE")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def print_company_comparison(company_a, data_a, company_b, data_b, metric_name):
    """
    Print a side-by-side comparison of one metric for two companies over years.

    Parameters
    ----------
    company_a : str
    data_a : dict
        Mapping year -> value for company A.
    company_b : str
    data_b : dict
        Mapping year -> value for company B.
    metric_name : str
    """
    years = sorted(set(data_a.keys()) | set(data_b.keys()))
    if not years:
        print_error("No data to compare.")
        return

    # Determine column widths
    year_width = max(4, max(len(str(y)) for y in years))
    col_a_name = f"{company_a} {metric_name}"
    col_b_name = f"{company_b} {metric_name}"
    col_a_width = max(len(col_a_name), 10)
    col_b_width = max(len(col_b_name), 10)

    # Header
    header = (
        str("Year").rjust(year_width)
        + "  "
        + col_a_name.rjust(col_a_width)
        + "  "
        + col_b_name.rjust(col_b_width)
    )
    print(header)
    print("-" * len(header))

    for year in years:
        val_a = data_a.get(year)
        val_b = data_b.get(year)
        val_a_str = format_value(val_a, metric_name).rjust(col_a_width)
        val_b_str = format_value(val_b, metric_name).rjust(col_b_width)
        line = str(year).rjust(year_width) + "  " + val_a_str + "  " + val_b_str
        print(line)

    print()

