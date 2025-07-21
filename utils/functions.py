from lxml import etree
import lxml

# to convert some of the turkish lowercase characters to their corresponding upper case pairs
def special_char_upper_func(param):
    special_chars = {"ğ":"Ğ", "ü":"Ü", "i":"İ", "ş":"Ş", "ö":"Ö", "ç":"Ç"}
    for key, value in special_chars.items():
        param = param.replace(key, value)
    return param.upper()

# Replaces keyword with corresponding value in dict_to_search
# Example: keyword = abc, dict_to_search = {"abc":"def"}
# result = replace_keyword(keyword, dict_to_search) => result = "def"
def replace_keyword(keyword, dict_to_search):
    for key in dict_to_search:
        if key == keyword:
            return dict_to_search[key]
    raise KeyError("Matching key not found! This shouldn't have happened, there could be an issue with SOAP response, or dictionary passed as parameter.")

# converts given input to ms
# Example: /DateTime(number)/, extracts number
def ms_parser(line):
    startidx = -1
    endidx = -1

    for i in range(len(line)):
        if (line[i] == '('):
            startidx = i
        elif (line[i] == ')'):
            endidx = i
    date_to_ms = int(line[startidx+1:endidx])
    return date_to_ms

def convert_etree_tags_to_english(response_list, keys_dictionary):
    outp_buffer = []
    for table in response_list:
        if isinstance(table, lxml.etree._Element) == False:
            raise TypeError(f"Invalid type {type(table)} passed to parse_xml function")
        updated_dict = {}
        for element in table:
            updated_dict[replace_keyword(element.tag, keys_dictionary)] = element.text
        outp_buffer.append(updated_dict)
    return outp_buffer

def convert_dict_keys_to_english(response_list, keys_dictionary):
    outp_buffer = []
    for element in response_list:
        updated_dict = {}
        for key in element.keys():
            updated_dict[replace_keyword(key, keys_dictionary)] = element[key]
        outp_buffer.append(updated_dict)
    return outp_buffer

def etree_constructor(tables): # helper for methods below. 
    root_elem = etree.Element("NewDataSet")
    for i in range(len(tables)):
        root_elem.append(etree.Element("Table"))
    curr_table_index = 0
    for table in tables:
        for key, value in table.items():
            element = lxml.etree.Element(key)
            element.text = value
            root_elem[curr_table_index].append(element)
        curr_table_index += 1
    return root_elem

