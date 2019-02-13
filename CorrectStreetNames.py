
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET


# In[2]:


#audit_street_type function search the input string for the regex. If there is a match and it is not within the "expected" list, add the match as a key and add the string to the set.
#is_street_name function looks at the attribute k if k="addr:street"
#audit function will return the list that match previous two functions. After that, we would do a pretty print the output of the audit. With the list of all the abbreviated street types we can understand and fill-up our "mapping" dictionary as a preparation to convert these street name into proper form.

from collections import defaultdict
import re
import pprint
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
samplefile = 'C:\Users\Sujay\Downloads\sample.osm'
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road","Trail", "Parkway", "Commons","Ridge","Heights","Station","Plateau","Gate","Alley","Cove","Broadway","SouthWest","SouthEast","NorthEast","North","South","West","East","Highway","Way","Section","Circle","Plaza","Green","Close","Point","Speedway","Woods","Loop","Center","Wall","Esplanade","US-101","Vista","Gardens","South","View"]
ignored = ["20","525","D","H","Landing","Meridian","530","Run","Everett","Rise","3","308","101","104","2","B","99","12","f","Cleveland","Division","Yesler","Dell","9","Crescent","US-12","m","Terrace","Grove"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


# In[3]:


st_types = audit(samplefile)


# In[4]:


# mapping is the dictonary we will create based on the incorrect street types we  get from audit function this will be used in update name fucntion to get correct values
mapping = { "St": "Street",
            "St.": "Street",
            "ST": "Street",
           "street": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "avenue": "Avenue",
            "Rd.": "Road",
            "Rd":  "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Bl": "Boulevard",
            "DRIVE": "Drive",
            "Dr": "Drive",
            "Ct": "Court",
            "Ct.": "Court",
            "Pl": "Place",
            "Sq": "Square",
            "La": "Lane",
            "Ln": "Lane",
            "Tr": "Trail",
            "Pkwy": "Parkway",
            "Pkwy.": "Parkway",
            "Cmns": "Commons",
            "SW": "SouthWest",
            "Southwest":"SouthWest",
           "Southeast": "SouthEast",
            "NE": "NorthEast",
           "Northeast": "NorthEast",
           "Northwest": "NorthWest",
           "NW": "NorthWest",
            "S": "South",
            "S.": "South",
           "south": "South",
           "N": "North",
           "W": "West",
           "SE": "SouthEast",
           "Hwy": "Highway",
           "E": "East",
           "WY": "Way",
           "20th": "20",
           "44th": "44",
           "WA)" : "WA",
           "98296": "",
           "Wood": "Woods",
           "FIXME": "",
           "WA-906": "WA",
           "WA-507": "WA"
            }
# this function will replace the incorrect street name with the correct one mentioned in Mapping dictonary, it will ignore values from expected and ignored list.
def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        print street_type
        if street_type not in expected:
            if street_type not in ignored:
                name = re.sub(street_type_re,mapping[street_type],name)

    return name


# In[5]:


for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name


# In[ ]:




