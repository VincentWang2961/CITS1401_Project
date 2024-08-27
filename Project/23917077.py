def main():
    # Open the file Amazon_products.csv
    # product_id,product_name,category,discounted_price $,actual_price $,discount_percentage %,rating,rating_count
    with open("/Users/vincent/Desktop/Python/CITS1401_Project/Project/Amazon_products.csv", "r") as file1:
        # Skip the first line
        file1.readline()
        # Initialise values
        hdiscount = int(file1.readline().rstrip().split(",")[3])
        ldiscount = hdiscount
        hid, lid = '', ''
        # Get the highest and lowest discount and it's id
        for line in file1:
            row = line.rstrip().split(",")
            if int(row[3]) > hdiscount:
                hdiscount = int(row[3])
                hid = row[0]
            elif int(row[3]) < ldiscount:
                ldiscount = int(row[3])
                lid = row[0]

        # Print values for test
        #print(f"Product ID: {hid}, Discounted price: {hdiscount}")
        #print(f"Product ID: {lid}, Discounted price: {ldiscount}")
 

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
    sum = 0.0
    for i in data_set:
        sum += i
    ave = sum / len(data_set)
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


# Function that get a approximate square root by using Newton's method
def get_square_root(num: float) -> float:
    # Inilialise guess value
    guess_value = num / 2
    # Set the accuracy
    accuracy = 10 ** -10
    while abs(guess_value ** 2 - num) > accuracy:
        guess_value -= (guess_value ** 2 - num) / (2 * guess_value)
    return guess_value


# Function
def get_standard_deviation(data_set: list[float]) -> float:
    data_ave = get_average(data_set)
    list_len = len(data_set)
    sd_num = 0
    for i in range(list_len):
        sd_num += (data_ave - data_set[i]) ** 2
    sd_num /= list_len - 1
    sd_num = get_square_root(sd_num)
    return sd_num


# Maybe there is a function that convert a list into an int list needed?


#main()
#print(get_median([1, 2, 3, 4, 5]))
#print(get_average(['1', 1, 3, 4]))
#print(get_mean_absolute_deviation([1, 2, 3, 4, 5]))
print(get_square_root(6))