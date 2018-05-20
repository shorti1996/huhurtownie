import csv

input_filename = "input/gun-violence-data.csv"

output_filename = "output/gvd-short.csv"
out_file = open(output_filename, 'w', encoding='utf-8', newline='\n')

fields = []
csvwriter = csv.writer(out_file)

csvwriter.writerow(["incident_id", "incident_characteristics", "notes"])

with open(input_filename, 'r', encoding='utf-8') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)

    i = 1
    for row in csvreader:
        # try:
        #     int(row[0])
        # except Exception:
        #     x = 1
        # if i == 11:
        #     xxx = 0
        #     pass
        incident_id_index = fields.index("incident_id")
        incident_char_index = fields.index("incident_characteristics")
        notes_index = fields.index("notes")
        notes = row[incident_char_index].replace(",", "")
        csvwriter.writerow([row[incident_id_index], notes])
        i += 1

    out_file.close()
