
# coding: utf-8

# In[153]:


import requests
import time

from datetime import datetime

def render_headlines():
    
    date_today = datetime.today().strftime('%Y-%m-%d')
    url = ('https://newsapi.org//v2/top-headlines?q=Modi&from='+ date_today + '&sortBy=popularity&apiKey=38998884556e4a2bb8d5fc4d57e8d8bc')

    headlines_list = []

    response = requests.get(url).json()
    for a in response['articles']:
        headlines_list.append(a['title'])

    headlines=list(set(headlines_list))
    #print(headlines)

    return headlines

