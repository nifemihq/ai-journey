# Create a list of squares for numbers 0–9.
squares = [x**2 for x in range(0, 10)]
print(squares)

# Convert a list of temperatures in Celsius to Fahrenheit.
celsius = [32, 76, 43, 21, 12, 34]
fahrenheit = [(temp * 9/5) + 32 for temp in celsius]
print(fahrenheit)

# exctract even numbers
numbers = [1, 2, 3, 4, 5, 76, 87, 98, 90, 54, 32, 23, 534]
even_numbers = [x for x in numbers if x % 2 == 0]
print(even_numbers)

# Get the length of each word in a sentence.
sentence = 'My name is Oluwanifemi'
sentence = sentence.split()
len_words = [len(x) for x in sentence]
print(len_words)

# Replace all negative numbers in a list with 0
numbers = [12, -12, 3, -3, 45, -45, 60, -60]
alt_numbers = [x  if x >= 0 else 0 for x in numbers]
print(alt_numbers)

# Return 'even' for even numbers, 'odd' for odd numbers in a range 0–10.
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
numbers = ['even' if x%2==0 else 'odd' for x in numbers]
print(numbers)

# Extract only the strings from a mixed list of strings and numbers.
lst = [13, 'number', 45, 'tomorrow', 'dagger', 776, 'aanu']
lst = [x for x in lst if type('ok') == type(x)]
print(lst)

# For a list of numbers, replace numbers < 10 with 'small', otherwise keep the number.
numbers = [12, 23, 3, 4, 5, 79, 7, 8, 121]
numbers = [x if x >= 10 else 'small' for x in numbers]
print(numbers)

# For each word in a list, return uppercase if it starts with a vowel.
words = ['hello', 'apple', 'elephant', 'noise', 'discipline', 'everest']
words = [x.upper() if x[0] in 'aeiou' else x for x in words]
print(words)

# Create a list of numbers 1–50 that are divisible by both 3 and 5.
numbers = [x for x in range(1, 51) if x%3 == 0 and x%5 == 0]
print(numbers)

# Flatten a 2D list: [[1, 2], [3, 4]] → [1, 2, 3, 4].
listt = [[1, 2], [3, 4]]
listt = [x for i in listt for x in i]
print(listt)

