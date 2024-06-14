import g
import util


def status():
    status_rows = util.csv_get_rows(g.CSV_STATUS_FILEPATH)
    status_cols = util.csv_get_cols(status_rows)
    status_rows = status_rows[1:]

    return status_rows, status_cols


def herbs_auto():
    herbs_auto_rows = util.csv_get_rows(g.CSV_HERBS_AUTO_FILEPATH)
    herbs_auto_cols = util.csv_get_cols(herbs_auto_rows)
    herbs_auto_rows = herbs_auto_rows[1:]

    return herbs_auto_rows, herbs_auto_cols