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
        print(f"Product ID: {hid}, Discounted price: {hdiscount}")
        print(f"Product ID: {lid}, Discounted price: {ldiscount}")
 

# Function that take an input of integer list and return median value
def get_median(data_set: list):
    # Get the number of data set
    n = len(data_set)
    # Sort the list
    data_set.sort()
    # If n is odd
    if n % 2:
        return data_set[int((n + 1) / 2) - 1]
    # If n is even
    else:
        return (data_set[int(n / 2) - 1] + data_set[int(n / 2 + 1) - 1]) / 2



#main()
print(get_median([1, 2, 3, 4, 5, 6]) + 1)