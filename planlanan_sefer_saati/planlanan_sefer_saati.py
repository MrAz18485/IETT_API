# not working. Probably due to incorrect method name?
# No definition '{http://tempuri.org/}GetPlanlananSeferSaati_XMLAuthHeader' in 'messages' found
from zeep import Client, Settings
import json

wsdl = "planlanan_sefer_saati/PlanlananSeferSaati.asmx.xml"

hat_kodu = input("Hat kodu giriniz: ")

try:
    client = Client(wsdl=wsdl)
    sefer_saatleri = client.service.GetPlanlananSeferSaati_json(hat_kodu)
    
    sefer_saatleri = json.loads(sefer_saatleri)
    print()
    
    if len(sefer_saatleri) == 0:
        raise Exception("Sefer bulunamadı! / No timetable found!")
    for element in sefer_saatleri:
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
