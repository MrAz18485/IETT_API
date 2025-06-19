import zeep
import json

wsdl = "https://api.ibb.gov.tr/iett/AracAnaVeri/AracOzellik.asmx?wsdl"

date_val = input("Yil ve ay sayilarini giriniz (arada bosluk birakarak) / Enter year and month number (leaving space in between): ")
date_val = date_val.split(' ')

try:
    if (len(date_val) != 2):
        raise Exception("Yanlis format")
    client = zeep.Client(wsdl=wsdl)
    akaryakit_litre = client.service.GetAkarYakitToplamLitre_json(date_val[0], date_val[1])
    akaryakit_litre = json.loads(akaryakit_litre)
    
    for element in akaryakit_litre:
        print("Toplam Akaryakıt:", element["ToplamAkarYakit"], "L")
        print("Gün:", element["Gun"])
        print("Ay:", element["Ay"])
        print("Yıl:", element["Yil"], "\n")

except Exception as exc:
    print("An exception occurred:", exc)