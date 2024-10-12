'''Header Descr'''

'''Main function'''


def main(CSVfile: str, TXTfile: str, category: str):
    print("For test")
    CSVdict = read_csv_as_dict(CSVfile)
    CSVdict = read_txt_into_dict(CSVdict, TXTfile)

    OP1 = task1(CSVdict)
    print(OP1[0]['afghanistan'])
    print(OP1[1]['afghanistan'])
    print(OP1[2]['afghanistan'])

    OP2 = task2(CSVdict, OP1)
    print(len(OP2))
    print(OP2['afghanistan'])
    print(OP2['albania'])

    OP3 = task3(CSVdict, category)
    print(OP3['afghanistan']) #785004.5
    print(OP3['brunei darussalam']) #24420.5

    OP4 = task4(CSVdict)
    print(len(OP4['children']))
    print(OP4['children']['canada']) #[3925.4, 4448, 22.0588]
'''Task functions'''


def task1(CSVdict: dict) -> list:
    # Initialisation for each dict
    country_to_hospitals = {}
    country_to_death = {}
    country_to_covid_stroke = {}
    # Update or append data into the dict
    for country, hospital, death, covid, stroke in zip(CSVdict['country'], CSVdict['hospital_id'], CSVdict['no_of_deaths_in_2022'], CSVdict['covid'], CSVdict['stroke']):
        if country in country_to_hospitals:
            country_to_hospitals[country].append(hospital)
            country_to_death[country].append(int(death))
            country_to_covid_stroke[country].append(int(covid) + int(stroke))
        else:
            country_to_hospitals.update({country: [hospital]})
            country_to_death.update({country: [int(death)]})
            country_to_covid_stroke.update({country: [int(covid) + int(stroke)]})
    return [country_to_hospitals, country_to_death, country_to_covid_stroke]


def task2(CSV_dict: dict, data_list: list) -> dict:
    cosine_dict = {}
    death_data_set = []
    covid_stroke_data_set = []
    for country in CSV_dict['country']:
        if not country in cosine_dict:
            death_data_set = data_list[1][country]
            covid_stroke_data_set = data_list[2][country]
            cosine_dict.update({country: get_cosine(death_data_set, covid_stroke_data_set)})
    return cosine_dict


def task3(CSV_dict: dict, category: str) -> dict:
    # Initialisation for the dicts
    variance_dict = {}
    c_hc_c_dict = {}
    # Get the formated data set for the next step
    for country, hospital_category, cancer in zip(CSV_dict['country'], CSV_dict['hospital_category'], CSV_dict['cancer']):
        if country in c_hc_c_dict:
            if hospital_category == category:
                c_hc_c_dict[country].append(int(cancer))
        else:
            if hospital_category == category:
                c_hc_c_dict.update({country: [int(cancer)]})
    # Calculate for the variance
    for country in c_hc_c_dict:
        if not country in variance_dict:
            variance_dict.update({country: get_variance(c_hc_c_dict[country])})
    return variance_dict


def task4(CSVdict: dict) -> dict:
    category_country_dict = {}
    counter_dict = {}

    for category, country, female_patients, no_of_staff, death_2022, death_2023 in zip(CSVdict['hospital_category'], CSVdict['country'], CSVdict['female_patients'], CSVdict['no_of_staff'], CSVdict['no_of_deaths_in_2022'], CSVdict['no_of_deaths_in_2023']):
        item = category+country
        if item not in counter_dict:
            counter_dict.update({item: [int(female_patients), 1, int(no_of_staff), int(death_2022), int(death_2023)]})
        else:
            counter_dict[item][0] += int(female_patients)
            counter_dict[item][1] += 1
            if int(no_of_staff) > counter_dict[item][2]:
                counter_dict[item][2] = int(no_of_staff)
            counter_dict[item][3] += int(death_2022)
            counter_dict[item][4] += int(death_2023)

    for category, country in zip(CSVdict['hospital_category'], CSVdict['country']):
        item = category+country
        if category not in category_country_dict:
            category_country_dict.update({category: {}})
        if country not in category_country_dict[category]:
            category_country_dict[category].update({country: [counter_dict[item][0]/counter_dict[item][1], counter_dict[item][2], get_pcad(counter_dict[item][3], counter_dict[item][4])]})
    return category_country_dict


'''Functional functions'''


# Read file as dict
def read_csv_as_dict(file: str) -> dict:
    # Create the fict
    file_dict = {}
    with open(file, 'r') as open_file:
        # Initialisation for the header line
        headers = open_file.readline().lower().strip().split(',')
        file_dict = {header: [] for header in headers}
        # Take the values into the dict by category
        for line in open_file:
            values = line.lower().strip().split(',')

            if validate_data(headers, values, file_dict) is False:
                continue

            for header, value in zip(headers, values):
                file_dict[header].append(value)
    return file_dict


def validate_data(headers, values, file_dict):
    # Check for correct length of values as the header's
    if not len(values) == len(headers):
        print('ERROR: Length')
        return False
    
    # Check for empty values
    if '' in values:
        print('ERROR: None Value')
        return False
    
    # Specific checks for hospital_id
    hid_index = headers.index('hospital_id')
    if 'hospital_id' in file_dict:
        hid = values[hid_index]
        if not len(hid) == 15 or hid in file_dict['hospital_id']:
            print('ERROR: hospital_id')
            return False
        
    # Check for no_of_staff
    sno_index = headers.index('no_of_staff')
    sno = values[sno_index]
    if 'no_of_staff' in file_dict and not int(sno) > 0:
        print('ERROR: no_of_staff')
        return False
    
    # Check for no_of_patients, male_patients, female_patients
    pno_index = headers.index('no_of_patients')
    mpno_index = headers.index('male_patients')
    fpno_index = headers.index('female_patients')
    pno, mpno, fpno = values[pno_index], values[mpno_index], values[fpno_index]
    if 'no_of_patients' in file_dict and (not (int(pno) > 0 and int(mpno) > 0 and int(fpno) > 0) or int(pno) != int(mpno) + int(fpno)):
        print('ERROR: no_of_patients')
        return False
    
    # Check for no_of_beds
    bno_index = headers.index('no_of_beds')
    bno = values[bno_index]
    if 'no_of_beds' in file_dict and not int(bno) > 0:
        print('ERROR: no_of_beds')
        return False
    
    # Check for no_of_deaths_in_2022 and no_of_deaths_in_2023
    dno22_index = headers.index('no_of_deaths_in_2022')
    dno23_index = headers.index('no_of_deaths_in_2023')
    dno22, dno23 = values[dno22_index], values[dno23_index]
    if 'no_of_deaths_in_2022' in file_dict and 'no_of_deaths_in_2023' in file_dict and (not (int(dno22) > 0 and int(dno23) > 0)):
        print('ERROR: no_of_deaths')
        return False
    
    # If there is no issues, returns True
    return True

def read_txt_into_dict(data_dict: dict, TXTfile: str) -> dict:
    with open(TXTfile, 'r') as open_file:
        # Initialisation for the diseases
        data_dict['covid'] = [None] * len(data_dict['hospital_id'])
        data_dict['stroke'] = [None] * len(data_dict['hospital_id'])
        data_dict['cancer'] = [None] * len(data_dict['hospital_id'])
        for line in open_file:
            # Create the list and dict or each row in TXT file
            element = [i.split(':') for i in line.lower().strip().split(', ')]
            element_dict = {element[i][0]: element[i][1].strip() for i in range(len(element))}
            # Insert the TXT data into the main dict
            if element_dict['hospital_id'] in data_dict['hospital_id']:
                index = data_dict['hospital_id'].index(element_dict['hospital_id'])
                data_dict['covid'][index] = element_dict['covid']
                data_dict['stroke'][index] = element_dict['stroke']
                data_dict['cancer'][index] = element_dict['cancer']
    return data_dict


'''Mathematical finctions'''


# Cosine similarity
def get_cosine(set_x: list, set_y: list) -> float:
    numerator, denumerator = 0, 0
    denumerator1, denumerator2 = 0, 0
    set_len = len(set_x)
    for i in range(set_len):
        numerator += set_x[i] * set_y[i]
        denumerator1 += set_x[i] ** 2
        denumerator2 += set_y[i] ** 2
    denumerator = (denumerator1 ** 0.5) * (denumerator2 ** 0.5)
    return round(numerator / denumerator, 4)

# Variance
def get_variance(data_set: list) -> float:
    try:
        set_len = len(data_set)
        set_mean = 0
        numerator = 0
        # Get the mean of the set
        for i in range(set_len):
            set_mean += data_set[i]
        set_mean /= set_len
        # Culculate the numerator
        for i in range (set_len):
            numerator += (data_set[i] - set_mean) ** 2
        return round(numerator / (set_len - 1), 1)
    except:
        return 0

# Average Percentage Change
def get_pcad(ave_death_2022: int, ave_death_2023: int) -> int:
    return round((ave_death_2023 - ave_death_2022) / ave_death_2022 * 100, 4)


'''Temp Test'''


main('Project2/hospital_data.csv', 'Project2/disease.txt', 'children')