import lxml.etree
import zeep
import json
import os
import lxml

from utils.functions import special_char_upper_func, convert_etree_tags_to_english

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

archive_tag_dict = {"ID": "ID", "NARSIVGOREVID": "ARCHIVE_MISSION_ID", "NKAYITGUNU": "REGISTER_DATE", "SHATKODU": "LINE_CODE", "SGUZERGAHKODU": "ROUTE_CODE", "SKAPINUMARA": "DOOR_NUMBER",
                    "DTBASLAMAZAMANI": "START_TIME", "DTBITISZAMANI": "END_TIME", "SGOREVDURUM": "MISSION_STATUS", "NGOREVID": "MISSION_ID", "DTPLANLANANBASLANGICZAMANI": "PLANNED_START_TIME", 
                    "DTDUZENLENENBASLANGICZAMANI": "EDITED_START_TIME"}

def validate_date_input(date_input):
    if len(date_input) != 8 or date_input.isnumeric() == False:
        raise ValueError("Incorrect format")        
    return True

def soap_call(date):
    client = zeep.Client(wsdl=wsdl)

    response = client.service.GetIettArsivGorev_XML(date)
    
    if len(response) == 0:
        print("No data found")
        exit()

    return response

def get_specific_bus_line_data(table_list, bus_line_code):
    bus_line_data = []
    if bus_line_code == "":
        return table_list
    else:
        for table in table_list:
            if bus_line_code == table["LINE_CODE"]:
                bus_line_data.append(table)
    return bus_line_data

def print_elements(element_list):
    print()
    for table in element_list:
        for key, value in table.items():
            print(f"{key}: {value}")
        print()

def main():
    try:
        date_input = input("Enter date (YYYYMMDD): ")

        validate_date_input(date_input)

        response = soap_call(date_input)

        response_parsed = convert_etree_tags_to_english(response, archive_tag_dict)

        bus_line_input = special_char_upper_func(input("Enter bus line code (Leave empty for all bus lines): "))

        specific_bus_line_data = get_specific_bus_line_data(response_parsed, bus_line_input)

        print_elements(specific_bus_line_data)
    except ValueError as val_exc:
        print(f"ValueError exception: {val_exc}")  
    except TypeError as type_exc:
        print(f"TypeError exception: {type_exc}")  
if __name__ == "__main__":
    main()