'''
CITS1401 Computational Thinking with Python
Project 2, Semester 2, 2024 - Analyzing Hospital Data

Tasks

Author: Vincent Wang(also Wenshuo Wang)
Student ID: 23917077
Date: 13 Oct 2024
'''

'''Main function'''


def main(CSVfile: str, TXTfile: str, category: str):
    OP1, OP2, OP3, OP4 = [], {}, {}, {}

    data_dict = read_csv_as_dict(CSVfile)
    data_dict = read_txt_into_dict(data_dict, TXTfile)

    if 'country' not in data_dict:
        return OP1, OP2, OP3, OP4

    OP1 = generate_country_specific_health_data(data_dict)
    OP2 = calculate_cosine_similarity(data_dict, OP1)
    OP3 = calculate_cancer_admission_variance(data_dict, category)
    OP4 = generate_hospital_category_statistics(data_dict)

    return OP1, OP2, OP3, OP4


'''Task functions'''

# TASK1: Generate Country-Specific Hospital Data
def generate_country_specific_health_data(data_dict: dict) -> list:
    # Initialisation for each dict
    country_to_hospitals = {}
    country_to_death = {}
    country_to_covid_stroke = {}
    # Header check
    country_list = data_dict['country']
    hospital_list, death_list, covid_list, stroke_list = [[0]*len(country_list) for _ in range(4)]
    if 'hospital_id' in data_dict:
        hospital_list = data_dict['hospital_id']
    if 'no_of_deaths_in_2022' in data_dict:
        death_list = data_dict['no_of_deaths_in_2022']
    if 'covid' in data_dict and 'stroke' in data_dict:
        covid_list = data_dict['covid']
        stroke_list = data_dict['stroke']
    # Setdefault and append all values
    for country, hospital, death, covid, stroke in zip(country_list, hospital_list, death_list, covid_list, stroke_list):
        country_to_hospitals.setdefault(country, []).append(hospital)
        country_to_death.setdefault(country, []).append(int(death))
        country_to_covid_stroke.setdefault(country, []).append(int(covid) + int(stroke))
    return [country_to_hospitals, country_to_death, country_to_covid_stroke]


# TASK2: Calculate Cosine Similarity
def calculate_cosine_similarity(data_dict: dict, data_list: list) -> dict:
    # Initialisation for each dict and list
    cosine_dict = {}
    # Header check
    if not data_list[1] or not data_list[2]:
        return cosine_dict
    else:
        country_list = data_dict['country']
        country_to_death_list = data_list[1]
        country_to_covid_stroke_list = data_list[2]
    # Pass the value from OP1 to get_cosine function, and put returned value into the dict
    for country in country_list:
        if not country in cosine_dict:
            death_data_set = country_to_death_list[country]
            covid_stroke_data_set = country_to_covid_stroke_list[country]
            cosine_dict[country] = round(get_cosine(death_data_set, covid_stroke_data_set), 4)
    return cosine_dict


# TASK3: Analyze Variance in Cancer Admissions
def calculate_cancer_admission_variance(data_dict: dict, category: str) -> dict:
    # Initialisation for the dicts
    variance_dict = {}
    c_hc_c_dict = {}
    # Header check
    if 'hospital_category' not in data_dict or 'cancer' not in data_dict or category not in data_dict['hospital_category']:
        return variance_dict
    else:
        country_list = data_dict['country']
        category_list = data_dict['hospital_category']
        cancer_list = data_dict['cancer']
    # Get the formated data set for the next step
    for country, hospital_category, cancer in zip(country_list, category_list, cancer_list):
        if hospital_category == category:
            c_hc_c_dict.setdefault(country, []).append(int(cancer))
    # Calculate the cancer variance
    for country, cancers in c_hc_c_dict.items():
        variance_dict[country] = get_variance(cancers)
    return variance_dict


# TASK4: Generate Hospital Category Statistics
def generate_hospital_category_statistics(data_dict: dict) -> dict:
    category_country_dict = {}
    temp_dict = {}
    # Header check
    if 'hospital_category' not in data_dict:
        return category_country_dict
    else:
        country_list = data_dict['country']
        category_list = data_dict['hospital_category']
    female_list, staff_list, death22_list, death23_list = [[0]*len(country_list) for _ in range(4)]
    if 'female_patients' in data_dict:
        female_list = data_dict['female_patients']
    if 'no_of_staff' in data_dict:
        staff_list = data_dict['no_of_staff']
    if 'no_of_deaths_in_2022' in data_dict and 'no_of_deaths_in_2023' in data_dict:
        death22_list = data_dict['no_of_deaths_in_2022']
        death23_list = data_dict['no_of_deaths_in_2023']

    # Collect and aggregate data
    for category, country, female_patients, no_of_staff, death_2022, death_2023 in zip(category_list, country_list, female_list, staff_list, death22_list, death23_list):
        item = category + country
        if item in temp_dict:
            data = temp_dict[item]
            data[0] += int(female_patients)
            data[1] += 1
            data[2] = max(data[2], int(no_of_staff))
            data[3] += int(death_2022)
            data[4] += int(death_2023)
        else:
            temp_dict[item] = [int(female_patients), 1, int(no_of_staff), int(death_2022), int(death_2023)]
    # Calculate the needed data
    for category, country in zip(category_list, country_list):
        item = category + country
        data = temp_dict[item]
        avg_patients = round(data[0] / data[1], 4)
        max_staff = data[2]
        pcad = round(get_pcad(data[3], data[4]), 4)
        category_country_dict.setdefault(category, {}).update({country: [avg_patients, max_staff, pcad]})
    return category_country_dict


'''Functional functions'''


# Function that read a CSV file and make a dict by header
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
            if not validate_data(headers, values, file_dict):
                continue
            for header, value in zip(headers, values):
                file_dict[header].append(value)
    return file_dict


# Function that validate a single line data in a dict 
def validate_data(headers: list, values: list, file_dict: dict) -> bool:
    # Convert headers and values into a dictionary
    line = dict(zip(headers, values))

    # Check for correct length of values as the header's
    if not len(values) == len(headers):
        print('ERROR: Length')
        return False
    
    if 'country' in file_dict:
        cty = line.get('country')
        if all(cha.isdigit() for cha in cty):
            print('ERROR: country')
            return False
        
    if 'hospital_category' in file_dict:
        cat = line.get('hospital_category')
        if all(cha.isdigit() for cha in cat):
            print('ERROR: hospital_category')
            return False

    # Specific checks for hospital_id
    if 'hospital_id' in file_dict:
        hid = line.get('hospital_id')
        if not len(hid) == 15 or hid in file_dict['hospital_id']:
            print('ERROR: hospital_id')
            return False
        
    # Check for no_of_staff
    if 'no_of_staff' in file_dict:
        sno = line.get('no_of_staff')
        if not sno.isdigit() or not int(sno) > 0:
            print('ERROR: no_of_staff')
            return False
    
    # Check for no_of_patients, male_patients, female_patients
    if 'no_of_patients' in file_dict:
        pno = line['no_of_patients']
        if not pno.isdigit() or not int(pno) > 0:
            print('ERROR: no_of_patients')
            return False
        if 'male_patients' in file_dict:
            mpno = line['male_patients']
            if not mpno.isdigit() or not int(mpno) > 0:
                print('ERROR: no_of_patients')
                return False
        if 'female_patients' in file_dict:
            fpno = line['female_patients']
            if not fpno.isdigit() or not int(fpno) > 0:
                print('ERROR: no_of_patients')
                return False
        if 'male_patients' in file_dict and 'female_patients' in file_dict:
            if not int(pno) >= int(fpno) + int(mpno):
                print('ERROR: no_of_patients')
                return False
    
    # Check for no_of_beds
    if 'no_of_beds' in file_dict:
        bno = line.get('no_of_beds')
        if not bno.isdigit() or not int(bno) > 0:
            print('ERROR: no_of_beds')
            return False
    
    # Check for no_of_deaths_in_2022 and no_of_deaths_in_2023
    if 'no_of_deaths_in_2022' in file_dict and 'no_of_deaths_in_2023' in file_dict:
        dno22 = line['no_of_deaths_in_2022']
        dno23 = line['no_of_deaths_in_2023']
        if not dno22.isdigit() and not dno23.isdigit() and not (int(dno22) > 0 or int(dno23) > 0):
            print('ERROR: no_of_deaths')
            return False
    
    # If there is no issues, returns True
    return True


# Function that read the txt data into the exist dict
def read_txt_into_dict(data_dict: dict, TXTfile: str) -> dict:
    if 'hospital_id' not in data_dict:
        return data_dict
    # Make a index map for hospoital ids
    index_map = {hid: index for index, hid in enumerate(data_dict['hospital_id'])}
    with open(TXTfile, 'r') as open_file:
        # Initialisation for the diseases
        disease_list = ['covid', 'stroke', 'cancer']
        for disease in disease_list:
            data_dict[disease] = [0] * len(data_dict['hospital_id'])
        for line in open_file:
            # Create the dict for each line in TXT file
            elements = line.lower().strip().split(', ')
            element_dict = {header: value.strip() for header, value in (item.split(':') for item in elements)}
            # Insert the TXT data into the main dict
            hid = element_dict['hospital_id']
            if hid in index_map:
                index = index_map[hid]
                for disease in disease_list:
                    if disease in element_dict:
                        data_dict[disease][index] = element_dict[disease]
    return data_dict


'''Mathematical finctions'''


# Cosine similarity
def get_cosine(set_x: list, set_y: list) -> float:
    try:
        # initialisation
        numerator, denumerator = 0, 0
        denumerator1, denumerator2 = 0, 0
        set_len = len(set_x)
        # Calculating cosine similarity
        for i in range(set_len):
            numerator += set_x[i] * set_y[i]
            denumerator1 += set_x[i] ** 2
            denumerator2 += set_y[i] ** 2
        denumerator = (denumerator1 ** 0.5) * (denumerator2 ** 0.5)
        return numerator / denumerator
    except:
        return 0


# Variance
def get_variance(data_set: list) -> float:
    try:
        # Initialisation
        set_len = len(data_set)
        set_mean = 0
        numerator = 0
        if set_len <= 1:
            return 0
        # Get the mean and the numerator
        set_mean = sum(data_set) / set_len
        numerator = sum((i - set_mean) ** 2 for i in data_set)
        return numerator / (set_len - 1)
    except:
        return 0


# Average Percentage Change
def get_pcad(ave_death_2022: int, ave_death_2023: int) -> int:
    try:
        if ave_death_2022 <= 0:
            return 0
        return (ave_death_2023 - ave_death_2022) / ave_death_2022 * 100
    except:
        return 0


'''Temp Test'''


#OP1, OP2, OP3, OP4 = main('/Users/vincent/Desktop/Python/CITS1401_Project/Project2/hospital_data.csv', '/Users/vincent/Desktop/Python/CITS1401_Project/Project2/disease.txt', 'children')
OP1, OP2, OP3, OP4 = main('/Users/vincent/Desktop/Python/CITS1401_Project/TEST2/hospital_data 11.csv', '/Users/vincent/Desktop/Python/CITS1401_Project/TEST2/disease 1.txt', 'children')

print(OP1[0]['afghanistan']) #['4eb9d3e5cf79b91', 'bba52b87bb6a32f','8a9190a50adf241']
print(OP1[1]['afghanistan']) #[20, 2, 12]
print(OP1[2]['afghanistan']) #[830, 3898, 6854]

print(len(OP2)) #32
print(OP2['afghanistan']) #0.5746
print(OP2['albania']) #0.9257

print(OP3['afghanistan']) #785004.5
print(OP3['brunei darussalam']) #24420.5

print(len(OP4['children'])) #32
print(OP4['children']['canada']) #[3925.4, 4448, 22.0588]

#print(OP1)
#print(OP2)
#print(OP3)
#print(OP4)

if OP1[0]['afghanistan'] == ['4eb9d3e5cf79b91', 'bba52b87bb6a32f','8a9190a50adf241'] and OP1[1]['afghanistan'] == [20, 2, 12] and OP1[2]['afghanistan'] == [830, 3898, 6854]:
    if len(OP2) == 32 and OP2['afghanistan'] == 0.5746 and OP2['albania'] == 0.9257:
        if OP3['afghanistan'] == 785004.5 and OP3['brunei darussalam'] == 24420.5:
            if len(OP4['children']) == 32 and OP4['children']['canada'] == [3925.4, 4448, 22.0588]:
                print('PASSED ALL')
