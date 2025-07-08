# Outputs the top 50 bus lines with highest number of travels for the given date
# If the user asks for a specific bus line, (considering it's in top 50), only information regarding that bus line is displayed instead.

import zeep
import json
from datetime import date, timedelta
import utils.functions

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

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
             output_buffer.append(element)

    return output_buffer

def print_elements(buffer):
    print()
    for element in buffer:
        date_to_ms = utils.functions.ms_parser(element["Gun"])
        curr_date_conversion = ms_to_date_converter(date_to_ms) 
        print(f"Gün: {curr_date_conversion}")
        print(f"Hat: {element["Hat"]}")
        print(f"Yolculuk: {element["Yolculuk"]}\n")

def main():
    try:
        date_val = input("Tarih giriniz (YYY-MM-DD) / Enter date (YYY-MM-DD): ")

        validate_inputs(date_val)

        bus_line_val = utils.functions.special_char_upper_func(input("Hat ismi giriniz (Tum hatlar icin enter'a basin) / Enter bus line code (For all lines press enter): "))

        soap_response = soap_call(date_val)

        soap_response_list = convert_soap_response_to_list(soap_response)

        bus_data = get_data_of_specific_bus_line(bus_line_val, soap_response_list)
        
        if len(bus_data) == 0:
            print("Belirlenen hat için yolculuk sayısı bulunamadı / Number of trips not found for the specified bus line")
            exit()

        print_elements(bus_data)
    except ValueError as val_exc:
        print("ValueError exception:", val_exc)

if __name__ == "__main__":
    main()