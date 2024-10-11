'''Header Descr'''

'''Main function'''

def main(CSVfile: str, TXTfile: str):
    print("For test")
    CSVdict = read_csv_as_dict(CSVfile)

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

            # If the length is not as the header's
            if not len(values) == len(headers):
                print('ERROR: Length')
                continue
            # If there is an empty of value
            if '' in values:
                print('ERROR: None Value')
                continue

            # If there is an unique hispital ID, and 15long ID length
            # 15th long id need to be considered
            hid = values[headers.index('hospital_id')]
            if 'hospital_id' in file_dict:
                if not len(hid) == 15:
                    print('ERROR: hostital_id')
                    continue
                elif hid in file_dict['hospital_id']:
                    print('ERROR: hostital_id')
                    continue

            # If there is a negative or zero number of staff, or None value
            sno = values[headers.index('no_of_staff')]
            if 'no_of_staff' in file_dict:
                if not int(sno) > 0:
                    print('ERROR: no_of_staff')
                    continue
            
            # If there is a negative or zero number of patients, or None value
            # Not sure if the sum of patients of f and m need to be considered
            pno = values[headers.index('no_of_patients')]
            mpno = values[headers.index('male_patients')]
            fpno = values[headers.index('female_patients')]
            if 'no_of_patients' in file_dict and 'male_patients' in file_dict and 'female_patients' in file_dict:
                if not (int(pno) > 0 and int(mpno) > 0 and int(fpno) > 0):
                    print('ERROR: no_of_patients')
                    continue
                elif not (int(pno) == int(mpno) + int(fpno)):
                    print('ERROR: no_of_patients')
                    continue

            # If there is a negative or zero number of bed, or None value
            bno = values[headers.index('no_of_beds')]
            if 'no_of_beds' in file_dict:
                if not int(bno) > 0:
                    print('ERROR: no_of_beds')
                    continue

            # If there is a negative or zero number of deaths, or None value
            dno22 = values[headers.index('no_of_deaths_in_2022')]
            dno23 = values[headers.index('no_of_deaths_in_2023')]
            if 'no_of_deaths_in_2022' in file_dict and 'no_of_deaths_in_2023' in file_dict:
                if not (int(dno22) > 0 and int(dno23) > 0):
                    print('ERROR: no_of_deaths')
                    continue

            for header, value in zip(headers, values):
                file_dict[header].append(value)
    return file_dict


def validate_data(headers, values, file_dict):
    # Check for correct length of values
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