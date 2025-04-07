import os

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read

def teas_popular_get():
    output = []
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}/teas'
        json_filepath = f'database/json/{url}.json'
        if os.path.exists(json_filepath):
            data = json_read(json_filepath, create=True)
            for obj in data['remedies']:
                found = False
                for item in output:
                    if obj['herb_name_scientific'] == item['herb_name_scientific']:
                        item['herb_total_score'] += obj['herb_total_score']
                        found = True
                        break
                if not found:
                    output.append({
                        'herb_name_scientific': obj['herb_name_scientific'],
                        'herb_total_score': obj['herb_total_score'],
                    })
    output = sorted(output, key=lambda x: x['herb_total_score'], reverse=True)
    return output


