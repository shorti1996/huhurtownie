import csv

input_filename = "input/gun-violence-data.csv"
output_guns_filename = "output/guns.csv"
output_vic_to_gun_filename = "output/vic_to_gun.csv"
output_gun_violence_filename = "output/gun-violence-data-AFTER_GUNS.csv"

fields = []
rows = []

out_file_guns = open(output_guns_filename, 'w', encoding='utf-8', newline='\n')
out_file_vic_to_gun = open(output_vic_to_gun_filename, 'w', encoding='utf-8', newline='\n')
out_file_gun_violence = open(output_gun_violence_filename, 'w', encoding='utf-8', newline='\n')
csvwriter_guns = csv.writer(out_file_guns)
csvwriter_vic_to_gun = csv.writer(out_file_vic_to_gun)
csvwriter_gvd = csv.writer(out_file_gun_violence)


def split_row_to_guns(row, fields):
    def split_field(field_index, row):
        splitted = [x for x in row[field_index].split("||")]
        if len(splitted) < 2:
            return dict()
        dictionary = dict((x.split('::')[0], x.split('::')[1]) for x in splitted)
        return dictionary

    def create_gun_row(key, i_id, g_stolen, g_type):
        stolen = extract_by_key_if_present(key, g_stolen)
        type = extract_by_key_if_present(key, g_type)
        return [i_id, stolen, type]

    def extract_by_key_if_present(key, p_ages, return_val_if_absent=None):
        return p_ages[key] if key in p_ages.keys() else return_val_if_absent

    i_id_index = fields.index("incident_id")
    g_stolen_index = fields.index("gun_stolen")
    g_type_index = fields.index("gun_type")

    i_id = row[i_id_index]
    g_stolen_list = split_field(g_stolen_index, row)
    g_type_list = split_field(g_type_index, row)

    guns = []
    for i, participant_type in g_type_list.items():
        gun = create_gun_row(i, i_id, g_stolen_list, g_type_list)
        guns.append(gun)
    return guns

# return [i_id, stolen, type]
csvwriter_guns.writerow(["gun_id", "incident_id", "gun_stolen", "gun_type"])

with open(input_filename, 'r', encoding='utf-8') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)

    g_id = 1

    for row in csvreader:
        guns = split_row_to_guns(row, fields)
        for g in guns:
            csvwriter_guns.writerow([str(g_id)] + g)
            g_id += 1

    out_file_guns.close()
    out_file_vic_to_gun.close()
    print("Total no. of rows: %d" % (csvreader.line_num))

print('Field names are:' + ', '.join(field for field in fields))
