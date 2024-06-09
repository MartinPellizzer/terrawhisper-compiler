import csv

import g


def csv_get_rows(filepath, delimiter='\\'):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, line in enumerate(reader):
            rows.append(line)
    return rows


def csv_get_cols(rows):
    cols = {}
    for i, val in enumerate(rows[0]):
        cols[val] = i
    return cols


# JUNCIONS
j_status_preparations_rows = csv_get_rows(g.CSV_STATUS_PREPARATIONS_FILEPATH)
j_status_preparations_cols = csv_get_cols(j_status_preparations_rows)
j_status_preparations_rows = j_status_preparations_rows[1:]