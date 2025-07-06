# Otobüs hattındaki duyuruları listeler
# Lists announcments for the specified bus line

import zeep
import json
import os
import utils.functions

wsdl = "https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl"

def take_line_code(line_code_input):
    line_code = utils.functions.special_char_upper_func(line_code_input)
    return line_code

def soap_call():
    client = zeep.Client(wsdl=wsdl)
    announcments_response = client.service.GetDuyurular_json()

    if len(announcments_response) == 0:
        print("Duyurular bulunamadı / Announcments not found")
        exit()

    return announcments_response

def soap_response_to_list(soap_response):
    return json.loads(soap_response)

def get_specific_bus_lines_announcments(line_code, announcment_list):
    output_buffer = []
    for element in announcment_list:
        if line_code in element["HATKODU"] :
            output_buffer.append(element)
    return output_buffer

def print_elements(outp_buffer):
    print()
    for list_element in outp_buffer: 
        print("Hat Kodu:", list_element["HATKODU"])
        print("Hat:", list_element["HAT"])
        print("Tip:", list_element["TIP"])
        print("Güncelleme Saati:", list_element["GUNCELLEME_SAATI"])
        print("Mesaj:", list_element["MESAJ"])
        print()

def main():
    try:
        hat_kodu = take_line_code(input("Hat kodu giriniz (tüm duyurular için boş bırakın) / Enter bus line code (leave empty for all announcments): "))

        duyurular_response = soap_call()

        duyurular_response_list = soap_response_to_list(duyurular_response)

        specific_announcments = get_specific_bus_lines_announcments(hat_kodu, duyurular_response_list)

        print_elements(specific_announcments)

    except IndexError as index_exc:
        print("Index error when iterating/doing something a list:", index_exc)

if __name__ == "__main__": 
    main() 