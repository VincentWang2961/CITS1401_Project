'''Header Descr'''

'''Main function'''


def main(CSVfile: str, TXTfile: str):
    print("For test")
    CSVdict = read_csv_as_dict(CSVfile)
    OP1 = task1(CSVdict)
    print(OP1[0]['afghanistan'])
    print(OP1[1]['afghanistan'])

    #To finish part3 of OP1, txt file is needed
    #print(OP1[2]['afghanistan'])

'''Task functions'''


def task1(CSVdict: dict) -> list:
    country_to_hospitals = {}
    country_to_death = {}
    country_to_covid_stroke = {}
    for country, hospital, death in zip(CSVdict['country'], CSVdict['hospital_id'], CSVdict['no_of_deaths_in_2022']):
        if country in country_to_hospitals:
            country_to_hospitals[country].append(hospital)
            country_to_death[country].append(death)
        else:
            country_to_hospitals.update({country: [hospital]})
            country_to_death.update({country: [death]})

    return [country_to_hospitals, country_to_death, country_to_covid_stroke]



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
    return numerator / denumerator

# Variance
def get_variance(data_set: list) -> float:
    set_len = len(data_set)
    set_mean = 0
    numerator = 0
    for i in range(set_len):
        set_mean += data_set[i]
    for i in range (set_len):
        numerator += (data_set[i] - set_mean) ** 2
    return numerator / (set_len - 1)

# Average Percentage Change
def get_pcad(ave_death_2022: int, ave_death_2023: int) -> int:
    return (ave_death_2023 - ave_death_2022) / ave_death_2022


'''Temp Test'''


print(main('Project2/hospital_data.csv', 'Project2/disease.txt'))