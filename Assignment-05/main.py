# Task 1 Imports
import math_utils
from math_utils import square

print("----- Math Utils -----")
print("Add:", math_utils.add(10, 5))
print("Subtract:", math_utils.subtract(10, 5))
print("Square:", square(6))


# Task 2 Imports
import string_utils

print("\n----- String Utils -----")
text = "python programming language"

print("Capitalized:", string_utils.capitalize_words(text))
print("Reversed:", string_utils.reverse_string(text))
print("Word Count:", string_utils.word_count(text))


# Task 3 & 4 Package Imports
import shop_package.discount as disc
from shop_package.billing import calculate_total, apply_tax

print("\n----- Shop Package -----")

price = 1000

print("10% Discount:", disc.apply_discount(price, 10))
print("Flat Discount:", disc.flat_discount(price))

prices = [100, 200, 300]

total = calculate_total(prices)
print("Total Bill:", total)

print("Total With Tax:", apply_tax(total))