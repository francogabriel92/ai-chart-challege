import csv, os
from datetime import datetime, time
from sqlmodel import select
from app.models.sale import Sale
from app.database.db import get_session


def seed_sales_from_csv():
    session_gen = get_session()
    session = next(session_gen)
    try:
        result = session.exec(select(Sale)).first()
        if result:
            print("Data already exists. Skipping seeding.", flush=True)
            return

        print("Seeding data from CSV...", flush=True)

        csv_path = os.path.join(os.path.dirname(__file__), "data", "data.csv")

        if not os.path.exists(csv_path):
            print(
                f"CSV file not found at {csv_path}. Please check the path.", flush=True
            )
            return

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            sales = []
            for row in reader:

                # Parse date from MM/DD/YYYY format
                date_obj = datetime.strptime(row["date"], "%m/%d/%Y").date()

                # Parse time from H:MM or HH:MM format
                time_str = row["hour"]
                if ":" in time_str:
                    hour, minute = time_str.split(":")
                    time_obj = time(int(hour), int(minute))
                else:
                    # Handle case where only hour is provided
                    time_obj = time(int(time_str), 0)

                # Combine date and time into a single datetime object
                combined_datetime = datetime.combine(date_obj, time_obj)
                if not combined_datetime:
                    print(
                        f"Invalid date or time in row: {row}, dateTime: {combined_datetime}",
                        flush=True,
                    )
                    continue

                sale = Sale(
                    date=combined_datetime,
                    week_day=row["week_day"],
                    ticket_number=row["ticket_number"],
                    waiter=row["waiter"],
                    product_name=row["product_name"],
                    quantity=float(row["quantity"]),
                    unitary_price=float(row["unitary_price"]),
                    total=float(row["total"]),
                )
                sales.append(sale)
            session.add_all(sales)
            session.commit()
    except Exception:
        print(f"An error occurred while seeding data, please check the CSV file", flush=True)
        session.rollback()
    finally:
        session.close()
