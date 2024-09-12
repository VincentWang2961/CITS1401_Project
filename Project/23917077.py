def main(CSVfile: str, TXTfile: str, category: str):
    # Read the files
    product_list = read_file_as_list(CSVfile)
    sales_list = read_file_as_list(TXTfile)

    # File error occur if there is no valid info in the files
    if len(product_list) <= 1 or len(sales_list) == 0:
        print("[main]ERROR: An unexpected error occurred: No data avaliable.")
        return [], [], [], 0
    
    # Case insensitive for category
    category = category.lower()

    # Initialisation to prevent unexpected error
    OP1, OP2, OP3, OP4 = [], [], [], 0

    # Task1, OP1 = [Product ID1, Product ID2]
    OP1 = task1(product_list, category)
    # Task2, OP2 = [mean, median, mean absolute deviation]
    OP2 = task2(product_list, category, 1000)
    # Task3, [STD1, STD2, ... , STDN]
    OP3 = task3(product_list, 3.3, 4.3)
    # Task4, Correlation
    OP4 = task4(sales_list, OP1[0], OP1[1])

    # Eventually return the target values
    return OP1, OP2, OP3, OP4


''' Task Functions'''


# Identify Extreme Discount Prices
def task1(product_list: list, category: str) -> list[str]:
    hdiscounted, ldiscounted = None, None
    # Index
    category_index = get_index(product_list, "category")
    discounted_price_index = get_index(product_list, "discounted_price $")
    product_id_index = get_index(product_list, "product_id")
    product_list = product_list[1:]
    for row in product_list:
        # Find the category
        if category in row[category_index]:
            discounted = int(row[discounted_price_index])
            # Initialisation for high and low discounted
            if hdiscounted is None:
                hdiscounted, ldiscounted = discounted, discounted
                hid, lid = row[product_id_index], row[product_id_index]
            # To get the hdiscount and its id
            elif discounted > hdiscounted:
                hdiscounted = discounted
                hid = row[product_id_index]
            # To get the ldiscount and its id
            elif discounted < ldiscounted:
                ldiscounted = discounted
                lid = row[product_id_index]
    return [hid, lid]


# Summarize Price Distribution
def task2(product_list: list, category: str, rating_count: int) -> list[float]:
    # Index
    category_index = get_index(product_list, "category")
    rating_count_index = get_index(product_list, "rating_count")
    actual_price_index = get_index(product_list, "actual_price $")
    product_list = product_list[1:]
    data_set = []
    # Get the needed values as a list
    for row in product_list:
        if category in row[category_index] and float(row[rating_count_index]) > rating_count:
            data_set.append(float(row[actual_price_index]))
    # Get the values by mathematical functions
    mean = get_average(data_set)
    median = get_median(data_set)
    mean_absolute_deviation = get_mean_absolute_deviation(data_set, mean)
    return [mean, median, mean_absolute_deviation]


# Calculate Standard Deviation of Discounted Percentages
def task3(product_list: list, min_rating: float, max_rating: float) -> list[float]:
    temp_dict, sd_list = {}, []
    # Index
    category_index = get_index(product_list, "category")
    rating_index = get_index(product_list, "rating")
    discount_percentage_index = get_index(product_list, "discount_percentage %")
    product_list = product_list[1:]
    for row in product_list:
        # Rating conditional
        if min_rating <= float(row[rating_index]) <= max_rating:
            # Sort the values by category to make a dict
            category = row[category_index]
            discount_percent = float(row[discount_percentage_index])
            if category in temp_dict:
                temp_dict[category].append(discount_percent)  
            else:
                temp_dict[category] = [discount_percent]
    # Get the standard deviation for each list from the dict
    for row in temp_dict.values():
        sd_list.append(get_standard_deviation(row))
    sd_list.sort(reverse = True)
    return sd_list


# Correlate Sales Data
def task4(sales_list: list, hid: str, lid: str) -> float:
    # Initialise two lists with highest and lowest discounted product
    hi_list, lo_list =  [], []
    for row in sales_list:
        # Initialise the value of the list
        hi_list.append(0)
        lo_list.append(0)
        for unit in row[1:]:
            # Have a slice to get the id and the number
            if unit[1:11] == hid:
                hi_list[-1] = int(unit[13:])
                break
            elif unit[1:11] == lid:
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
    except Exception as e:
        print(f"[get_median]ERROR: An unexpected error occurred: {e}")
        return 0


# Function that take an int data set and return a float number
def get_average(data_set: list[float]) -> float:
    try:
        ave = sum(data_set) / len(data_set)
        return ave
    except Exception as e:
        print(f"[get_average]ERROR: An unexpected error occurred: {e}")
        return 0


# Function that to get mean absolute deviation
def get_mean_absolute_deviation(data_set: list[float], data_ave: float) -> float:
    try:
        md_num = sum(abs(data_ave - i) for i in data_set) / len(data_set)
        return md_num
    except Exception as e:
        print(f"[get_mean_absolute_deviation]ERROR: An unexpected error occurred: {e}")
        return 0


# Function to get the standard deviation
def get_standard_deviation(data_set: list[float]) -> float:
    try:
        #validate_data_set(data_set)
        if len(data_set) <= 1:
            raise ZeroDivisionError("The input list must have at least 2 values.")
        data_ave = get_average(data_set)
        list_len = len(data_set)
        # To get the SD and round to .4 deciaml
        sd_num = sum((data_ave - i) ** 2 for i in data_set) / (list_len - 1)
        sd_num = round(sd_num ** 0.5, 4)
        return sd_num
    except Exception as e:
        print(f"[get_standard_deviation]ERROR: An unexpected error occurred: {e}")
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
        if denumerator == 0:
            raise ZeroDivisionError("Denumerator can not be zero.")
        cc_num = numerator / denumerator
        return cc_num
    except Exception as e:
        print(f"[get_correlation_coeddicient]ERROR: An unexpected error occurred: {e}")
        return 0


''' Other Functions'''


# Function to get the data set list from a file
def read_file_as_list(file: str) -> list:
    file_list = []
    with open(file, 'r') as open_file:
        for line in open_file:
            file_list.append(line.lower().strip().split(','))
    return file_list
    

# Index function
def get_index(product_list: list, header: str) -> int:
    index = product_list[0].index(header)
    return index


''' Temp Testing Part of The Project'''


OP1, OP2, OP3, OP4 = main('/Users/vincent/Desktop/Python/CITS1401_Project/TEST/Amazon_products 2.csv', '/Users/vincent/Desktop/Python/CITS1401_Project/TEST/Amazon_sales 2.txt', 'COmputers&ACcessories')
#OP1, OP2, OP3, OP4 = main("/Users/vincent/Desktop/Python/CITS1401_Project/TEST/Amazon_products 6.csv", "/Users/vincent/Desktop/Python/CITS1401_Project/TEST/Amazon_sales 6.txt", "COmputers&ACcessories")
if OP1 == ['b07vtfn6hm', 'b08y5kxr6z'] and OP2 == [2018.8, 800, 2132.48] and OP3 == [0.297, 0.2654, 0.2311, 0.198, 0.1701, 0.1596, 0.0071] and OP4 == -0.0232:
    print("PASSED!")
else:
    print("ERROR! NOT PASSED!")
print(OP1)
print(OP2)
print(OP3)
print(OP4)