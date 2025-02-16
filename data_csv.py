import g
import util


def status():
    status_rows = util.csv_get_rows(g.CSV_STATUS_FILEPATH)
    status_cols = util.csv_get_cols(status_rows)
    status_rows = status_rows[1:]
    return status_rows, status_cols

def herbs():
    rows = util.csv_get_rows(g.CSV_HERBS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def herbs_auto():
    herbs_auto_rows = util.csv_get_rows(g.CSV_HERBS_AUTO_FILEPATH)
    herbs_auto_cols = util.csv_get_cols(herbs_auto_rows)
    herbs_auto_rows = herbs_auto_rows[1:]
    return herbs_auto_rows, herbs_auto_cols

def systems():
    rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def preparations():
    rows = util.csv_get_rows(g.CSV_PREPARATIONS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def equipments():
    rows = util.csv_get_rows('database/csv/equipments.csv')
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols



#######################
# JUNCTIONS
#######################

def status_systems():
    status_rows = util.csv_get_rows(g.CSV_STATUS_SYSTEMS_FILEPATH)
    status_cols = util.csv_get_cols(status_rows)
    status_rows = status_rows[1:]
    return status_rows, status_cols

def status_organs():
    status_rows = util.csv_get_rows(g.CSV_STATUS_ORGANS_FILEPATH)
    status_cols = util.csv_get_cols(status_rows)
    status_rows = status_rows[1:]
    return status_rows, status_cols

def status_herbs():
    rows = util.csv_get_rows(g.CSV_STATUS_HERBS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def status_preparations():
    rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def status_preparations_teas():
    rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_TEAS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def status_preparations_tinctures():
    rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_TINCTURES_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def status_preparations_decoctions():
    rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_DECOCTIONS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def status_preparations_essential_oils():
    rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_ESSENTIAL_OILS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def status_preparations_capsules():
    rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_CAPSULES_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def status_preparations_creams():
    rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_CREAMS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def herbs_names_common():
    rows = util.csv_get_rows(g.CSV_HERBS_NAMES_COMMON_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def herbs_benefits():
    rows = util.csv_get_rows(g.CSV_HERBS_BENEFITS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def herbs_preparations():
    rows = util.csv_get_rows(g.CSV_HERBS_PREPARATIONS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def herbs_constituents():
    rows = util.csv_get_rows(g.CSV_HERBS_CONSTITUENTS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def herbs_side_effects():
    rows = util.csv_get_rows(g.CSV_HERBS_SIDE_EFFECTS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

def herbs_precautions():
    rows = util.csv_get_rows(g.CSV_HERBS_PRECAUTIONS_FILEPATH)
    cols = util.csv_get_cols(rows)
    rows = rows[1:]
    return rows, cols

