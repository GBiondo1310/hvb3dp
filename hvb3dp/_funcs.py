from datetime import timedelta


def seconds_to_timespan(seconds: int) -> str:
    """Converts time in seconds to a readable timespan"""

    td = timedelta(seconds=seconds)
    hours = td.seconds / 60 / 60
    minutes = (hours - int(hours)) * 60

    return f"{td.days} days {int(hours)} hours {round(minutes)} minutes"
