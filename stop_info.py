# Displays information about stops of specified bus line
# Supports searching for a stop of specified bus line

import lxml.etree
import zeep
import sys
import lxml

import utils.functions

def take_inputs(): # For handling I/O
    line_code = utils.functions.special_char_upper_func(input("Hat kodu giriniz / Enter bus code: "))
    
    if line_code == "":
        raise ValueError("Hat kodu boş bırakılamaz / Bus code cannot be left empty")
    
    direction_choice = utils.functions.special_char_upper_func(input("Gitmek istediğiniz yönü giriniz (tüm yönler için boş bırakın) / Enter direction you would like to go (for all directions leave empty): "))

    print("1 - Durak listele\n2 - Durak ara")
    choice = input("Tercih giriniz / Enter choice: ")

    if choice not in ["1", "2"]:
        raise ValueError("Hatalı tercih / Invalid choice")
    
    stop_name = ""
    if choice == "2":
        stop_name = utils.functions.special_char_upper_func(input("Durak adı giriniz / Enter stop name: "))

    IO_Dict = {"Line Code": line_code, "Direction": direction_choice, "Choice": choice, "Stop": stop_name}
    return IO_Dict

def soap_call(hat_kodu, wsdl):
    client = zeep.Client(wsdl=wsdl)
    root = client.service.DurakDetay_GYY_wYonAdi(hat_kodu)

    if len(root) == 0:
        print("Hat bulunamadı / Bus line not found")
        exit()
    return root

def parse_soap_response(inputs, root):
    outp_buffer = []
    if inputs["Choice"] == "1":
        if inputs["Direction"] == "":
            for table in root:
                outp_buffer.append(table)
        else:
            for table in root:
                if inputs["Direction"] in table[2].text:
                    outp_buffer.append(table)

    elif inputs["Choice"] == "2":
        if inputs["Direction"] == "":
            for table in root:
                if inputs["Stop"] in table[5].text:
                    outp_buffer.append(table)
        else:
            for table in root:
                if inputs["Direction"] in table[2].text and inputs["Stop"] in table[5].text:
                    outp_buffer.append(table)
    else:
        raise ValueError("Hatalı tercih / Invalid choice")
    
    if len(outp_buffer) == 0: # I prefer not raising exceptions for this case, this can be a totally valid case.
        print("Durak bulunamadı / No stop found")
        exit(1)

    return outp_buffer

def print_xml_tree_tables(input_tree):
    print() # for better styling
    for table in input_tree:
        for element in table.iterchildren():
            print(element.tag, ":", element.text) # display the elements in current table
        print()

def main():
    try:
        wsdl = "xml/durak_hat_bilgi.xml"

        inputs = take_inputs()
        
        root = soap_call(inputs["Line Code"], wsdl)

        outp_buffer = parse_soap_response(inputs, root)
        
        print_xml_tree_tables(outp_buffer)

    except ValueError as val_exc:
        print("Value error exception occurred:", val_exc)

if __name__ == "__main__":
    main()
