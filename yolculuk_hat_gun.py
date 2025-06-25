# en çok yolculuk yapan 50 hattı içerir

import zeep
import json
from datetime import date, timedelta
import utils.functions

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

# Converts ms to date by adding ms_input to epoch date (1970-01-01) 
def ms_to_date_converter(ms_input):
    return date.fromisoformat('1970-01-02') + timedelta(milliseconds=ms_input) # epoch + 1 + ms, API call returns values of previous day

try:
    client = zeep.Client(wsdl=wsdl)

    date_val = input("Tarih giriniz (YYY-MM-DD) / Enter date (YYY-MM-DD): ")

    hat_val = utils.functions.special_char_upper_func(input("Hat ismi giriniz (Tum hatlar icin enter'a basin) / Enter bus line code (For all lines press enter): "))

    duyurular = client.service.GetIettYolculukHat_json(date_val)

    duyurular = json.loads(duyurular)

    if hat_val == "":
        if len(duyurular) == 0:
            print("En çok yolculuk yapan ilk 50 hattın yolculuk sayısı bulunamadı / Top 50 bus lines based on number of trips not found ")
            exit()

        print() # for styling
        for line in duyurular:
            date_to_ms = utils.functions.ms_parser(line)
            curr_date_conversion = ms_to_date_converter(date_to_ms)

            print("Gün: ", curr_date_conversion)
            print("Hat: ", line["Hat"])
            print("Yolculuk: ", line["Yolculuk"], "\n")
    else:
        outp_buffer = []

        for line in duyurular:
            if line["Hat"] == hat_val:
                outp_buffer.append(line)

        if len(outp_buffer) == 0:
            print("Belirlenen hat için yolculuk sayısı bulunamadı / Number of trips not found for the specified bus line")
            exit()

        print()
        for line in outp_buffer:
            date_to_ms = utils.functions.ms_parser(line)
            curr_date_conversion = ms_to_date_converter(date_to_ms)

            print("Gün: ", curr_date_conversion)
            print("Hat: ", line["Hat"])
            print("Yolculuk: ", line["Yolculuk"], "\n")
except Exception as exc:
    print("An exception occurred:", exc)
