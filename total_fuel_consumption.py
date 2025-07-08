# Displays total fuel consumption for given date

import zeep
import json

wsdl = "https://api.ibb.gov.tr/iett/AracAnaVeri/AracOzellik.asmx?wsdl"

def take_inputs():
    date_val = input("Yil ve ay sayilarini giriniz (arada bosluk birakarak) / Enter year and month number (leaving space in between): ").split(' ')

    if len(date_val) != 2 or date_val[0].isnumeric() == False or date_val[1].isnumeric() == False:
        raise ValueError("Incorrect format")
    
    return {"Year": date_val[0], "Month": date_val[1]}

def convert_dict_strings_to_int(input_dict):
    for key, value in input_dict.items():
        input_dict[key] = int(value) # raises exception if element is not convertable to int
    return input_dict

def soap_call(input_dict):
    client = zeep.Client(wsdl=wsdl)
    akaryakit_litre = client.service.GetAkarYakitToplamLitre_json(input_dict["Year"], input_dict["Month"])
    if len(akaryakit_litre) == 2: # I don't know why it returns 2 characters
        print("No data found / Veri bulunamadı")
        exit()
    return akaryakit_litre

def convert_soap_response_to_dictionary(input_string):
    input_string = json.loads(input_string)
    return input_string

def print_dictionary(input_array):
    for element in input_array:
        print(f"Toplam Akaryakıt: {element["ToplamAkarYakit"]}L")
        print(f"Gün: {element["Gun"]}")
        print(f"Ay: {element["Ay"]}")
        print(f"Yıl: {element["Yil"]}\n")

def main():
    try:
        input_dict = take_inputs()
        formatted_input_dict = convert_dict_strings_to_int(input_dict)

        soap_response = soap_call(formatted_input_dict)
        formatted_soap_response = convert_soap_response_to_dictionary(soap_response)
        
        print_dictionary(formatted_soap_response)

    except ValueError as val_exc:
        print("Value error exception:", val_exc)

if __name__ == "__main__":
    main()