import zeep
import lxml.etree
import pytest

wsdl = "durak_hat_bilgi/durak_hat_bilgi.xml"

# python fails to convert some of the turkish lowercase characters to their corresponding upper case pairs
def special_char_upper_func(param):
    special_chars = {"ğ":"Ğ", "ü":"Ü", "i":"İ", "ş":"Ş", "ö":"Ö", "ç":"Ç"}
    for key, value in special_chars.items():
        param = param.replace(key, value)
    return param.upper()

try:
    client = zeep.Client(wsdl=wsdl)

    hat_kodu = special_char_upper_func(input("Hat kodu giriniz / Enter bus code: "))
    
    if hat_kodu == "":
        raise Exception("Hat kodu boş bırakılamaz / Bus code cannot be left empty")
    
    root = client.service.DurakDetay_GYY(hat_kodu)

    if len(root) == 0:
        raise Exception("Hat bulunamadı / Bus line not found")
    
    print("1 - Durak listele\n2 - Durak ara")
    choice = input("Tercih giriniz / Enter choice: ")

    if int(choice) != 1 and int(choice) != 2:
        raise Exception("Hatalı tercih / Invalid choice")

    print("G - Gidiş, D - Dönüş")
    direction_choice = input("Yön seçiniz / Choose direction (leave blank for both): ").upper()
    
    if direction_choice not in {"G", "D", ""}:
        raise Exception("Hatalı tercih / Invalid choice")

    outp_buffer = []

    if (int(choice) == 1):
        if direction_choice == "": # prints all stops 
            for table in root:
                outp_buffer.append(table)
        else:
            for table in root:
                if table[1].text == direction_choice: # display only the tables that have chosen direction
                    outp_buffer.append(table)
    elif (int(choice) == 2):
        durak_adi = special_char_upper_func(input("Durak adı giriniz / Enter stop name: "))
        if direction_choice == "":
            for table in root:
                if durak_adi in table[4].text:
                    outp_buffer.append(table)
        else:
            for table in root:
                if table[1].text == direction_choice and durak_adi in table[4].text:
                    outp_buffer.append(table)
    else:
        raise Exception("Hatalı tercih / Invalid choice")
    
    if len(outp_buffer) == 0:
        print("Durak bulunamadı / No stop found")
        exit(1)
    
    print()
    for table in outp_buffer:
        for element in table.iterchildren():
            print(element.tag, ":", element.text) # display the elements in buffer
        print()


except Exception as exc:
    print("An exception occurred:", exc)
