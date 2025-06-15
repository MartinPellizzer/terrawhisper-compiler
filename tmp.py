from oliark_io import csv_read_rows_to_json

import g

status_list = csv_read_rows_to_json(g.CSV_STATUS_FILEPATH)
system_list = csv_read_rows_to_json(g.CSV_SYSTEMS_FILEPATH)

status_system_list = csv_read_rows_to_json(g.CSV_STATUS_SYSTEMS_FILEPATH)

for status in status_list:
    # print(status)
    status_id = status['status_id']
    status_slug = status['status_slug']
    status_name = status['status_names'].split(',')[0].strip()
    status_system = [obj for obj in status_system_list if obj['status_id'] == status_id][0]
    system = [obj for obj in system_list if obj['system_id'] == status_system['system_id']][0]
    system_id = system['system_id']
    system_slug = system['system_slug']
    system_name = system['system_name']
    organ_slug = status['body_part']
    print(f'{status_name} -> {system_slug} -> {organ_slug}')

    system_slug = system_slug.split('-')[0]
    with open('systems-organs-ailments.csv', 'a') as f:
        f.write(f'{system_slug}\\{organ_slug}\\{status_slug}\\{status_name}\n')

