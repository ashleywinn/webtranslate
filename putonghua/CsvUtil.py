import csv

def csv_dict_iter(csv_file, 
                  headings_row=0,
                  data_start_row=1,
                  column_names_upper=False):
    rec_reader = csv.reader(open(csv_file, 'rU'))
    row_num = 0
    while row_num < headings_row:
        rec_reader.__next__()
        row_num += 1
    headings = rec_reader.__next__()
    while row_num < data_start_row:
        rec_reader.__next__()
        row_num += 1
    if (column_names_upper):
        headings = [head.upper() for head in headings]
    for row in rec_reader:
        new_record = dict()
        for i, value in enumerate(row):
            new_record[headings[i]] = value
        yield new_record
    

def create_spreadsheet_from_records(csv_file, records, column_list=[]):
    rec_writer = csv.writer(open(csv_file, 'wb'))
    if not len(column_list):
        column_list = records[0].keys()
    rec_writer.writerow(column_list)
    for rec in records:
        rec_writer.writerow([rec.get(col_name, '') for col_name in column_list])




