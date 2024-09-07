def main(CSVfile: str, TXTfile: str, category: str):
    
    category = category.lower()

    # Task1, OP1 = [Product ID1, Product ID2]
    OP1 = task1(CSVfile, category)
    # Task2, OP2 = [mean, median, mean absolute deviation]
    OP2 = task2(CSVfile, category, 1000)
    # Task3, [STD1, STD2, ... , STDN]
    OP3 = task3(CSVfile, 3.3, 4.3)
    # Task4, Correlation
    OP4 = task4(CSVfile, TXTfile, category)

    # Fianlly return the target values
    return OP1, OP2, OP3, OP4


''' Task Functions'''


# Function of task1, to get highest and lowest id
def task1(CSVfile: str, category: str) -> list[str]:
    # Open the product file 
    with open(CSVfile, 'r') as product_file:
        # Skip the first header line
        product_file.readline()
        # Initialise the values
        hdiscount, ldiscount = 0, 0
        # Get the highest and lowest discount and it's id
        for line in product_file:
            row = to_lower_case(line.split(','))
            if row[2] == category:
                if int(row[3]) > hdiscount or hdiscount == 0:
                    hdiscount = int(row[3])
                    hid = row[0]
                elif int(row[3]) < ldiscount or ldiscount == 0:
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
            row = to_lower_case(line.split(','))
            if row[2] == category and int(row[7]) > rating_count:
                data_set.append(int(row[4]))
        # Get the values
        mean = get_average(data_set)
        median = get_median(data_set)
        mean_absolute_deviation = get_mean_absolute_deviation(data_set)
    return [mean, median, mean_absolute_deviation]


# Function for task3
def task3(CSVfile: str, min_rating: float, max_rating: float) -> list[float]:
    temp_dict = {}
    sd_list = []
    with open(CSVfile, 'r') as product_file:
        # Skip the first header line
        product_file.readline()
        for line in product_file:
            row = to_lower_case(line.split(','))
            # Rating conditional
            if min_rating <= float(row[6]) <= max_rating:
                # Sort the values by category
                try:
                    temp_list = list(temp_dict[row[2]])
                    temp_list.append(float(row[5]))  
                except KeyError:
                    temp_list = [float(row[5])]    
                temp_dict.update({row[2]:temp_list})
    # Get the standard deviation for each list
    for row in temp_dict.values():
        sd_list.append(get_standard_deviation(row))
    # Sorted by descending order     
    sd_list.sort(reverse = True)
    return sd_list


# Function for task4 to get correlation
def task4(CSVfile: str, TXTfile: str, category: str) -> float:
    # Initialise two lists with highest and lowest discounted product
    hi_list, lo_list =  [], []
    # Open TXT file
    with open(TXTfile, 'r') as sales_file:
        for line in sales_file:
            # Get 'xxx:xxx'
            line_list = to_lower_case(line.split(','))
            # Initialise the value of the list
            hi_list.append(0)
            lo_list.append(0)
            for unit in line_list:
                # Have a slice to get the id and the number
                if unit[1:11] == task1(CSVfile, category)[0]:
                    hi_list[-1] = int(unit[13:])
                    break
                elif unit[1:11] == task1(CSVfile, category)[1]:
                    lo_list[-1] = int(unit[13:])
                    break
    cc_num = round(get_correlation_coeddicient(hi_list, lo_list), 4)
    return cc_num


''' Mathmatical Functions of the Project'''


# Function that take an input of integer list and return median value
def get_median(data_set: list[float]) -> float:
    try:
        # Get the len, midlen and sort the list
        list_len = len(data_set)
        data_set.sort()
        mid = list_len // 2
        # If the lenth of list is odd
        if list_len % 2:
            return (data_set[mid - 1] + data_set[mid]) / 2
        # If len is even
        else:
            return data_set[mid]
    except Exception:
        print("Can not get the median")
        return 0


# Function that take an int data set and return a float number
def get_average(data_set: list[float]) -> float:
        ave = sum(data_set) / len(data_set)
        return ave

# Function that to get mean absolute deviation
def get_mean_absolute_deviation(data_set: list[float]) -> float:
    try:
        data_ave = get_average(data_set)
        list_len = len(data_set)
        md_num = 0
        for i in range(list_len):
            md_num += abs(data_ave - data_set[i])
        md_num /= list_len
        return md_num
    except Exception:
        print("Can not get the mean abosulute deviation")
        return 0


# Function to get the standard deviation
def get_standard_deviation(data_set: list[float]) -> float:
    try:
        data_ave = get_average(data_set)
        list_len = len(data_set)
        sd_num = 0
        for i in range(list_len):
            sd_num += (data_ave - data_set[i]) ** 2
        sd_num /= list_len - 1
        sd_num = round(sd_num ** 0.5, 4)
        return sd_num
    except Exception:
        print("Can not get the standatf deviation")
        return 0


# Function that take two lists and return the correlation coeddicient value
def get_correlation_coeddicient(data_set_x: list, data_set_y: list) -> float:
    try:
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
    except Exception:
        print("Can not get the correlation coeddicient")
        return 0


''' Other Functions'''


# Function that implement case insensitive to a list
def to_lower_case(olist: list[str]) -> list:
    list_len = len(olist)
    for i in range(list_len):
        olist[i] = olist[i].lower()
    return olist


''' Temp Testing Part of The Project'''


OP1, OP2, OP3, OP4 = main('/Users/vincent/Desktop/Python/CITS1401_Project/Amazon product and sales data/Amazon_products.csv', '/Users/vincent/Desktop/Python/CITS1401_Project/Amazon product and sales data/Amazon_sales.txt', 'Computers&Accessories')
print(OP1)
print(OP2)
print(OP3)
print(OP4)
print(get_correlation_coeddicient([],[]))