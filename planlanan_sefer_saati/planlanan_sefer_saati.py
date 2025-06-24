from zeep import Client, Settings
import json
import sys

wsdl = "planlanan_sefer_saati/PlanlananSeferSaati.asmx.xml"

def special_char_upper_func(param):
    special_chars = {"ğ":"Ğ", "ü":"Ü", "i":"İ", "ş":"Ş", "ö":"Ö", "ç":"Ç"}
    for key, value in special_chars.items():
        param = param.replace(key, value)
    return param.upper()

try:
    client = Client(wsdl=wsdl)
    hat_kodu = special_char_upper_func(input("Hat kodu giriniz / Enter bus line code: "))

    if hat_kodu == "":
        raise Exception("Hat kodu boş bırakılamaz / Bus code cannot be left empty")
    
    sefer_saatleri = client.service.GetPlanlananSeferSaati_json(hat_kodu)
    sefer_saatleri = json.loads(sefer_saatleri)

    if len(sefer_saatleri) == 0:
        raise Exception("Sefer saatleri bulunamadı / Timetable not found")
    
    # problematic, since a bus line can have multiple routes, but we're displaying only the first one that appears that is fetched
    print(sefer_saatleri[0]["SHATKODU"], "(", sefer_saatleri[0]["HATADI"], ")")
    direction = input("Yön giriniz (G - Gidiş, D-Dönüş, soldan sağa) / Enter direction (G - from left to right, D - from right to left): ").upper()

    if direction != "G" and direction != "D":
        raise Exception("Hatalı yön seçimi / Incorrect direction choice")

    day = input("Gün seçiniz (I - hafta içi, C - Cumartesi, P - Pazar) / Choose day (I - weekdays, C - Saturday, P - Sunday): ")

    if day not in {"I", "C", "P"}:
        raise Exception("Hatalı gün seçimi / Incorrect day choice")
    
    print()
    outp_buffer = []

    for element in sefer_saatleri:
        if element["SYON"] == direction and element["SGUNTIPI"] == day:
            outp_buffer.append(element)

    if len(outp_buffer) == 0:
        print("Sorgulanan hattın sefer saatleri bulunamadı / Unable to find timetable of queried bus line")

    else:
        for element in outp_buffer:
            print("Hat Kodu: ", element["SHATKODU"])
            print("Hat Adı: ", element["HATADI"])
            print("Güzergah Kodu: ", element["SGUZERAH"])
            print("Yön Bilgisi: ", element["SYON"])
            print("Gün Bilgisi: ", element["SGUNTIPI"])
            print("Güzergah İşareti: ", element["GUZERGAH_ISARETI"])
            print("Servis Tipi: ", element["SSERVISTIPI"])
            print("Saat Bilgisi: ", element["DT"], "\n")

except Exception as exc:
    print("An exception occurred: ", exc)
