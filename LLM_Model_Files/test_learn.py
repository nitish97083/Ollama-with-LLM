# 1. Define the lambda function
get_review = lambda x: x['rating'] if x['rating'] in rat else 'Rating is not in the list of valid ratings'


rat = [1,2,3,4,5]
# 2. Create a test dictionary
test_data = {"review": "This course is amazing!", "rating": 5}

# 3. Call the lambda just like a normal function
result = get_review(test_data)

# print(result) 
# Output: This course is amazing!

e_l = list(filter(lambda x: x if x%2==0 else None , rat))

print(e_l)  # Output: [8]

