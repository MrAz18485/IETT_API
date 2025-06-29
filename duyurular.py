# Otobüs hattındaki duyuruları listeler
# Lists announcments for the specified bus line

import zeep
import json
import os
import utils.functions

wsdl = "https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl"

def take_hat_kodu(hat_kodu_input):
    hat_kodu = utils.functions.special_char_upper_func(hat_kodu_input)
    return hat_kodu

def soap_call():
    client = zeep.Client(wsdl=wsdl)
    duyurular_response = client.service.GetDuyurular_json()

    duyurular_response = json.loads(duyurular_response)

    if len(duyurular_response) == 0:
        print("Duyurular bulunamadı / Announcments not found")
        exit()

    return duyurular_response

def write_to_tempfile(input_buffer, file_name):
    with open(f'{file_name}', "w") as temp_file: # file gets automatically closed after duyurular is exhausted
        for element in input_buffer:
            temp_file.write(f'{element}\n')

def read_from_tempfile(hat_kodu, file_name):
    # there's definitely a better approach than this, but let's keep it this way for this script
    outp_lines = []
    with open(f"{file_name}", "r") as temp_file:
        for line in temp_file:
            line_buffer = line.split(",")
            if "HATKODU" in line_buffer[0] and hat_kodu in line_buffer[0]:
                line = line.strip("\n")
                outp_lines.append(line)
    return outp_lines
    
def string_to_dict(buffer):
    formatted_buffer = []
    for line in buffer:
        line = line.replace("\'", "\"")
        formatted_buffer.append(json.loads(line))
    return formatted_buffer

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
        hat_kodu = take_hat_kodu(input("Hat kodu giriniz (tüm duyurular için boş bırakın) / Enter bus line code (leave empty for all announcments): "))

        duyurular_resonse = soap_call()

        # write the tables to temp_file.txt
        write_to_tempfile(duyurular_resonse, "temp_output.txt")

        # read from temp_file.txt, store returned list in outp_lines
        outp_lines = read_from_tempfile(hat_kodu, "temp_output.txt")

        outp_lines_formatted = string_to_dict(outp_lines)

        print_elements(outp_lines_formatted)

        if os.path.exists("temp_output.txt") == False:
            raise FileNotFoundError("Failed to delete temporary file! Please remove temp_output.txt manually if you wish to.")
        os.remove("temp_output.txt")
    except FileNotFoundError as filenotfound_exc:
        print("File error:", filenotfound_exc)
    except IndexError as index_exc:
        print("Index error when iterating/doing something a list:", index_exc)

if __name__ == "__main__": 
    main() 