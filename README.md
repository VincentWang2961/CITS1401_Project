# CITS1401_Project
A personal project of Python  

## Project Overview

In the rapidly expanding world of e-commerce, platforms like Amazon provide vast amounts of data that can offer valuable insights into various aspects of product performance. This project aims to analyze Amazon data for different products within specific categories, utilizing key parameters such as *product ID, product name, category, discounted price, actual price, ratings,* *rating coun*t etc., The data set includes a diverse range of categories, each with multiple products, allowing us to identify trends and patterns specific to each category. You are required to write a Python 3 program that will read two different files: a CSV file and a TXT file. Your program will perform four different tasks outlined below. While the CSV file is required to solve all the tasks (Tasks1-4), the TXT file is only required for the last task (Task 4).

After reading the CSV file, your program is required to complete the following:

### Task 1: Identify Extreme Discount Prices

Find the product ID with the highest *discounted price* and the product ID with the lowest discounted price for a specific category.

### **Task 2**: Summarize Price Distribution

Provide a summary of the ‘*actual price*’ distribution i.e., mean, median and mean absolute deviation of products for a specific category, considering only the products with a *rating count* higher than 1000.

### **Task 3**: Calculate Standard Deviation of Discounted Percentages

Calculate the standard deviation of the *discounted percentages* for products with *rating* in the range 3.3≤*rating*≤4.3, for each category.

### Task 4**: **Correlate Sales Data

Find the correlations between the sales of the products identified in Task 1 (products with highest and lowest *discounted prices* for a specific category).

### Steps:

1. Read the TXT file which contains the sales data for several years, such as 1998-2021. Each line lists product IDs and the units sold for that year. If a product ID is not mentioned in a line, it means zero units sold for that year.

2. Create two lists, one for the sales of the product with the highest discounted price and another for the sales of the product with the lowest discounted price identified in Task 1.

3. Process each line of the TXT file to determine the number of units sold each year.

4. Each list should have one entry per year, with the total number of entries matching the number of lines in the TXT file. 

5. Finally, calculate the correlation coefficient between the two sales lists.
