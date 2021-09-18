from datetime import timedelta


def date_diff_in_seconds(dt2, dt1):
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds


def dhms_from_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return days, hours, minutes, seconds


def get_elapsed_time(start, end):
    """Get elapsed time in a human readable format."""
    return "%s days, %s hours, %s minutes, %s seconds" % dhms_from_seconds(date_diff_in_seconds(start, end))
