# import os
# from dotenv import load_dotenv

# # Load the .env file from the current directory
# load_dotenv()

# # Fetch the variables
# db_url = os.getenv("DATABASE_URL")
# api_key = os.getenv("API_KEY")

# print(f"URL: {db_url}")
# print(f"Key: {api_key}");

import os

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("LANGSMITH_API_KEY")
end_point = os.getenv("LANGSMITH_ENDPOINT")

# api_key = os.getenv("API_KEY")

print(f"end_point: {end_point}")
print(f"Key: {api_key}");

