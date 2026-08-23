# 1. Define the lambda function
import re


get_review = lambda x: x['rating'] if x['rating'] in rat else 'Rating is not in the list of valid ratings'


rat = [1,2,3,4,5]
# 2. Create a test dictionary
test_data = {"review": "This course is amazing!", "rating": 5}

# 3. Call the lambda just like a normal function
result = get_review(test_data)

# print(result) 
# Output: This course is amazing!

e_l = list(filter(lambda x: x if x%2==0 else None , rat))

# print(e_l)  # Output: [8]

con = ['I am working ', 'Ollama ','RAG testing ', 'Test identify the AI ','power']

def clean_text(text):
   text =  re.sub(r'\n\n+', '\n\n', text)
   text = re.sub(r'\t+', '\t',text)
   text = re.sub(r'\s+',' ',text)
   return text


user_question = "tell me about IPO Listing Soon in Aug 2026"
# text = clean_text(con)
# print(user_question[:50])
over = 5
li = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
ne_li = []
for i in range(0,len(li),over-2):
    
    ne_li.append(li[i:i+over])
    print(f" nummber is --> {i}")

print(f"new list --> {ne_li}")

#  6, 9,12,15,18