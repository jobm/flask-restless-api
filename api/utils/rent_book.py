import pytz
from datetime import datetime


def calculate_rent_cost(due_at):
    today = datetime.now(pytz.utc)
    due_at = due_at.astimezone(pytz.utc)
    days = (due_at - today).days or 1
    return days * 1
