# Displays information about stops of specified bus line
# Supports searching for a stop of specified bus line

import lxml.etree
import zeep
import sys
import lxml

from utils.functions import special_char_upper_func, convert_etree_tags_to_english
wsdl = "xml/line_service.xml"

stop_info_key_dict = {"HATKODU": "LINE_CODE", "YON": "DIRECTION", "YON_ADI": "DIRECTION_NAME", "SIRANO": "QUEUE_NUMBER", "DURAKKODU": "STOP_CODE",
                      "DURAKADI": "STOP_NAME", "XKOORDINATI": "X_COORDINATE", "YKOORDINATI":"Y_COORDINATE", 
                      "DURAKTIPI": "STOP_TYPE", "ISLETMEBOLGE": "SERVICE_REGION", "ISLETMEALTBOLGE": "SERVICE_SUBREGION", "ILCEADI": "DISTRICT_NAME"}

def take_inputs(): # For handling I/O
    line_code = special_char_upper_func(input("Enter bus line code: "))
    
    if line_code == "":
        raise ValueError("Bus line code cannot be left empty")
    
    direction_choice = special_char_upper_func(input("Enter direction you would like to go (for all directions leave empty): "))

    print("1 - List stops\n2 - Search for a stop")
    choice = input("Enter choice: ")

    if choice not in ["1", "2"]:
        raise ValueError("Invalid choice")
    
    stop_name = ""
    if choice == "2":
        stop_name = special_char_upper_func(input("Enter stop name: "))

    IO_Dict = {"Line_Code": line_code, "Direction": direction_choice, "Choice": choice, "Stop": stop_name}
    return IO_Dict

def soap_call(line_code, wsdl):
    client = zeep.Client(wsdl=wsdl)
    root = client.service.DurakDetay_GYY_wYonAdi(line_code)

    if len(root) == 0:
        print("Bus line not found")
        exit()
    return root

def parse_soap_response(inputs, root):
    outp_buffer = []
    if inputs["Choice"] == "1":
        if inputs["Direction"] == "":
            for table in root:
                outp_buffer.append(table)
        else:
            for table in root:
                if inputs["Direction"] in table[2].text:
                    outp_buffer.append(table)

    elif inputs["Choice"] == "2":
        if inputs["Direction"] == "":
            for table in root:
                if inputs["Stop"] in table[5].text:
                    outp_buffer.append(table)
        else:
            for table in root:
                if inputs["Direction"] in table[2].text and inputs["Stop"] in table[5].text:
                    outp_buffer.append(table)
    else:
        raise ValueError("Invalid choice")
    
    if len(outp_buffer) == 0: # I prefer not raising exceptions for this case, this can be a totally valid case.
        print("No stop(s) found")
        exit()

    return outp_buffer

def print_stops(stop_dictionary_list):
    print() # for better styling
    for stop in stop_dictionary_list:
        for key, value in stop.items():
            print(f"{key}: {value}")
        print()

def main():
    try:
        inputs = take_inputs()
        
        root = soap_call(inputs["Line_Code"], wsdl)

        stop_results = parse_soap_response(inputs, root)

        stop_results_formatted = convert_etree_tags_to_english(stop_results, stop_info_key_dict)

        print_stops(stop_results_formatted)

    except ValueError as val_exc:
        print("Value error exception occurred:", val_exc)

if __name__ == "__main__":
    main()
