#!/Users/navi/Projects/kxwheels.com/bin/python
import csv
import pprint
from kxwheels.apps.vehicle.models import *


VALID_COLUMNS = (
    'year',
    'manufacturer',
    'name',
    'boltpattern',
    'centerbore',

    'front_offset_range',
    'front_wheelwidth_range',
    'front_diameter_range',
    'rear_offset_range',
    'rear_wheelwidth_range',
    'rear_diameter_range',
    'oe_tiresize',
    'oe_staggered_tiresize',
    'plus_tiresize',
    'plus_staggered_tiresize',
)

def parse():
    with open('./fixtures/sample.csv', 'rU') as data:
        rows = csv.reader(data)
        fieldnames = rows.next()

        headings = map(lambda title: title.lower().strip(), fieldnames)
        if (fieldnames != headings):
            print("Fields don't match headings. Check it out!")
            return False

        mappings = dict((c, []) for c in VALID_COLUMNS)
        for i, fieldname in enumerate(fieldnames):
            mappings[fieldname].append(i)

        data = []
        for row in rows:
            row_dict = {}
            for fieldname, fieldindex in mappings.items():
                fieldvalues = []
                for i in fieldindex:
                    if row[i]:
                        fieldvalues.append(row[i])

                row_dict[fieldname] = fieldvalues
            data.append(row_dict)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)


def main():
    parse()

if __name__=="__main__":
    main()
