import zeep
import json
import os

wsdl = "https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl"

hat_kodu = input("Hat Kodu Giriniz: ")

try:
    client = zeep.Client(wsdl=wsdl)
    duyurular = client.service.GetDuyurular_json()

    duyurular = json.loads(duyurular)
    
    # could make this smaller, but this is more human-readable
    with open("temp_output.txt", "a") as temp_file: # file gets automatically closed after duyurular is exhausted
        for element in duyurular:
            temp_file.write("Hat Kodu: " + element["HATKODU"] + "\n")
            temp_file.write("Hat: " + element["HAT"] + "\n")
            temp_file.write("Tip: " + element["TIP"] + "\n")
            temp_file.write("Güncelleme Saati: " + element["GUNCELLEME_SAATI"] + "\n")
            temp_file.write("Mesaj: " + element["MESAJ"] + "\n\n")

    outp_lines = []
    with open("temp_output.txt", "r") as temp_file:
        buffer_lines = []
        for line in temp_file:
            if len(buffer_lines) == 5:
                if "Hat Kodu" in buffer_lines[0]:
                    if hat_kodu in buffer_lines[0]:
                        temp_list = []
                        for curr_line in buffer_lines:
                            temp_list.append(curr_line)
                        outp_lines.append(temp_list)
                buffer_lines.pop(0)
                buffer_lines.append(line)
            else:
                buffer_lines.append(line)
    for list_element in outp_lines: 
        for element in list_element:
            print(element.strip())
        print()

    if os.path.exists("temp_output.txt") == False:
        raise Exception("Failed to delete temporary file! Please remove temp_output.txt manually if you wish to.")
    os.remove("temp_output.txt")

except Exception as exc:
    print("An exception occurred:", exc)
