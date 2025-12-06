import os
import csv

DATA_DIR = "data"
OUTPUT_FILE = "sample_financials.csv"

YEARS = list(range(2015, 2025))

# Values in *billions* USD, loosely based on public data.
APPLE_REVENUE_B = {
    2015: 233,
    2016: 216,
    2017: 229,
    2018: 266,
    2019: 260,
    2020: 274,
    2021: 365,
    2022: 394,
    2023: 383,
    2024: 391,
}

APPLE_NET_INCOME_B = {
    2015: 53,
    2016: 45,
    2017: 48,
    2018: 60,
    2019: 55,
    2020: 57,
    2021: 94,
    2022: 99,
    2023: 97,
    2024: 94,
}

NETFLIX_REVENUE_B = {
    2015: 6.8,
    2016: 8.8,
    2017: 11.7,
    2018: 15.8,
    2019: 20.1,
    2020: 25.0,
    2021: 29.7,
    2022: 31.6,
    2023: 33.7,
    2024: 39.0,
}

NETFLIX_NET_INCOME_B = {
    2015: 0.12,
    2016: 0.19,
    2017: 0.56,
    2018: 1.21,
    2019: 1.87,
    2020: 2.76,
    2021: 5.12,
    2022: 4.49,
    2023: 5.41,
    2024: 8.71,
}

CS_REVENUE_B = {
    2015: 22,
    2016: 21,
    2017: 20,
    2018: 21,
    2019: 22,
    2020: 22.4,
    2021: 22.7,
    2022: 14.9,
    2023: 10.0,
    2024: 0.0,
}

CS_NET_INCOME_B = {
    2015: 2.5,
    2016: 2.2,
    2017: 1.8,
    2018: 1.6,
    2019: 2.0,
    2020: 2.67,
    2021: -0.6,
    2022: -7.3,
    2023: -2.0,
    2024: 0.0,
}


def add_gnb_rows(rows):
    """Fictional mid-sized industrial company with steady growth."""
    base_revenue = 700.0  # in millions
    for year in YEARS:
        years_since_start = year - YEARS[0]
        revenue = round(base_revenue * (1.07 ** years_since_start), 1)
        cogs = round(revenue * 0.60, 1)
        ebit = round(revenue * 0.20, 1)
        net_income = round(revenue * 0.15, 1)
        total_assets = round(revenue * 0.80, 1)
        total_equity = round(total_assets * 0.50, 1)
        total_debt = round(total_equity * 0.50, 1)
        shares_outstanding = 100  # millions
        share_price = round(20 + years_since_start * 1.2, 1)
        ebitda = round(ebit + revenue * 0.03, 1)

        rows.append([
            "GNB Corp",
            year,
            revenue,
            cogs,
            ebit,
            net_income,
            total_assets,
            total_equity,
            total_debt,
            shares_outstanding,
            share_price,
            ebitda,
        ])


def add_apple_rows(rows):
    """Apple, loosely based on historical revenue & net income (in millions)."""
    for year in YEARS:
        revenue = APPLE_REVENUE_B[year] * 1000  # millions
        net_income = APPLE_NET_INCOME_B[year] * 1000
        gross_margin = 0.40
        ebit_margin = 0.27 if year >= 2020 else 0.25

        cogs = int(round(revenue * (1 - gross_margin)))
        ebit = int(round(revenue * ebit_margin))

        total_assets = {
            2015: 290000,
            2016: 320000,
            2017: 375000,
            2018: 365000,
            2019: 338000,
            2020: 324000,
            2021: 351000,
            2022: 352000,
            2023: 352000,
            2024: 360000,
        }[year]

        total_equity = {
            2015: 120000,
            2016: 128000,
            2017: 134000,
            2018: 107000,
            2019: 90000,
            2020: 65000,
            2021: 63000,
            2022: 60000,
            2023: 55000,
            2024: 50000,
        }[year]

        total_debt = {
            2015: 75000,
            2016: 85000,
            2017: 97000,
            2018: 110000,
            2019: 108000,
            2020: 112000,
            2021: 120000,
            2022: 120000,
            2023: 115000,
            2024: 110000,
        }[year]

        shares_outstanding = {
            2015: 5700,
            2016: 5400,
            2017: 5100,
            2018: 4800,
            2019: 4600,
            2020: 4400,
            2021: 4300,
            2022: 4200,
            2023: 4100,
            2024: 4000,
        }[year]  # millions of shares

        share_price = {
            2015: 120,
            2016: 110,
            2017: 170,
            2018: 160,
            2019: 260,
            2020: 130,
            2021: 170,
            2022: 150,
            2023: 190,
            2024: 200,
        }[year]

        ebitda = int(round(ebit + revenue * 0.05))

        rows.append([
            "Apple Inc.",
            year,
            revenue,
            cogs,
            ebit,
            net_income,
            total_assets,
            total_equity,
            total_debt,
            shares_outstanding,
            share_price,
            ebitda,
        ])


def add_netflix_rows(rows):
    """Netflix, loosely based on historical revenue & net income (in millions)."""
    for year in YEARS:
        revenue = int(round(NETFLIX_REVENUE_B[year] * 1000))
        net_income = int(round(NETFLIX_NET_INCOME_B[year] * 1000))

        gross_margin = 0.38
        if year <= 2017:
            ebit_margin = 0.15
        elif year <= 2020:
            ebit_margin = 0.20
        else:
            ebit_margin = 0.23

        cogs = int(round(revenue * (1 - gross_margin)))
        ebit = int(round(revenue * ebit_margin))

        total_assets = {
            2015: 11000,
            2016: 13000,
            2017: 20000,
            2018: 25000,
            2019: 33000,
            2020: 39000,
            2021: 44000,
            2022: 48000,
            2023: 50000,
            2024: 52000,
        }[year]

        total_equity = {
            2015: 3200,
            2016: 3500,
            2017: 4000,
            2018: 5000,
            2019: 6000,
            2020: 7000,
            2021: 9000,
            2022: 9500,
            2023: 10000,
            2024: 11000,
        }[year]

        total_debt = {
            2015: 2400,
            2016: 3400,
            2017: 6500,
            2018: 10400,
            2019: 14800,
            2020: 15800,
            2021: 15400,
            2022: 14200,
            2023: 14000,
            2024: 13500,
        }[year]

        shares_outstanding = {
            2015: 430,
            2016: 432,
            2017: 434,
            2018: 436,
            2019: 438,
            2020: 441,
            2021: 443,
            2022: 445,
            2023: 447,
            2024: 449,
        }[year]  # millions

        share_price = {
            2015: 120,
            2016: 130,
            2017: 190,
            2018: 260,
            2019: 320,
            2020: 500,
            2021: 540,
            2022: 300,
            2023: 450,
            2024: 550,
        }[year]

        ebitda = int(round(ebit + revenue * 0.06))

        rows.append([
            "Netflix Inc.",
            year,
            revenue,
            cogs,
            ebit,
            net_income,
            total_assets,
            total_equity,
            total_debt,
            shares_outstanding,
            share_price,
            ebitda,
        ])


def add_credit_suisse_rows(rows):
    """Credit Suisse, approximate data with high leverage (in millions)."""
    for year in YEARS:
        revenue = int(round(CS_REVENUE_B[year] * 1000))
        net_income = int(round(CS_NET_INCOME_B[year] * 1000))

        gross_margin = 0.70
        cogs = int(round(revenue * (1 - gross_margin)))

        if CS_NET_INCOME_B[year] >= 0:
            ebit_margin = 0.20
        else:
            ebit_margin = -0.10 if revenue > 0 else 0.0

        ebit = int(round(revenue * ebit_margin))

        total_assets = {
            2015: 980000,
            2016: 820000,
            2017: 776000,
            2018: 705000,
            2019: 789000,
            2020: 823000,
            2021: 912000,
            2022: 531000,
            2023: 520000,
            2024: 0,
        }[year]

        total_equity = {
            2015: 46000,
            2016: 44000,
            2017: 42000,
            2018: 40000,
            2019: 44000,
            2020: 47000,
            2021: 47000,
            2022: 45100,
            2023: 40000,
            2024: 0,
        }[year]

        total_debt = {
            2015: 300000,
            2016: 290000,
            2017: 285000,
            2018: 280000,
            2019: 290000,
            2020: 300000,
            2021: 305000,
            2022: 310000,
            2023: 320000,
            2024: 0,
        }[year]

        shares_outstanding = {
            2015: 2500,
            2016: 2600,
            2017: 2700,
            2018: 2800,
            2019: 2900,
            2020: 3000,
            2021: 3100,
            2022: 3300,
            2023: 3600,
            2024: 3900,
        }[year]  # millions

        share_price = {
            2015: 25,
            2016: 14,
            2017: 18,
            2018: 14,
            2019: 13,
            2020: 11,
            2021: 10,
            2022: 5,
            2023: 3,
            2024: 0.82,
        }[year]

        ebitda = int(round(ebit + revenue * 0.03)) if revenue > 0 else 0

        rows.append([
            "Credit Suisse Group AG",
            year,
            revenue,
            cogs,
            ebit,
            net_income,
            total_assets,
            total_equity,
            total_debt,
            shares_outstanding,
            share_price,
            ebitda,
        ])


def add_wayne_rows(rows):
    """Fictional conglomerate with decent margins and leverage (in millions)."""
    for index, year in enumerate(YEARS):
        base_b = 10 + index * 0.9  # revenue in billions
        revenue = round(base_b * 1000, 1)  # millions

        gross_margin = 0.35
        ebit_margin = 0.16 if year not in (2018, 2020) else 0.08
        net_margin = ebit_margin - 0.04

        cogs = round(revenue * (1 - gross_margin), 1)
        ebit = round(revenue * ebit_margin, 1)
        net_income = round(revenue * net_margin, 1)

        total_assets = round(revenue * 1.5, 1)
        total_equity = round(total_assets * 0.4, 1)
        total_debt = round(total_assets * 0.6, 1)

        shares_outstanding = 500  # millions
        share_price = round(40 + index * 2, 1)
        ebitda = round(ebit + revenue * 0.04, 1)

        rows.append([
            "Wayne Enterprises",
            year,
            revenue,
            cogs,
            ebit,
            net_income,
            total_assets,
            total_equity,
            total_debt,
            shares_outstanding,
            share_price,
            ebitda,
        ])


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, OUTPUT_FILE)

    header = [
        "company_name",
        "year",
        "revenue",
        "cogs",
        "ebit",
        "net_income",
        "total_assets",
        "total_equity",
        "total_debt",
        "shares_outstanding",
        "share_price",
        "ebitda",
    ]

    rows = []
    add_gnb_rows(rows)
    add_apple_rows(rows)
    add_netflix_rows(rows)
    add_credit_suisse_rows(rows)
    add_wayne_rows(rows)

    # Sort rows for readability
    rows.sort(key=lambda r: (r[0], r[1]))

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Written {len(rows)} rows to {path}")


if __name__ == "__main__":
    main()
