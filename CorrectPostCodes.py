
# coding: utf-8

# In[10]:


import xml.etree.ElementTree as ET
import pprint
import re


# In[7]:


#is_zipcode function looks at the attribute k if k=" addr:postcode"
#audit_postcode function looks at the first two digits of the value to see if they are numbers and if they are 98 as zip code in seattle start with 98. 

from collections import defaultdict
samplefile = 'C:\Users\Sujay\Downloads\sample.osm'
def audit_postcode(postcodes, zipcode):
    twoDigits = zipcode[0:2]
    
    if not twoDigits.isdigit():
        postcodes[twoDigits].add(zipcode)
    
    elif twoDigits != '98':
        postcodes[twoDigits].add(zipcode)
        
def is_valid_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_post(osmfile):
    osm_file = open(osmfile, "r")
    postcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_valid_postcode(tag):
                    audit_postcode(postcodes,tag.attrib['v'])

    return postcodes

wa_postcode = audit_post(samplefile)


# In[8]:


pprint.pprint(dict(wa_postcode))


# In[11]:


# this function will update the postcodes to correct values
def update_postcode(postcode):
    digitpost = (re.findall(r'\d+', postcode)) #get all digits
    if digitpost:
        if digitpost.__len__() == 2:
            return (re.findall(r'\d+', postcode))[0] + "-" +(re.findall(r'\d+', postcode))[1] # if more than 1 then will create one with - in between
        else:
            if postcode[0] == 'V' or postcode[0] == '1' or postcode[0] == '0':
                return None
            else:
                return (re.findall(r'\d+', postcode))[0]

for street_type, ways in wa_postcode.iteritems():
    for name in ways:
        better_name = update_postcode(name)
        print name, "=>", better_name


# In[ ]:




