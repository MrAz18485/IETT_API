# Lists announcments for the given bus line

import zeep
import json
import os
from utils.functions import special_char_upper_func, replace_keyword, etree_element_with_text

wsdl = "https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl"

announcments_tag_dict = {"HATKODU": "LINE_CODE", "HAT": "LINE", "TIP": "TYPE", "GUNCELLEME_SAATI": "UPDATE_TIME", "MESAJ": "MESSAGE"}

def take_line_code(line_code_input):
    line_code = special_char_upper_func(line_code_input)
    return line_code

def soap_call():
    client = zeep.Client(wsdl=wsdl)
    announcments_response = client.service.GetDuyurular_json()
    return announcments_response

def soap_response_to_list(soap_response):
    return json.loads(soap_response)

def get_specific_bus_lines_announcments(line_code, announcment_list):
    output_buffer = []
    for element in announcment_list:
        if line_code in element["HATKODU"]:
            updated_dict = {}
            for key in element:
                updated_dict[replace_keyword(key, announcments_tag_dict)] = element[key]
            output_buffer.append(updated_dict)
    if len(output_buffer) == 0:
        print("Announcments not found")
        exit()
    return output_buffer

def print_elements(outp_buffer):
    print()
    for list_element in outp_buffer: 
        print("Line Code:", list_element["LINE_CODE"])
        print("Line:", list_element["LINE"])
        print("Type:", list_element["TYPE"])
        print("Update Time:", list_element["UPDATE_TIME"])
        print("Message:", list_element["MESSAGE"])
        print()

def main():
    try:
        hat_kodu = take_line_code(input("Enter bus line code (leave empty for all announcments): "))

        duyurular_response = soap_call()

        duyurular_response_list = soap_response_to_list(duyurular_response)

        specific_announcments = get_specific_bus_lines_announcments(hat_kodu, duyurular_response_list)

        print_elements(specific_announcments)

        print(etree_element_with_text(tag="LINE_CODE", text="KM18"))
    except IndexError as index_exc:
        print("Index error when iterating/doing something a list:", index_exc)

if __name__ == "__main__": 
    main() 