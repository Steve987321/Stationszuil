""" Helper functies

"""

from datetime import datetime


def get_time_str(frmt: str):
    """ Geeft de tijd als string terug met de gegeven tijd formaat. """
    return datetime.now().strftime(frmt)
