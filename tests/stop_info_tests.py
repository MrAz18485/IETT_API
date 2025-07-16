import lxml.etree
import pytest
import os
from lxml import etree
import sys

sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

from utils.functions import etree_constructor
import stop_info

wsdl = "xml/line_service.xml"

def test_take_inputs_valid():
    with open("test_take_inputs_valid.txt", "w") as file1:
        file1.write("KM18\nKurtköy\n1\n")
    sys.stdin = open("test_take_inputs_valid.txt", "r")
    output = stop_info.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_valid.txt")
    assert output == {"Line_Code" : "KM18", "Direction" : "KURTKÖY", "Choice" : "1", "Stop" : ""}

def test_take_inputs_valid2():
    with open("test_take_inputs_valid2.txt", "w") as file1:
        file1.write("KM18\nSabancı\n2\nOtoyol\n")
    sys.stdin = open("test_take_inputs_valid2.txt", "r")
    output = stop_info.take_inputs()
    sys.stdin = sys.__stdin__ 
    os.remove("test_take_inputs_valid2.txt")
    assert output == {"Line_Code" : "KM18", "Direction" : "SABANCI", "Choice" : "2", "Stop" : "OTOYOL"}

def test_take_inputs_empty_line_code() :
    with pytest.raises(ValueError):
        with open("test_take_inputs_empty_line_code.txt", "w") as file1:
            file1.write("\n")
        sys.stdin = open("test_take_inputs_empty_line_code.txt", "r")
        output = stop_info.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_empty_line_code.txt")

def test_take_inputs_invalid_choice():
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

def test_parsesoap_response_choice1_nonexistent_direction(): # direction is not empty now, should get all elements in mock_etree
    with pytest.raises(SystemExit):
        inputs = {"Choice" : "1", "Direction" : "s"}
        mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Kurtköy", "ilikebiscuits" : "chocolate"}])

        result = stop_info.parse_soap_response(inputs, mock_etree) 

def test_parsesoap_response_choice2_directionempty():
    inputs = {"Choice" : "2", "Direction" : "", "Stop" : "OTOYOL_KAVSAGI"}
    mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Sabancı", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
    expected_result = list(mock_etree)

    result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

    assert result == expected_result

def test_parsesoap_response_choice2_directionempty_invalidstop(): # stop name doesn't exist, program should exit
    with pytest.raises(SystemExit):
        inputs = {"Choice" : "2", "Direction" : "", "Stop" : "mis_adana_kebap"}
        mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Kurtköy", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
        result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

def test_parsesoap_response_choice2_direction_stop(): # stop name doesn't exist, program should exit
    inputs = {"Choice" : "2", "Direction" : "Sabancı", "Stop" : "OTOYOL_KAVSAGI"}
    mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Sabancı", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
    result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list
    
    expected_result = list(mock_etree)
    
    assert result == expected_result

def test_parsesoap_response_choice2_direction_invalidstop(): # stop name doesn't exist, program should exit
    with pytest.raises(SystemExit):
        inputs = {"Choice" : "2", "Direction" : "", "Stop" : "idk_where_to_go"}
        mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Sabancı", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
        result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

def test_parsesoap_response_choice2_invalid_direction_stop(): # stop name doesn't exist, program should exit
    with pytest.raises(SystemExit):
        inputs = {"Choice" : "2", "Direction" : "abc", "Stop" : "OTOYOL_KAVSAGI"}
        mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Sabancı", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
        result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

def test_parsesoap_response_choice2_invalid_direction_invalid_stop(): # stop name doesn't exist, program should exit
    with pytest.raises(SystemExit):
        inputs = {"Choice" : "2", "Direction" : "abc", "Stop" : "abc"}
        mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Sabancı", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
        result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

def test_parsesoap_response_invalidchoice(): # invalid choice, should raise a ValueError exception
    with pytest.raises(ValueError):
        inputs = {"Choice" : "5", "Direction" : "Kurtköy"}
        mock_etree = etree_constructor([{"AB" : "C", "DE" : "F", "YON_ADI" : "Sabancı", "CART" : "curt", "as" : "df", "DURAK_ADI" : "OTOYOL_KAVSAGI"}])
        result = stop_info.parse_soap_response(inputs, mock_etree) # you have to convert mock_etree to list

def test_print_stops_single_element_input(capsys):
    input = [
        {
                "LINE_CODE" : "KM18",
                "DIRECTION" : "D",
                "DIRECTION_NAME" : "SABANCI ÜNİVERSİTESİ",
                "QUEUE_NUMBER" :"1",
                "STOP_CODE" : "289821",
                "STOP_NAME" : "KURTKÖY MAHALLESİ METRO",
                "X_COORDINATE" : "29.295970",
                "Y_COORDINATE" : "40.909935",
                "STOP_TYPE" : "İETTBAYRAK",
                "SERVICE_REGION" : "Anadolu2",
                "SERVICE_SUB_REGION" : "Pendik",
                "ILCEADI" : "Pendik"
        }
    ]  

    stop_info.print_stops(input)
    captured = capsys.readouterr()

    expected_output = str(
            "\nLINE_CODE: KM18\n" + 
            "DIRECTION: D\n" +
            "DIRECTION_NAME: SABANCI ÜNİVERSİTESİ\n" +
            "QUEUE_NUMBER: 1\n" +
            "STOP_CODE: 289821\n" + 
            "STOP_NAME: KURTKÖY MAHALLESİ METRO\n"+ 
            "X_COORDINATE: 29.295970\n" +
            "Y_COORDINATE: 40.909935\n" +
            "STOP_TYPE: İETTBAYRAK\n" +
            "SERVICE_REGION: Anadolu2\n" +
            "SERVICE_SUB_REGION: Pendik\n" +
            "ILCEADI: Pendik\n\n"
    )
    assert captured.out == expected_output

def test_print_stops_multiple_element_input(capsys):
    input = [
    {
        "LINE_CODE" : "KM18",
        "DIRECTION" : "D",
        "DIRECTION_NAME" : "SABANCI ÜNİVERSİTESİ",
        "QUEUE_NUMBER" :"1",
        "STOP_CODE" : "289821",
        "STOP_NAME" : "KURTKÖY MAHALLESİ METRO",
    },   
    {                
    "LINE_CODE" : "KM18",
    "DIRECTION" : "D",
    "DIRECTION_NAME" : "SABANCI ÜNİVERSİTESİ",
    "QUEUE_NUMBER" : "2",
    "STOP_CODE" : "263191",
    "STOP_NAME" : "ENSAR CADDESİ GİRİŞİ",
    }]
    
    stop_info.print_stops(input)
    captured = capsys.readouterr()
    
    expected_output = str(
            "\nLINE_CODE: KM18\n" +
            "DIRECTION: D\n" +
            "DIRECTION_NAME: SABANCI ÜNİVERSİTESİ\n" +
            "QUEUE_NUMBER: 1\n" + 
            "STOP_CODE: 289821\n" + 
            "STOP_NAME: KURTKÖY MAHALLESİ METRO\n\n" +
            "LINE_CODE: KM18\n" + 
            "DIRECTION: D\n" + 
            "DIRECTION_NAME: SABANCI ÜNİVERSİTESİ\n" +
            "QUEUE_NUMBER: 2\n" +
            "STOP_CODE: 263191\n" +
            "STOP_NAME: ENSAR CADDESİ GİRİŞİ\n\n"
    )
    assert captured.out == expected_output

def test_print_stops_empty(capsys): # shouldn't print anything
    input = []
    
    stop_info.print_stops(input)
    captured = capsys.readouterr()
    
    expected_output = str("\n")
    assert captured.out == expected_output

def test_print_stops_invalid_input(capsys): # should raise exception
    with pytest.raises(AttributeError) as exc:
        input = ["abc"] # no items() method
        stop_info.print_stops(input)