import zeep
import json
import lxml.etree

wsdl = "xml/durak_hat_bilgi.xml"

try:
    client = zeep.Client(wsdl=wsdl)

    hat_kodu = input("Hat kodu giriniz (tüm hatlar için boş bırakın) / Enter bus line code (leave empty for all lines): ")

    hat_servisi_response = client.service.HatServisi_GYY(hat_kodu) # returns lxml.etree._Element
    
    if len(hat_servisi_response) == 0:
        print("Hat bulunamadı / Bus line not found")
        exit()

    # don't need to append resulting tables one by one to an array
    # however, for doing any manipulations further, it makes our job easier
    outp_buffer = []

    for table in hat_servisi_response:
        outp_buffer.append(table)
    
    print()
    for table in outp_buffer:
        for element in table:
            print(element.tag, ":", element.text)

except Exception as exc:
    print("An exception occurred:", exc)
