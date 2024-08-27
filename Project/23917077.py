def main(CSVfile: str, TXTfile: str, category: str):
    ''' 
    OP1 = [Product ID1, Product ID2]
    OP2 = [mean, median, mean absolute deviation]
    OP3 = [STD1, STD2, ... , STDN]
    OP4 = Correlation
    '''
    OP1, OP2, OP3 = [], [], []
    OP4 = 0.0
    
    # Task1
    OP1 = task1(CSVfile, category)

    # Task2
    OP2 = task2(CSVfile, category, 1000)
    
    # Task3
    OP3 = task3(CSVfile, category, 3.3, 4.3)

    # Fianlly return the target values
    return OP1, OP2, OP3, OP4


''' Task Functions'''


# Function of task1, to get highest and lowest id
# To do: task1 note unfinished
#        need to figure out why the output is not as the expected with highest to be the lowest
def task1(CSVfile: str, category: str) -> list[str]:
    # Open the file Amazon_products.csv
    # product_id,product_name,category,discounted_price $,actual_price $,discount_percentage %,rating,rating_count
    with open(CSVfile, 'r') as product_file:
        # Skip the first header line
        product_file.readline()
        # Initialise values
        hdiscount = 0
        for line in product_file:
            row = line.rstrip().split(',')
            if row[2] == category:
                hdiscount = int(row[3])
                break
        ldiscount = hdiscount
        hid, lid = '', ''
        # Get the highest and lowest discount and it's id
        for line in product_file:
            row = line.rstrip().split(',')
            if row[2] == category:
                if int(row[3]) > hdiscount:
                    hdiscount = int(row[3])
                    hid = row[0]
                elif int(row[3]) < ldiscount:
                    ldiscount = int(row[3])
                    lid = row[0]
    return [hid, lid]


# Function for task2
def task2(CSVfile: str, category: str, rating_count: int) -> list[float]:
    data_set = []
    with open(CSVfile, 'r') as product_file:
        # Skip the first header line
        product_file.readline()
        # Get the needed values as a list
        for line in product_file:
            row = line.rstrip().split(',')
            if row[2] == category and int(row[7]) > rating_count:
                data_set.append(int(row[4]))
        # Get the values
        mean = get_average(data_set)
        median = get_median(data_set)
        mean_absolute_deviation = get_mean_absolute_deviation(data_set)
    return [mean, median, mean_absolute_deviation]


# Function for task3
def task3(CSVfile: str, category: str, min_rating: float, max_rating: float) -> list[float]:
    temp_dict = {}
    sd_list = []
    with open(CSVfile, 'r') as product_file:
        # Skip the first header line
        product_file.readline()
        for line in product_file:
            row = line.rstrip().split(',')
            # Rating conditional
            if min_rating <= float(row[6]) <= max_rating:
                # Sort the values by category
                # Might be reversed with more simple conditional
                try:
                    temp_list = list(temp_dict[row[2]])
                    temp_list.append(float(row[5]))  
                except KeyError:
                    temp_list = [float(row[5])]    
                temp_dict.update({row[2]:temp_list})
    # Get the standard deviation for each list
    for row in temp_dict.values():
        #print(row)
        sd_list.append(get_standard_deviation(row))     
    sd_list.sort(reverse = True)
    return sd_list


''' Mathmatical Part of the Project'''


# Function that take an input of integer list and return median value
def get_median(data_set: list[float]) -> float:
    # Get the number of data set
    list_len = len(data_set)
    # Sort the list
    data_set.sort()
    # If n is odd
    if list_len % 2:
        median_num = data_set[int((list_len + 1) / 2) - 1]
        return median_num
    # If n is even
    else:
        median_num = (data_set[int(list_len / 2) - 1] + data_set[int(list_len / 2 + 1) - 1]) / 2
        return median_num


# Function that take an int data set and return a float number
def get_average(data_set: list[float]) -> float:
    ave = sum(data_set) / len(data_set)
    return ave


# Function that to get mean absolute deviation
def get_mean_absolute_deviation(data_set: list[float]) -> float:
    data_ave = get_average(data_set)
    list_len = len(data_set)
    md_num = 0
    for i in range(list_len):
        md_num += abs(data_ave - data_set[i])
    md_num /= list_len
    return md_num


# Function to get the standard deviation
def get_standard_deviation(data_set: list[float]) -> float:
    data_ave = get_average(data_set)
    list_len = len(data_set)
    sd_num = 0
    for i in range(list_len):
        sd_num += (data_ave - data_set[i]) ** 2
    sd_num /= list_len - 1
    sd_num = sd_num ** 0.5
    sd_num = round(sd_num, 4)
    return sd_num


# Function that take two lists and return the correlation coeddicient value
def get_correlation_coeddicient(data_set_x: list, data_set_y: list) -> float:
    # Set the ave values of x and y
    ave_x, ave_y = get_average(data_set_x), get_average(data_set_y)
    # Initialise variables of numerator and denumerator
    numerator = 0
    denumerator_temp1, denumerator_temp2 = 0, 0
    list_len = len(data_set_x)
    # Get values by throughout two lists
    for i in range(list_len):
        numerator += (data_set_x[i] - ave_x) * (data_set_y[i] - ave_y)
        denumerator_temp1 += (data_set_x[i] - ave_x) ** 2
        denumerator_temp2 += (data_set_y[i] - ave_y) ** 2
    denumerator = (denumerator_temp1 * denumerator_temp2) ** 0.5
    cc_num = numerator / denumerator
    return cc_num


# Maybe there is a function that convert a list into an int list needed?


''' Temp Testing Part of The Project'''


OP1, OP2, OP3, OP4 = main('/Users/vincent/Desktop/Python/CITS1401_Project/Amazon product and sales data/Amazon_products.csv', '', 'Computers&Accessories')
print(OP1)
print(OP2)
print(OP3)
print(OP4)


# For temp test
#print(get_median([1, 2, 3, 4, 5]))
#print(get_average(['1', 1, 3, 4]))
#print(get_mean_absolute_deviation([1, 2, 3, 4, 5]))
#print(get_square_root(6))
#print(get_standard_deviation([1, 2, 3, 4, 5]))
#print(get_correlation_coeddicient([1, 4, 6, 7, 1],[2, 5, 7, 8, 1]))
