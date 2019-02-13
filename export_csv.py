
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import pprint


# In[2]:


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road","Trail", "Parkway", "Commons","Ridge","Heights","Station","Plateau","Gate","Alley","Cove","Broadway","SouthWest","SouthEast","NorthEast","North","South","West","East","Highway","Way","Section","Circle","Plaza","Green","Close","Point","Speedway","Woods","Loop","Center","Wall","Esplanade","US-101","Vista","Gardens","South","View"]
ignored = ["20","525","D","H","Landing","Meridian","530","Run","Everett","Rise","3","308","101","104","2","B","99","12","f","Cleveland","Division","Yesler","Dell","9","Crescent","US-12","m","Terrace","Grove"]


# In[3]:


# mapping is the dictonary we will create based on the incorrect street types we  get from audit function this will be used in update name fucntion to get correct values
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
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
        if street_type not in expected:
            if street_type not in ignored:
                name = re.sub(street_type_re,mapping[street_type],name)

    return name


# In[4]:


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


# In[6]:


#If the element top level tag is "node" it will return a dictionary in format : {"node": .., "node_tags": ...}
#If the element top level tag is "way" it will return a dictionary in the format {"way": ..., "way_tags": ..., "way_nodes": ...}
#more details can be found in the ReportAnalysis.docx file 
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema
samplefile = 'C:\Users\Sujay\Downloads\sample.osm'
OSM_PATH = samplefile

NODES_PATH = 'C:\\Data Analysis\\SeattleData\\nodes.csv'
NODE_TAGS_PATH = 'C:\\Data Analysis\\SeattleData\\nodes_tags.csv'
WAYS_PATH = 'C:\\Data Analysis\\SeattleData\\ways.csv'
WAY_NODES_PATH = 'C:\\Data Analysis\\SeattleData\\ways_nodes.csv'
WAY_TAGS_PATH = 'C:\\Data Analysis\\SeattleData\\ways_tags.csv'

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    # YOUR CODE HERE
    if element.tag == 'node':
        for a in element.attrib:
            if a in NODE_FIELDS:
                node_attribs[a] = element.attrib[a]
                #node_attribs[a['k']] = a['v']
        id_val = node_attribs['id']
        for tag in element.iter('tag'):
            tg = {}
            tg['id'] = id_val
            #print tag.attrib['k']
            #print tag.attrib['v']
            if not PROBLEMCHARS.search(tag.attrib['k']):
                if LOWER_COLON.search(tag.attrib['k']):
                    if tag.attrib['k'] == "addr:street":
                        tg['value']  = update_name(tag.attrib['v'], mapping)
                    elif tag.attrib['k'] == "addr:postcode":
                        tg['value']  = update_postcode(tag.attrib['v'])
                    else:
                        tg['value'] = tag.attrib['v']
                    types = tag.attrib['k'].split(':',1)
                    tg['key'] =  types[1]
                    tg['type'] = types[0]
                    tg['id'] = id_val
                    tags.append(tg)
                else:
                    tg['key'] =  tag.attrib['k']
                    tg['value'] = tag.attrib['v']
                    tg['type'] = default_tag_type
                    tg['id'] = id_val
                    #print 'lower Colon else'
                    tags.append(tg)
            else:
                #print 'PROBLEMCHARS'
                None
        #print tags        
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        for a in element.attrib:
            if a in WAY_FIELDS:
                way_attribs[a] = element.attrib[a]
        id_val_way = way_attribs['id']
        cnt = 0
        
        for nd in element.iter('nd'):
            way_node = {}
            way_node['id'] = id_val_way
            way_node['node_id'] = nd.attrib['ref']
            way_node['position'] = cnt
            way_nodes.append(way_node)
            cnt +=1
            
        for tag in element.iter('tag'):
            tg_way = {}
            tg_way['id'] = id_val_way
            #print tag.attrib['k']
            #print tag.attrib['v']
            if not PROBLEMCHARS.search(tag.attrib['k']):
                if LOWER_COLON.search(tag.attrib['k']):
                    #print 'lower Colon'
                    types = tag.attrib['k'].split(':',1)
                    tg_way['key'] =  types[1]
                    tg_way['value'] = tag.attrib['v']
                    tg_way['type'] = types[0]
                    tg_way['id'] = id_val_way
                    tags.append(tg_way)
                else:
                    tg_way['key'] =  tag.attrib['k']
                    tg_way['value'] = tag.attrib['v']
                    tg_way['type'] = default_tag_type
                    tg_way['id'] = id_val_way
                    #print 'lower Colon else'
                    tags.append(tg_way)
            else:
                #print 'PROBLEMCHARS'
                None
        print way_attribs
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


#def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    #if validator.validate(element, schema) is not True:
        #field, errors = next(validator.errors.iteritems())
        #message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        #error_string = pprint.pformat(errors)
        
        #raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                #if validate is True:
                    #validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)


# In[ ]:




