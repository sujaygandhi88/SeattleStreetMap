
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET


# In[3]:


#!/usr/bin/env python

import xml.etree.cElementTree as ET
import pprint
import re
"""
Key type functio n returns four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.

"""
samplefile = 'C:\Users\Sujay\Downloads\sample.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']):
            if 'lower' not in keys:
                keys['lower'] = 1
            else:
                keys['lower'] +=1
        elif lower_colon.search(element.attrib['k']):
            if 'lower_colon' not in keys:
                keys['lower_colon'] = 1
            else:
                keys['lower_colon'] +=1
        elif problemchars.search(element.attrib['k']):
            if 'problemchars' not in keys:
                keys['problemchars'] = 1
            else:
                keys['problemchars'] +=1
        else:
            if 'other' not in keys:
                keys['other'] = 1
            else:
                keys['other'] +=1
        # YOUR CODE HERE
    return keys
    



def process_map_type(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():

    keys = process_map_type(samplefile)
    pprint.pprint(keys)


if __name__ == "__main__":
    test()


# In[ ]:




