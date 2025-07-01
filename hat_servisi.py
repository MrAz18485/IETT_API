import zeep
import json
import lxml.etree
import utils.functions

wsdl = "xml/durak_hat_bilgi.xml"

def take_hat_kodu(hat_kodu_input):
    hat_kodu = utils.functions.special_char_upper_func(hat_kodu_input)
    return hat_kodu

def soap_call(hat_kodu):
    client = zeep.Client(wsdl=wsdl)
    hat_servisi_response = client.service.HatServisi_GYY(hat_kodu) # returns lxml.etree._Element

    if len(hat_servisi_response) == 0:
        print("Hat bulunamadı / Bus line not found")
        exit()
    return hat_servisi_response

def print_etree(input_lxml_etree):
    for table in input_lxml_etree:
        print()
        for element in table:
            print(element.tag, ":", element.text)

def main():
    try:
        hat_kodu = take_hat_kodu(input("Hat kodu giriniz (tüm hatlar için boş bırakın) / Enter bus line code (leave empty for all lines): "))
        hat_servisi_response = soap_call(hat_kodu=hat_kodu)
        
        print_etree(hat_servisi_response)
    except ValueError as val_error_exc:
        print(val_error_exc)

if __name__ == "__main__": # to prevent accidental execution when imported
    main() 