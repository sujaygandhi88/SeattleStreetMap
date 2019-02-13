
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET


# In[2]:


# This function will give us the unique users in the xml
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib:
            users.add(element.attrib['uid'])
    return users


# In[4]:


samplefile = 'C:\Users\Sujay\Downloads\sample.osm'
users = process_map(samplefile)
len(users)


# In[ ]:




