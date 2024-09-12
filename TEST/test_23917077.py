def main(CSVfile: str, TXTfile: str, category: str):
    # Case insensitive
    category = category.lower()

    # Read the files
    product_list = read_file(CSVfile)
    sales_list = read_file(TXTfile)
    # Task1, OP1 = [Product ID1, Product ID2]
    OP1 = task1(product_list[1:], category)
    # Task2, OP2 = [mean, median, mean absolute deviation]
    OP2 = task2(product_list[1:], category, 1000)
    # Task3, [STD1, STD2, ... , STDN]
    OP3 = task3(product_list[1:], 3.3, 4.3)
    # Task4, Correlation
    OP4 = task4(product_list[1:], sales_list, category)

    # Fianlly return the target values
    return OP1, OP2, OP3, OP4


''' Task Functions'''


# Function for task1, to get highest and lowest id
def task1(product_file: list, category: str) -> list[str]:
    hdiscount, ldiscount = None, None
    for line in product_file:
        row = line.lower().split(',')
        # Find the category
        if category in row[2]:
            discount = int(row[3])
            # To get the hdiscount and its id
            if hdiscount is None or discount > hdiscount:
                hdiscount = discount
                hid = row[0]
            # To get the ldiscount and its id
            elif ldiscount is None or discount < ldiscount:
                ldiscount = discount
                lid = row[0]
    return [hid, lid]


# Function for task2
def task2(product_file: list, category: str, rating_count: int) -> list[float]:
    data_set = []
    # Get the needed values as a list
    for line in product_file:
        row = line.lower().split(',')
        if category in row[2] and int(row[7]) > rating_count:
            data_set.append(int(row[4]))
    # Get the values
    mean = get_average(data_set)
    median = get_median(data_set)
    mean_absolute_deviation = get_mean_absolute_deviation(data_set)
    return [mean, median, mean_absolute_deviation]


# Function for task3
def task3(product_file: list, min_rating: float, max_rating: float) -> list[float]:
    temp_dict = {}
    sd_list = []
    for line in product_file:
        row = line.lower().split(',')
        # Rating conditional
        if min_rating <= float(row[6]) <= max_rating:
            # Sort the values by category to make a dict
            category = row[2]
            discount_percent = float(row[5])
            if category in temp_dict:
                temp_dict[category].append(discount_percent)  
            else:
                temp_dict[category] = [discount_percent]
    # Get the standard deviation for each list in the dict
    for row in temp_dict.values():
        sd_list.append(get_standard_deviation(row))
    sd_list.sort(reverse = True)
    return sd_list


# Function for task4 to get correlation
def task4(product_file: list, sales_file: list, category: str) -> float:
    # Initialise two lists with highest and lowest discounted product
    hi_list, lo_list =  [], []
    for line in sales_file:
        line_list = line.lower().split(',')
        # Initialise the value of the list
        hi_list.append(0)
        lo_list.append(0)
        for unit in line_list:
            # Have a slice to get the id and the number
            if unit[1:11] == task1(product_file, category)[0]:
                hi_list[-1] = int(unit[13:])
                break
            elif unit[1:11] == task1(product_file, category)[1]:
                lo_list[-1] = int(unit[13:])
                break
    cc_num = round(get_correlation_coeddicient(hi_list, lo_list), 4)
    return cc_num


''' Mathematical Functions of the Project '''


# Function that take an input of integer list and return median value
def get_median(data_set: list[float]) -> float:
    try:
        # Get the len, midlen and sort the list
        list_len = len(data_set)
        data_set.sort()
        mid = list_len // 2
        # If the lenth of list is odd
        if list_len % 2:
            return data_set[mid]
        # If len is even
        else:
            return (data_set[mid - 1] + data_set[mid]) / 2
    except:
        print("[get_median]ERROR! Can not get the median!")
        return 0


# Function that take an int data set and return a float number
def get_average(data_set: list[float]) -> float:
        try:
            ave = sum(data_set) / len(data_set)
            return ave
        except ZeroDivisionError:
            print("[get_average]ERROR! Division by zero!")
            return 0
        except:
            print("[get_average]ERROR! Can not get the averange!")
            return 0


# Function that to get mean absolute deviation
def get_mean_absolute_deviation(data_set: list[float]) -> float:
    try:
        data_ave = get_average(data_set)
        md_num = sum(abs(data_ave - i) for i in data_set) / len(data_set)
        return md_num
    except ZeroDivisionError:
        print("[get_mean_absolute_devisation]ERROR! Division by zero!")
    except:
        print("[get_mean_absolute_devisation]ERROR! Can not get the mean abosulute deviation!")
        return 0


# Function to get the standard deviation
def get_standard_deviation(data_set: list[float]) -> float:
    try:
        data_ave = get_average(data_set)
        list_len = len(data_set)
        sd_num = sum((data_ave - i) ** 2 for i in data_set) / (list_len - 1)
        sd_num = round(sd_num ** 0.5, 4)
        return sd_num
    except ZeroDivisionError:
        print("[get_standard_deviation]ERROR! Division by zero!")
        return 0
    except:
        print("[get_standard_deviation]ERROR! Can not get the standatf deviation!")
        return 0


# Function that take two lists and return the correlation coeddicient value
def get_correlation_coeddicient(data_set_x: list, data_set_y: list) -> float:
    try:
        # Set the ave values of x and y
        ave_x, ave_y = get_average(data_set_x), get_average(data_set_y)
        # Initialisation
        numerator, sum_sq_x, sum_sq_y = 0, 0, 0
        for x, y in zip(data_set_x, data_set_y):
            numerator += (x - ave_x) * (y - ave_y)
            sum_sq_x += (x - ave_x) ** 2
            sum_sq_y += (y - ave_y) ** 2
        denumerator = (sum_sq_x * sum_sq_y) ** 0.5
        cc_num = numerator / denumerator
        return cc_num
    except ZeroDivisionError:
        print("[get_correlation_coeddicient]ERROR! Division by zero!")
        return 0
    except:
        print("[get_correlation_coeddicient]ERROR! Can not get the correlation coeddicient!")
        return 0


''' Other Functions'''


# Function to get the info list from a file
def read_file(file: str) -> list:
    file_list = []
    with open(file) as open_file:
        for line in open_file:
            file_list.append(line)
    return file_list



''' Temp Testing Part of The Project'''


OP1, OP2, OP3, OP4 = main('/Users/vincent/Desktop/Python/CITS1401_Project/Amazon product and sales data/Amazon_products.csv', '/Users/vincent/Desktop/Python/CITS1401_Project/Amazon product and sales data/Amazon_sales.txt', 'COmputers&Accessories')
if OP1 == ['b07vtfn6hm', 'b08y5kxr6z'] and OP2 == [2018.8, 800, 2132.48] and OP3 == [0.297, 0.2654, 0.2311, 0.198, 0.1701, 0.1596, 0.0071] and OP4 == -0.0232:
    print("PASSED!")
else:
    print("ERROR! NOT PASSED!")