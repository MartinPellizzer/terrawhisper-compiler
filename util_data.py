import csv

import g
import util
import data_csv

status_rows, status_cols = data_csv.status()
herbs_rows, herbs_cols = data_csv.herbs()
herbs_names_common_rows, herbs_names_common_cols = data_csv.herbs_names_common()

status_herbs_rows, status_herbs_cols = data_csv.status_herbs()
status_systems_rows, status_systems_cols = data_csv.status_systems()
status_preparations_teas_rows, status_preparations_teas_cols = data_csv.status_preparations_teas()
status_preparations_tinctures_rows, status_preparations_tinctures_cols = data_csv.status_preparations_tinctures()
status_preparations_decoctions_rows, status_preparations_decoctions_cols = data_csv.status_preparations_decoctions()
status_preparations_essential_oils_rows, status_preparations_essential_oils_cols = data_csv.status_preparations_essential_oils()
status_preparations_capsules_rows, status_preparations_capsules_cols = data_csv.status_preparations_capsules()

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

def get_herbs_by_status(status_id):
    status_herbs_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_HERBS_FILEPATH, status_herbs_cols['status_id'], status_id,
    )
    status_herbs_ids = [
        row[status_herbs_cols['herb_id']] 
        for row in status_herbs_rows_filtered
        if row[status_herbs_cols['status_id']] == status_id
    ]
    herbs_rows_filtered = []
    for herb_row in herbs_rows:
        herb_id = herb_row[herbs_cols['herb_id']]
        if herb_id in status_herbs_ids:
            herbs_rows_filtered.append(herb_row)
    return herbs_rows_filtered

def get_herbs_names_common_by_status(status_id, preparation_slug):
    # get rows of specific preparation for status
    status_remedies_rows_filtered = []
    if preparation_slug == 'teas':
        status_remedies_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_PREPARATIONS_TEAS_FILEPATH, status_preparations_teas_cols['status_id'], status_id,
        )
    elif preparation_slug == 'tinctures':
        status_remedies_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_PREPARATIONS_TINCTURES_FILEPATH, status_preparations_tinctures_cols['status_id'], status_id,
        )
    elif preparation_slug == 'decoctions':
        status_remedies_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_PREPARATIONS_DECOCTIONS_FILEPATH, status_preparations_decoctions_cols['status_id'], status_id,
        )
    elif preparation_slug == 'essential-oils':
        status_remedies_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_PREPARATIONS_ESSENTIAL_OILS_FILEPATH, status_preparations_essential_oils_cols['status_id'], status_id,
        )
    elif preparation_slug == 'capsules':
        status_remedies_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_PREPARATIONS_CAPSULES_FILEPATH, status_preparations_capsules_cols['status_id'], status_id,
        )
    remedies_rows_filtered = []
    for status_remedy_row in status_remedies_rows_filtered:
        jun_remedy_id = status_remedy_row[status_preparations_teas_cols['remedy_id']]
        for herb_row in herbs_names_common_rows:
            herb_id = herb_row[herbs_cols['herb_id']]
            if herb_id == jun_remedy_id:
                remedies_rows_filtered.append(herb_row)
                break
    return remedies_rows_filtered

def get_status_by_system(system_id):
    status_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_SYSTEMS_FILEPATH, status_systems_cols['system_id'], system_id,
    )
    junction_status_ids = [
        row[status_systems_cols['status_id']] 
        for row in status_systems_rows_filtered
        if row[status_systems_cols['system_id']] == system_id
    ]
    status_rows_filtered = []
    for status_row in status_rows:
        status_id = status_row[status_cols['status_id']]
        if status_id in junction_status_ids:
            status_rows_filtered.append(status_row)
    return status_rows_filtered

