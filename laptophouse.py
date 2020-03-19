#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup


# In[2]:


page = requests.get("https://www.laptophouse.sg")


# In[3]:


obj = BeautifulSoup(page.text, 'html.parser')


# In[4]:


titles = []
links = []
images_url = []
products = []


# In[5]:


for title in obj.find_all('h2', class_='woocommerce-loop-product__title'):
    titles.append(title.text)
print(titles)


# In[6]:


for link in obj.findAll('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link'):
    links.append(link.get('href'))


# In[7]:


for image in obj.findAll('img', class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail'):
    images_url.append(image.get('src'))
print(len(images_url))


# In[8]:


import re


# In[9]:


for i in range(len(images_url)):
    page = requests.get(links[i])
    obj = BeautifulSoup(page.text, 'html.parser')
    details = []
    for specific in obj.find_all('p'):
        details.append(specific.text)
    spec = re.split('\n',details[2])
    if len(spec) >= 8:
        products.append(
        {
            'title':titles[i],
            'price':details[0],
            'processor':spec[3].replace("Processor: ",""),
            'ram':spec[4].replace("RAM: ",""),
            'graphics':spec[5].replace("Graphics: ",""),
            'storage':spec[6].replace(" HDD: ",""),
            'img_url':images_url[i]
        })


# In[11]:


products


# In[14]:


import json


# In[15]:


f=open('laptophouse.json','w')
json.dump(products,f)
f.close()


# In[ ]:




