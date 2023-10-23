import google.generativeai as palm
import os

API_KEY = 'AIzaSyDxNAyUjWXMJ6fpqFcOnAphr_AlF39RhHI'
palm.configure(api_key= API_KEY)

response = palm.chat(messages=["Hello."])
print(response.last) #  'Hello! What can I help you with?'
#response.reply("Can you tell me a joke?")
