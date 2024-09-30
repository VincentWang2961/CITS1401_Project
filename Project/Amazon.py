def main(CSVfile: str, TXTfile: str, category: str):
    # Read the files
    product_list = read_file_as_list(CSVfile)
    sales_list = read_file_as_list(TXTfile)

    # File error occur if there is no valid info in the files
    if len(product_list) <= 1 or len(sales_list) == 0:
        print("[main]ERROR: An unexpected error occurred: No data avaliable.")
        return [], [], [], 0
    
    # Index
    index_dict = {}
    for header in product_list[0]:
        index_dict.update({header: product_list[0].index(header)})
    
    # Case insensitive for category
    category = category.lower()

    # Initialisation to prevent unexpected error
    OP1, OP2, OP3, OP4 = [], [], [], 0

    # Task1, OP1 = [Product ID1, Product ID2]
    OP1 = find_extreme_discount_prices(product_list[1:], category, index_dict)
    # Task2, OP2 = [mean, median, mean absolute deviation]
    OP2 = summarize_price_statistics(product_list[1:], category, 1000, index_dict)
    # Task3, [STD1, STD2, ... , STDN]
    OP3 = calculate_discount_std_deviation(product_list[1:], 3.3, 4.3, index_dict)
    # Task4, Correlation
    OP4 = correlate_sales_data(sales_list, OP1[0], OP1[1])

    # Eventually return the target values
    return OP1, OP2, OP3, OP4


''' Task Functions'''


# TASK1: Identify Extreme Discount Prices
def find_extreme_discount_prices(product_list: list, category: str, index_dict: dict) -> list[str]:
    hdiscounted, ldiscounted = None, None
    hid, lid = None, None
    for row in product_list:
        # Find the category
        if category == row[index_dict["category"]]:
            discounted = int(row[index_dict["discounted_price $"]])
            # Initialisation for high and low discounted
            if hdiscounted is None:
                hdiscounted, ldiscounted = discounted, discounted
                hid = row[index_dict["product_id"]]
                lid = hid
            # To get the hdiscount and its id
            elif discounted > hdiscounted:
                hdiscounted = discounted
                hid = row[index_dict["product_id"]]
            # To get the ldiscount and its id
            elif discounted < ldiscounted:
                ldiscounted = discounted
                lid = row[index_dict["product_id"]]
    return [hid, lid]


# TASK2: Summarize Price Distribution
def summarize_price_statistics(product_list: list, category: str, rating_count: int, index_dict: dict) -> list[float]:
    data_set = []
    # Get the needed values as a list
    for row in product_list:
        if category == row[index_dict["category"]] and float(row[index_dict["rating_count"]]) > rating_count:
            data_set.append(float(row[index_dict["actual_price $"]]))
    # Get the values by mathematical functions
    mean = get_average(data_set)
    median = get_median(data_set)
    mean_absolute_deviation = get_mean_absolute_deviation(data_set, mean)
    return [mean, median, mean_absolute_deviation]


# TASK3: Calculate Standard Deviation of Discounted Percentages
def calculate_discount_std_deviation(product_list: list, min_rating: float, max_rating: float, index_dict: dict) -> list[float]:
    temp_dict, sd_list = {}, []
    for row in product_list:
        # Rating conditional
        if min_rating <= float(row[index_dict["rating"]]) <= max_rating:
            # Sort the values by category to make a dict
            category = row[index_dict["category"]]
            discount_percent = float(row[index_dict["discount_percentage %"]])
            if category in temp_dict:
                temp_dict[category].append(discount_percent)  
            else:
                temp_dict[category] = [discount_percent]
    # Get the standard deviation for each list from the dict
    for row in temp_dict.values():
        sd_list.append(get_standard_deviation(row))
    sd_list.sort(reverse = True)
    return sd_list


# TASK4: Correlate Sales Data
def correlate_sales_data(sales_list: list, hid: str, lid: str) -> float:
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
    except Exception:
        return 0


# Function that take an int data set and return a float number
def get_average(data_set: list[float]) -> float:
    try:
        ave = sum(data_set) / len(data_set)
        return ave
    except Exception:
        return 0


# Function that to get mean absolute deviation
def get_mean_absolute_deviation(data_set: list[float], data_ave: float) -> float:
    try:
        md_num = sum(abs(data_ave - i) for i in data_set) / len(data_set)
        return md_num
    except Exception:
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
    except Exception:
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
    except Exception:
        return 0


''' Other Functions'''


# Function to get the data set as a list from a file
def read_file_as_list(file: str) -> list:
    file_list = []
    with open(file, 'r') as open_file:
        for line in open_file:
            file_list.append(line.lower().strip().split(','))
    return file_list