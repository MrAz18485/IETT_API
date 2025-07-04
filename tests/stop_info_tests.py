import lxml.etree
import pytest
import os
from lxml import etree
import sys
sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import stop_info

wsdl = "/home/lolundcmd/Desktop/IETT_API_Tools/xml/durak_hat_bilgi.xml"

def test_take_inputs_valid():
    with open("test_take_inputs_valid.txt", "w") as file1:
        file1.write("KM18\nKurtköy\n1\n")
    sys.stdin = open("test_take_inputs_valid.txt", "r")
    output = stop_info.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_valid.txt")
    assert output == {"Line Code" : "KM18", "Direction" : "KURTKÖY", "Choice" : "1", "Stop" : ""}

def test_take_inputs_valid2():
    with open("test_take_inputs_valid2.txt", "w") as file1:
        file1.write("KM18\nSabancı\n2\nOtoyol\n")
    sys.stdin = open("test_take_inputs_valid2.txt", "r")
    output = stop_info.take_inputs()
    sys.stdin = sys.__stdin__ 
    os.remove("test_take_inputs_valid2.txt")
    assert output == {"Line Code" : "KM18", "Direction" : "SABANCI", "Choice" : "2", "Stop" : "OTOYOL"}

def test_take_inputs_empty_line_code() :
    with pytest.raises(ValueError):
        with open("test_take_inputs_empty_line_code.txt", "w") as file1:
            file1.write("\n")
        sys.stdin = open("test_take_inputs_empty_line_code.txt", "r")
        output = stop_info.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_empty_line_code.txt")

def test_take_inputs_invalid_choice_1():
    with pytest.raises(ValueError):
        with open("test_take_inputs_invalid_choice_1.txt", "w") as file1:
            file1.write("KM18\n\n3\n")
        sys.stdin = open("test_take_inputs_invalid_choice_1.txt", "r")
        output = stop_info.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_invalid_choice_1.txt")

# Not going to make a lot of checks here other than invalid inputs
# I can only check whether if the user gives valid inputs or not, API is responsible for other stuff

def test_soapcall_invalid(capsys):
    with pytest.raises(SystemExit):
        stop_info.soap_call("abc", wsdl)

def etree_constructor(tables): # helper for methods below. 
    root_elem = etree.Element("NewDataSet")
    for i in range(len(tables)):
        root_elem.append(etree.Element("Table"))
    curr_table_index = 0
    for table in tables :
        for key, value in table.items():
            element = lxml.etree.Element(key)
            element.text = value
            root_elem[curr_table_index].append(element)
        curr_table_index += 1
    return root_elem

def test_parsesoap_response_choice1_directionempty(): # should get all elements in mock_etree
    inputs = {"Choice" : "1", "Direction" : ""}
    mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "M" : "k", "ilikebiscuits" : "chocolate"}])
    result = stop_info.parse_soap_response(inputs, mock_etree)

    expected_result = list(mock_etree)
    assert result == expected_result

def test_parsesoap_response_choice1_direction(): # direction is not empty now, should get all elements in mock_etree
    inputs = {"Choice" : "1", "Direction" : "Kurtköy"}
    mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Kurtköy", "ilikebiscuits" : "chocolate"}])

    result = stop_info.parse_soap_response(inputs, mock_etree) 

    expected_result = list(mock_etree)
    assert result == expected_result

def test_parsesoap_response_choice2_directionempty_invalidstop(): # stop name doesn't exist, program should exit
    with pytest.raises(SystemExit):
        inputs = {"Choice" : "2", "Direction" : "", "Stop" : "mis_adana_kebap"}
        mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Kurtköy", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
        result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

def test_parsesoap_response_choice2_direction_invalidstop(): # stop name doesn't exist, program should exit
    with pytest.raises(SystemExit):
        inputs = {"Choice" : "2", "Direction" : "", "Stop" : "idk_where_to_go"}
        mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Sabancı", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
        result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

def test_parsesoap_response_choice2_direction():
    inputs = {"Choice" : "2", "Direction" : "", "Stop" : "OTOYOL_KAVSAGI"}
    mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Sabancı", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
    expected_result = list(mock_etree)

    result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

    assert result == expected_result


def test_parsesoap_response_invalidchoice(): # invalid choice, should raise a ValueError exception
    with pytest.raises(ValueError):
        inputs = {"Choice" : "5", "Direction" : "Kurtköy"}
        mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Sabancı", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
        result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

def test_printxmltree_tables_valid1(capsys):
    input = etree_constructor([
    {
                "HATKODU" : "KM18",
                "YON" : "D",
                "YON_ADI" : "SABANCI ÜNİVERSİTESİ",
                "SIRANO" :"1",
                "DURAKKODU" : "289821",
                "DURAKADI" : "KURTKÖY MAHALLESİ METRO",
                "XKOORDINATI" : "29.295970",
                "YKOORDINATI" : "40.909935",
                "DURAKTIPI" : "İETTBAYRAK",
                "ISLETMEBOLGE" : "Anadolu2",
                "ISLETMEALTBOLGE" : "Pendik",
                "ILCEADI" : "Pendik"
    }
    ])  

    stop_info.print_xml_tree_tables(input)
    captured = capsys.readouterr()

    expected_output = str(
            "\nHATKODU : KM18\n" + 
            "YON : D\n" +
            "YON_ADI : SABANCI ÜNİVERSİTESİ\n" +
            "SIRANO : 1\n" +
            "DURAKKODU : 289821\n" + 
            "DURAKADI : KURTKÖY MAHALLESİ METRO\n"+ 
            "XKOORDINATI : 29.295970\n" +
            "YKOORDINATI : 40.909935\n" +
            "DURAKTIPI : İETTBAYRAK\n" +
            "ISLETMEBOLGE : Anadolu2\n" +
            "ISLETMEALTBOLGE : Pendik\n" +
            "ILCEADI : Pendik\n\n"
    )
    assert captured.out == expected_output

def test_printxmltree_tables_valid2(capsys):
    input = etree_constructor([
    {
        "HATKODU" : "KM18",
        "YON" : "D",
        "YON_ADI" : "SABANCI ÜNİVERSİTESİ",
        "SIRANO" :"1",
        "DURAKKODU" : "289821",
        "DURAKADI" : "KURTKÖY MAHALLESİ METRO",
    },   
    {                
    "HATKODU" : "KM18",
    "YON" : "D",
    "YON_ADI" : "SABANCI ÜNİVERSİTESİ",
    "SIRANO" : "2",
    "DURAKKODU" : "263191",
    "DURAKADI" : "ENSAR CADDESİ GİRİŞİ",
    }])
    
    stop_info.print_xml_tree_tables(input)
    captured = capsys.readouterr()
    
    expected_output = str(
            "\nHATKODU : KM18\nYON : D\n" +
            "YON_ADI : SABANCI ÜNİVERSİTESİ\n" +
            "SIRANO : 1\n" + 
            "DURAKKODU : 289821\n" + 
            "DURAKADI : KURTKÖY MAHALLESİ METRO\n\n" +
            "HATKODU : KM18\n" + 
            "YON : D\n" + 
            "YON_ADI : SABANCI ÜNİVERSİTESİ\n" +
            "SIRANO : 2\n" +
            "DURAKKODU : 263191\n" +
            "DURAKADI : ENSAR CADDESİ GİRİŞİ\n\n"
    )
    assert captured.out == expected_output

def test_printxmltree_tables_empty(capsys): # shouldn't print anything
    input = lxml.etree.Element("abc")
    
    stop_info.print_xml_tree_tables(input)
    captured = capsys.readouterr()
    
    expected_output = str("\n")
    assert captured.out == expected_output
