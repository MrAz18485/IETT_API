import zeep
import json
import lxml.etree
import utils.functions

wsdl = "xml/durak_hat_bilgi.xml"

def take_line_code(line_code_input):
    line_code = utils.functions.special_char_upper_func(line_code_input)
    return line_code

def soap_call(line_code):
    client = zeep.Client(wsdl=wsdl)
    line_service_response = client.service.HatServisi_GYY(line_code) # returns lxml.etree._Element

    if len(line_service_response) == 0:
        print("Hat bulunamadı / Bus line not found")
        exit()
    return line_service_response

def print_etree(input_lxml_etree):
    for table in input_lxml_etree:
        print()
        for element in table:
            print(element.tag, ":", element.text)

def main():
    try:
        line_code = take_line_code(input("Hat kodu giriniz (tüm hatlar için boş bırakın) / Enter bus line code (leave empty for all lines): "))
        line_service_response = soap_call(line_code)
        
        print_etree(line_service_response)
    except ValueError as val_error_exc:
        print(val_error_exc)

if __name__ == "__main__": # to prevent accidental execution when imported
    main() 