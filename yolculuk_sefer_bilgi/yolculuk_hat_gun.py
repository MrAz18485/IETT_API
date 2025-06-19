# en çok yolculuk yapan 50 hattı içerir

import zeep
import json
from datetime import date, timedelta

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

date_val = input("Tarih giriniz (YYY-MM-DD) / Enter date (YYY-MM-DD): ")
hat_val = input("Hat ismi giriniz (Tum hatlar icin enter'a basin) / Enter bus line code (For all lines press enter): ")

# parses the date value to milliseconds
def ms_parser(line):
    startidx = -1
    endidx = -1

    for i in range(len(line["Gun"])):
        if (line["Gun"][i] == '('):
            startidx = i
        elif (line["Gun"][i] == ')'):
            endidx = i
    date_to_ms = int(line["Gun"][startidx+1:endidx])
    return date_to_ms

# Converts ms to date by adding ms_input to epoch date (1970-01-01) 
def ms_to_date_converter(ms_input):
    return date.fromisoformat('1970-01-01') + timedelta(milliseconds=ms_input) # epoch + ms

try:
    client = zeep.Client(wsdl=wsdl)
    duyurular = client.service.GetIettYolculukHat_json(date_val)

    duyurular = json.loads(duyurular)

    if hat_val == "":
        for line in duyurular:
            date_to_ms = ms_parser(line)
            curr_date_conversion = ms_to_date_converter(date_to_ms)

            print("Gün: ", curr_date_conversion)
            print("Hat: ", line["Hat"])
            print("Yolculuk: ", line["Yolculuk"], "\n")
    else:
        for line in duyurular:
            if line["Hat"] == hat_val:
                print()
                date_to_ms = ms_parser(line)
                curr_date_conversion = ms_to_date_converter(date_to_ms)

                print("Gün: ", curr_date_conversion)
                print("Hat: ", line["Hat"])
                print("Yolculuk: ", line["Yolculuk"], "\n")

except Exception as exc:
    print("An exception occurred:", exc)
