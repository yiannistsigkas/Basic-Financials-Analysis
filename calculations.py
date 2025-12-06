"""
calculations.py

Pure functions for financial ratios and valuation multiples.

Each function takes a single record dict and returns a float or None.
"""

def safe_div(numerator, denominator):
    """
    Divide numerator by denominator safely.

    Returns None if denominator is 0, or if either value is None or invalid.
    """
    try:
        if numerator is None or denominator is None:
            return None
        if denominator == 0:
            return None
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return None


def net_margin(record):
    """
    Net margin = net_income / revenue
    """
    return safe_div(record.get("net_income"), record.get("revenue"))


def ebit_margin(record):
    """
    EBIT margin = ebit / revenue
    """
    return safe_div(record.get("ebit"), record.get("revenue"))


def return_on_assets(record):
    """
    Return on Assets (ROA) = net_income / total_assets
    """
    return safe_div(record.get("net_income"), record.get("total_assets"))


def return_on_equity(record):
    """
    Return on Equity (ROE) = net_income / total_equity
    """
    return safe_div(record.get("net_income"), record.get("total_equity"))


def debt_to_equity(record):
    """
    Debt to Equity = total_debt / total_equity
    """
    return safe_div(record.get("total_debt"), record.get("total_equity"))


def earnings_per_share(record):
    """
    Earnings per Share (EPS) = net_income / shares_outstanding
    """
    return safe_div(record.get("net_income"), record.get("shares_outstanding"))


def price_earnings_ratio(record):
    """
    Price/Earnings (P/E) = share_price / EPS
    """
    eps = earnings_per_share(record)
    share_price = record.get("share_price")
    return safe_div(share_price, eps)


def enterprise_value(record):
    """
    Enterprise Value (EV) = share_price * shares_outstanding + total_debt

    (Ignoring cash for simplicity.)
    """
    share_price = record.get("share_price")
    shares = record.get("shares_outstanding")
    debt = record.get("total_debt")

    if share_price is None or shares is None or debt is None:
        return None

    try:
        return share_price * shares + debt
    except TypeError:
        return None


def ev_to_ebit(record):
    """
    EV/EBIT = Enterprise Value / EBIT
    """
    ev = enterprise_value(record)
    ebit = record.get("ebit")
    return safe_div(ev, ebit)


def ev_to_ebitda(record):
    """
    EV/EBITDA = Enterprise Value / EBITDA
    """
    ev = enterprise_value(record)
    ebitda = record.get("ebitda")
    return safe_div(ev, ebitda)


# Metric definitions for the menu.
# (order is preserved and used by main.py)
METRICS_INFO = [
    ("Net margin", "Net income / Revenue", net_margin),
    ("EBIT margin", "EBIT / Revenue", ebit_margin),
    ("ROA", "Net income / Total assets", return_on_assets),
    ("ROE", "Net income / Total equity", return_on_equity),
    ("Debt/Equity", "Total debt / Total equity", debt_to_equity),
    ("P/E", "Share price / Earnings per share", price_earnings_ratio),
    ("EV/EBIT", "Enterprise value / EBIT", ev_to_ebit),
    ("EV/EBITDA", "Enterprise value / EBITDA", ev_to_ebitda),
]


def get_metric_names():
    """
    Convenience function: returns a list of metric names in menu order.
    """
    return [name for (name, _desc, _func) in METRICS_INFO]


def _metric_name_to_function():
    """
    Internal helper to build a mapping from metric name to function.
    """
    return {name: func for (name, _desc, func) in METRICS_INFO}


def compute_multiples(record, selected_metrics):
    """
    Compute selected metrics for a single record.

    Parameters
    ----------
    record : dict
        Financial data for one company-year.
    selected_metrics : list of str
        Metric names to compute, e.g. ["ROE", "P/E"].

    Returns
    -------
    dict
        Mapping metric name -> float or None (if not computable).
    """
    name_to_func = _metric_name_to_function()
    results = {}

    for metric_name in selected_metrics:
        func = name_to_func.get(metric_name)
        if func is None:
            results[metric_name] = None
        else:
            results[metric_name] = func(record)

    return results
