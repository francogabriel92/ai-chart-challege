from datetime import datetime


def get_datetime(date: str, time: str) -> datetime:
    if not date or not time:
        raise ValueError("Both date and time must be provided")

    # Parse date from MM/DD/YYYY format
    date_obj = datetime.strptime(date, "%m/%d/%Y").date()

    # Parse time from H:MM or HH:MM format
    time_str = time
    if ":" in time_str:
        hour, minute = time_str.split(":")
        time_obj = time(int(hour), int(minute))
    else:
        # Handle case where only hour is provided
        time_obj = time(int(time_str), 0)

    # Combine date and time into a single datetime object
    combined_datetime = datetime.combine(date_obj, time_obj)
    if not combined_datetime:
        raise ValueError(f"Invalid date or time: {date} {time}")
    return combined_datetime
