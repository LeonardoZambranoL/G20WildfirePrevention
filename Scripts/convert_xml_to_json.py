import xml.etree.ElementTree as ET
import json

# Function to convert XML to JSON
def xml_to_json(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # A simple function to iterate through all elements and build a dictionary
    def recurse_children(element):
        return {elem.tag: recurse_children(elem) if len(elem) else elem.text for elem in element}

    data = recurse_children(root)
    
    # Convert dictionary to JSON
    json_data = json.dumps(data, indent=4)
    return json_data



# Example usage
xml_file = 'data/bra_ppp_2020_UNadj_constrained.tif.aux.xml'
json_data = xml_to_json(xml_file)
print(json_data)
