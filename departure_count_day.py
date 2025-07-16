# Outputs the top 50 bus lines with highest number of travels for the given date
# If the user asks for a specific bus line, (considering it's in top 50), only information regarding that bus line is displayed instead.

import zeep
import json
from datetime import date, timedelta
from utils.functions import ms_parser, special_char_upper_func, replace_keyword
import timeit

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

departure_tag_dict = {"Gun": "DAY", "Hat": "LINE", "Yolculuk": "PASSENGERS"}

# Converts ms to date by adding ms_input to epoch date (1970-01-01) 
def ms_to_date_converter(ms_input):
    return date.fromisoformat('1970-01-02') + timedelta(milliseconds=ms_input) # epoch + 1 + ms, API call returns values of previous day

def validate_inputs(date_val):
    date_val_list = date_val.split("-")

    if len(date_val_list) != 3:
        raise ValueError("Incorrect format")    
    elif int(date_val_list[0]) < 2019:
        raise ValueError("Year cannot be less than 2019")
    elif int(date_val_list[1]) < 1 or int(date_val_list[1]) > 12:
        raise ValueError("Invalid month")
    elif int(date_val_list[2]) < 1 or int(date_val_list[2]) > 31:
        raise ValueError("Invalid day")
    return True

def soap_call(date_val):
    client = zeep.Client(wsdl=wsdl)
    response = client.service.GetIettYolculukHat_json(date_val)
    if len(response) == 2:
        print("No data for given date found!")
        exit()
    return response

def convert_soap_response_to_list(soap_response):
    return json.loads(soap_response)

def get_data_of_specific_bus_line(bus_line_val, response_list):
    output_buffer = []
    for element in response_list:
         if isinstance(element["Hat"], str) and bus_line_val in element["Hat"]: # Don't add bus lines with bus line name "None"
            updated_dict = {}
            # Basically, changes the key of a value in dictionary based on departure_tag_dict
            for key in element:
                updated_dict[replace_keyword(key, departure_tag_dict)] = element[key] # set element[new_key] = element[old_key]
            output_buffer.append(updated_dict)
    return output_buffer

def print_elements(buffer):
    print()
    for element in buffer:
        date_to_ms = ms_parser(element["DAY"])
        curr_date_conversion = ms_to_date_converter(date_to_ms) 
        print(f"Day: {curr_date_conversion}")
        print(f"Line: {element["LINE"]}")
        print(f"Passengers: {element["PASSENGERS"]}\n")

def main():
    try:
        date_val = input("Enter date (YYY-MM-DD): ")

        validate_inputs(date_val)

        bus_line_val = special_char_upper_func(input("Enter bus line code (For all lines press enter): "))

        soap_response = soap_call(date_val)

        soap_response_list = convert_soap_response_to_list(soap_response)

        bus_data = get_data_of_specific_bus_line(bus_line_val, soap_response_list)
        
        if len(bus_data) == 0:
            print("Number of departures not found for the specified bus line")
            exit()

        print_elements(bus_data)
    except ValueError as val_exc:
        print(f"ValueError exception: {val_exc}")
    except KeyError as key_exc:
        print(f"KeyError exception: {key_exc}")

if __name__ == "__main__":
    main()
