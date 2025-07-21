import lxml
import zeep
from utils.functions import convert_etree_tags_to_english

crash_tag_dict = {"KAZASAAT":"CRASH_HOUR", "BOYLAM": "LONGITUDE", "ENLEM": "LATITUDE"}

wsdl = "xml/departure.xml"

def validate_date_input(date_val):
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

def make_soap_call(date_input, client):
    return client.service.GetKazaLokasyon_XML(date_input)

def validate_soap_response(response):
    if len(response) == 0:
        print("No data found")
        exit()
    return True

def print_elements(buffer):
    print()
    for element in buffer:
        for key, value in element.items():
            print(f"{key}: {value}")
        print()

def main():
    try:
        client = zeep.Client(wsdl=wsdl)
        
        date_input = input("Enter date input (YYYY-MM-DD): ")

        validate_date_input(date_input)
        
        soap_response = make_soap_call(date_input, client)
                
        validate_soap_response(soap_response)

        soap_response_parsed = convert_etree_tags_to_english(soap_response, crash_tag_dict)
        
        print_elements(soap_response_parsed)
    except ValueError as val_error:
        print(f"ValueError: {val_error}")

if __name__ == "__main__":
    main()