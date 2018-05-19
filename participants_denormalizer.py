import csv


class Location:
    def __init__(self, state=None, cityCounty=None, address=None, id=None):
        self.state = state
        self.cityCounty = cityCounty
        self.address = address
        self.id = id

    def __eq__(self, other):
        return \
            type(other) == Location \
            and self.state == other.state \
            and self.cityCounty == other.cityCounty \
            and self.address == other.address

    def __hash__(self):
        return hash(self.state) * 101\
                + hash(self.cityCounty) * 101 \
                + hash(self.address) * 101


input_filename = "input/gun-violence-data.csv"
output_victims_filename = "output/victims.csv"
output_subjects_filename = "output/subjects.csv"
output_locations_filename = "output/locations.csv"
output_vic_to_sub_filename = "output/vic_to_sub.csv"
# output_gun_violence_filename = "output/gun-violence-data-AFTER_GUNS.csv"

fields = []
rows = []

out_file_victims = open(output_victims_filename, 'w', encoding='utf-8', newline='\n')
out_file_subjects = open(output_subjects_filename, 'w', encoding='utf-8', newline='\n')
out_file_locations = open(output_locations_filename, 'w', encoding='utf-8', newline='\n')
out_file_vic_to_sub = open(output_vic_to_sub_filename, 'w', encoding='utf-8', newline='\n')
# out_file_gun_violence = open(output_gun_violence_filename, 'w', encoding='utf-8', newline='\n')

csvwriter_victims = csv.writer(out_file_victims)
csvwriter_subjects = csv.writer(out_file_subjects)
csvwriter_locations = csv.writer(out_file_locations)
csvwriter_vic_to_sub = csv.writer(out_file_vic_to_sub)
# csvwriter_gvd = csv.writer(out_file_gun_violence)


def split_field(field_index, row):
    splitted = [x for x in row[field_index].split("||")]
    if len(splitted) < 2:
        return dict()
    dictionary = dict((x.split('::')[0], x.split('::')[1]) for x in splitted)
    return dictionary


def extract_by_key_if_present(key, p_ages, return_val_if_absent=None):
    return p_ages[key] if key in p_ages.keys() else return_val_if_absent


def split_row_to_victims_and_subjects(row, fields):
    def create_victim_or_suspect(key, i_id, p_ages, p_genders, p_names, p_statuses):
        age = extract_by_key_if_present(key, p_ages)
        gender = extract_by_key_if_present(key, p_genders)
        name = extract_by_key_if_present(key, p_names)
        statuses = extract_by_key_if_present(key, p_statuses, return_val_if_absent="")
        is_unharmed = "Unharmed" in statuses
        is_injured = "Injured" in statuses
        is_killed = "Killed" in statuses
        is_arrested = "Arrested" in statuses
        return [i_id, age, gender, name, is_unharmed, is_injured, is_killed, is_arrested]

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
            victim = create_victim_or_suspect(i, i_id, p_ages, p_genders, p_names, p_statuses)
            victims.append(victim)
        else:
            subject = create_victim_or_suspect(i, i_id, p_ages, p_genders, p_names, p_statuses)
            subjects.append(subject)
    return victims, subjects

# return [i_id, age, gender, name, is_unharmed, is_injured, is_killed, is_arrested]
csvwriter_victims.writerow(["victim_id", "location_id", "date", "incident_id", "age", "gender", "name", "unharmed", "injured", "killed", "arrested"])
csvwriter_subjects.writerow(["subject_id", "incident_id", "age", "gender", "name", "unharmed", "injured", "killed", "arrested"])
csvwriter_locations.writerow(["id", "state", "cityCounty", "address"])
csvwriter_vic_to_sub.writerow(["id", "victim_id", "subject_id"])


def make_location(row, fields, location_index):
    l_state_index = fields.index("state")
    l_city_county_index = fields.index("city_or_county")
    l_address_index = fields.index("address")
    location = Location(row[l_state_index], row[l_city_county_index], row[l_address_index])
    location.id = location_index['val']
    location_index['val'] += 1
    locations_pool.append(location)
    csvwriter_locations.writerow([location.id, location.state, location.cityCounty, location.address])
    # loc_in_pool = [x for x in location_pool if x.__hash__() == location.__hash__()]
    # if len(loc_in_pool) == 0:
    #     location.id = location_index
    #     location_index += 1
    #     locations_pool.append(location)
    #     csvwriter_locations.writerow([location.id, location.state, location.cityCounty, location.address])
    # else:
    #     location.id = loc_in_pool[0].id
    return location


def make_date(date):
    """

    :type date: str
    """
    return date.replace('-', '')


with open(input_filename, 'r', encoding='utf-8') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)

    v_id, s_id = 1, 1
    location_index, locations_pool = {'val': 1}, []
    vic_to_sub_index = 1

    for row in csvreader:
        victims, subjects = split_row_to_victims_and_subjects(row, fields)
        location = make_location(row, fields, location_index)
        date = make_date(row[fields.index('date')])
        for s in subjects:
            csvwriter_subjects.writerow([str(s_id)] + s)
            s.append(s_id)
            s_id += 1
        for v in victims:
            csvwriter_victims.writerow([str(v_id), str(location.id), date] + v)
            for s in subjects:
                csvwriter_vic_to_sub.writerow([vic_to_sub_index, v_id, s[-1]])
                vic_to_sub_index += 1
            v_id += 1

    out_file_victims.close()
    out_file_subjects.close()
    out_file_locations.close()
    out_file_vic_to_sub.close()
    print("Total no. of rows: %d" % (csvreader.line_num))

print('Field names are:' + ', '.join(field for field in fields))

# #  printing first 5 rows
# print('\nFirst 5 rows are:\n')
# for row in rows[:5]:
#     # parsing each column of a row
#     for col in row:
#         print("%10s" % col),
#     print('\n')
