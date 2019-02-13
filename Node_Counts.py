
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET


# In[2]:


# This function will help us in getting the counts of tags in the xml file
def count_tags(filename):
        # YOUR CODE HERE
        tags = {}
        for event,elem in ET.iterparse(filename):
            if elem.tag not in tags:
                tags[elem.tag] = 1
            else:
                tags[elem.tag] += 1
        return tags


# In[3]:


samplefile = 'C:\Users\Sujay\Downloads\sample.osm'
tags = count_tags(samplefile)
print tags


# In[ ]:




