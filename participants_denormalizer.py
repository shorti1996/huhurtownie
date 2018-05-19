import csv

input_filename = "input/gun-violence-data.csv"
output_victims_filename = "output/victims.csv"
output_subjects_filename = "output/subjects.csv"

fields = []
rows = []

out_file_victims = open(output_victims_filename, 'w', encoding='utf-8', newline='\n')
out_file_subjects = open(output_subjects_filename, 'w', encoding='utf-8', newline='\n')
csvwriter_victims = csv.writer(out_file_victims)
csvwriter_subjects = csv.writer(out_file_subjects)


def split_row_to_victims_and_subjects(row, fields):
    def split_field(field_index, row):
        splitted = [x for x in row[field_index].split("||")]
        if len(splitted) < 2:
            return dict()
        dictionary = dict((x.split('::')[0], x.split('::')[1]) for x in splitted)
        return dictionary

    def create_victim_or_suspect_row(key, i_id, p_ages, p_genders, p_names, p_statuses):
        age = extract_by_key_if_present(key, p_ages)
        gender = extract_by_key_if_present(key, p_genders)
        name = extract_by_key_if_present(key, p_names)
        statuses = extract_by_key_if_present(key, p_statuses, return_val_if_absent="")
        is_unharmed = "Unharmed" in statuses
        is_injured = "Injured" in statuses
        is_killed = "Killed" in statuses
        is_arrested = "Arrested" in statuses
        return [i_id, age, gender, name, is_unharmed, is_injured, is_killed, is_arrested]

    def extract_by_key_if_present(key, p_ages, return_val_if_absent=None):
        return p_ages[key] if key in p_ages.keys() else return_val_if_absent

    i_id_index = fields.index("incident_id")
    p_age_index = fields.index("participant_age")
    p_gender_index = fields.index("participant_gender")
    p_name_index = fields.index("participant_name")
    p_status_index = fields.index("participant_status")  # killed, injured, etc.
    p_type_index = fields.index("participant_type")  # victim, subject-suspect

    i_id = row[i_id_index]
    p_ages = split_field(p_age_index, row)
    p_genders = split_field(p_gender_index, row)
    p_names = split_field(p_name_index, row)
    p_statuses = split_field(p_status_index, row)
    p_types = split_field(p_type_index, row)

    victims = []
    subjects = []
    for i, participant_type in p_types.items():
        if participant_type == "Victim":
            victim = create_victim_or_suspect_row(i, i_id, p_ages, p_genders, p_names, p_statuses)
            victims.append(victim)
        else:
            subject = create_victim_or_suspect_row(i, i_id, p_ages, p_genders, p_names, p_statuses)
            subjects.append(subject)
    return victims, subjects

# return [i_id, age, gender, name, is_unharmed, is_injured, is_killed, is_arrested]
csvwriter_victims.writerow(["victim_id", "incident_id", "age", "gender", "name", "unharmed", "injured", "killed", "arrested"])
csvwriter_subjects.writerow(["subject_id", "incident_id", "age", "gender", "name", "unharmed", "injured", "killed", "arrested"])

with open(input_filename, 'r', encoding='utf-8') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)

    v_id, s_id = 1, 1

    for row in csvreader:
        victims, subjects = split_row_to_victims_and_subjects(row, fields)
        for v in victims:
            csvwriter_victims.writerow([str(v_id)] + v)
            v_id += 1
        for s in subjects:
            csvwriter_subjects.writerow([str(s_id)] + s)
            s_id += 1

    out_file_victims.close()
    out_file_subjects.close()
    print("Total no. of rows: %d" % (csvreader.line_num))

print('Field names are:' + ', '.join(field for field in fields))

# #  printing first 5 rows
# print('\nFirst 5 rows are:\n')
# for row in rows[:5]:
#     # parsing each column of a row
#     for col in row:
#         print("%10s" % col),
#     print('\n')
