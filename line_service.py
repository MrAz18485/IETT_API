# Displays general information about given bus line

import zeep
import json
import lxml.etree
from utils.functions import special_char_upper_func, convert_etree_tags_to_english
wsdl = "xml/line_service.xml"

line_service_tag_dict = {"HAT_KODU": "LINE_CODE", "HAT_ADI": "LINE_NAME", "TAM_HAT_ADI": "FULL_LINE_NAME", "HAT_DURUMU": "LINE_STATUS", "BOLGE": "ZONE", "SEFER_SURESI": "TRAVEL_TIME"}

def take_line_code(line_code_input):
    line_code = special_char_upper_func(line_code_input)
    return line_code

def soap_call(line_code):
    client = zeep.Client(wsdl=wsdl)
    line_service_response = client.service.HatServisi_GYY(line_code) # returns lxml.etree._Element

    if len(line_service_response) == 0:
        print("Bus line not found")
        exit()
    return line_service_response

def print_elements(buffer):
    for table in buffer:
        print()
        for key, value in table.items():
            print(f"{key}: {value}")

def main():
    try:
        line_code = take_line_code(input("Enter bus line code (leave empty for all lines): "))
        
        line_service_response = soap_call(line_code)
        
        line_service_list = convert_etree_tags_to_english(line_service_response, line_service_tag_dict)
        
        print_elements(line_service_list)
    except ValueError as val_error_exc:
        print(val_error_exc)

if __name__ == "__main__": # to prevent accidental execution when imported
    main() 