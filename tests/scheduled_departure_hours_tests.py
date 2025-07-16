import pytest
import os
import sys
from lxml import etree
import zeep
import zeep.exceptions
sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import scheduled_departure_hours

wsdl = "xml/PlanlananSeferSaati.asmx.xml"

def test_validate_and_format_line_code_day_valid_linecode_day():
    input = ("KM18" , "I")
    result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])
    expected_result = {"Line_Code": "KM18", "Day": "I"}

    assert result == expected_result

def test_validate_and_format_line_code_day_lowercase_line_code_uppercase_day():
    input = ("üm73" , "C")
    result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])
    expected_result = {"Line_Code": "ÜM73", "Day": "C"}

    assert result == expected_result

def test_validate_and_format_line_code_day_uppercase_line_code_lowercase_day():
    input = ("34i" , "p")
    result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])
    expected_result = {"Line_Code": "34İ", "Day": "P"}

    assert result == expected_result

def test_validate_and_format_line_code_day_lowercase_line_code_lowercase_day():
    input = ("km43" , "ı")
    result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])
    expected_result = {"Line_Code": "KM43", "Day": "I"}

    assert result == expected_result

def test_validate_and_format_line_code_day_empty_linecode_valid_day():
    with pytest.raises(ValueError):
        input = ("" , "I")
        result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])

def test_validate_and_format_line_code_day_valid_linecode_invalid_day():
    with pytest.raises(ValueError):
        input = ("KM18" , "ç")
        result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])

def test_soap_call_empty_line_code():
    with pytest.raises(zeep.exceptions.Fault):
        input = ""
        response = scheduled_departure_hours.soap_call(input)
 
def test_soap_call_nonexistent_line_code():
    with pytest.raises(SystemExit):
        input = "boyle_bir_hat_yok"
        response = scheduled_departure_hours.soap_call(input)


def test_convert_soap_response_to_list_single_element():
    input = '[{"AB": "C", "D": "ef"}]'
    output = scheduled_departure_hours.convert_soap_response_to_list(input)

    expected_output = [{"AB": "C", "D": "ef"}]

    assert output == expected_output

def test_convert_soap_response_to_list_multiple_elements():
    input = '[{"AB": "C", "D": "ef"}, {"this": "is", "mock": "data"}]'
    output = scheduled_departure_hours.convert_soap_response_to_list(input)

    expected_output = [{"AB": "C", "D": "ef"}, {"this": "is", "mock": "data"}]

    assert output == expected_output

def test_convert_soap_response_to_list_empty():
    input = '[]'
    output = scheduled_departure_hours.convert_soap_response_to_list(input)

    expected_output = []

    assert output == expected_output


def test_obtain_unique_bus_line_names_single_line_input():
    input = [{"LINE_NAME": "SABANCI ÜNİ./MEDENİYET ÜNİ", "some_data": "here_and_there"}]
    output = scheduled_departure_hours.obtain_unique_bus_line_names(input)

    expected_output = ["SABANCI ÜNİ./MEDENİYET ÜNİ"]

    assert output == expected_output

def test_obtain_unique_bus_line_names_multiple_line_input():
    input = [
        {"LINE_NAME": "SABANCI ÜNİ./MEDENİYET ÜNİ", "some_data": "here_and_there"}, 
        {"LINE_NAME": "SABANCI ÜNİ./MEDENİYET ÜNİ", "some_data": "here_and_there"},
        {"LINE_NAME": "AKFIRAT EVLERİ - KARTAL METRO", "some_data": "here_and_there"}
    ]
    output = scheduled_departure_hours.obtain_unique_bus_line_names(input)

    expected_output = ["SABANCI ÜNİ./MEDENİYET ÜNİ", "AKFIRAT EVLERİ - KARTAL METRO"]

    assert output == expected_output

def test_obtain_unique_bus_line_names_empty_input():
    input = []
    output = scheduled_departure_hours.obtain_unique_bus_line_names(input)

    expected_output = []

    assert output == expected_output

def test_print_bus_line_names_single_element_list(capsys):
    input = ["SABANCI ÜNİ./MEDENİYET ÜNİ"]
    scheduled_departure_hours.print_bus_line_names(input)
    captured = capsys.readouterr()

    expected_output = "\nSABANCI ÜNİ./MEDENİYET ÜNİ\n"

    assert captured.out == expected_output

def test_print_bus_line_names_multiple_element_list(capsys):
    input = ["SABANCI ÜNİ./MEDENİYET ÜNİ", "AKFIRAT EVLERİ - KARTAL METRO"]
    scheduled_departure_hours.print_bus_line_names(input)
    captured = capsys.readouterr()

    expected_output = "\nSABANCI ÜNİ./MEDENİYET ÜNİ\n" + "AKFIRAT EVLERİ - KARTAL METRO\n"

    assert captured.out == expected_output

def test_print_bus_line_names_empty_list(capsys):
    input = []
    scheduled_departure_hours.print_bus_line_names(input)
    captured = capsys.readouterr()

    expected_output = "\n"

    assert captured.out == expected_output


def test_validate_direction_valid_input():
    input = "G"
    output = scheduled_departure_hours.validate_direction(input)

    expected_output = "G"
    
    assert output == expected_output

def test_validate_direction_invalid_input():
    with pytest.raises(ValueError):
        input = "Ş"
        output = scheduled_departure_hours.validate_direction(input)
    
def test_validate_direction_empty_input():
    with pytest.raises(ValueError):
        input = ""
        output = scheduled_departure_hours.validate_direction(input)

def test_get_specific_timetables_single_element_list():
    inputs = ([
        {"LINE_CODE": "KM18", "DIRECTION": "G", "DAY_TYPE": "I"}, 
    ], {"Direction": "G", "Day": "I"})
    output = scheduled_departure_hours.get_specific_timetables(inputs[0], inputs[1])

    expected_output = [{"LINE_CODE": "KM18", "DIRECTION": "G", "DAY_TYPE": "I"}]
    
    assert output == expected_output

def test_get_specific_timetables_multiple_element_list():
    inputs = ([
        {"LINE_CODE": "KM18", "DIRECTION": "G", "DAY_TYPE": "P"}, 
        {"LINE_CODE": "KM18", "DIRECTION": "G", "DAY_TYPE": "C"}, 
        {"LINE_CODE": "KM18", "DIRECTION": "G", "DAY_TYPE": "I"}, 
        {"LINE_CODE": "KM18", "DIRECTION": "D", "DAY_TYPE": "P"}, 
        {"LINE_CODE": "KM18", "DIRECTION": "D", "DAY_TYPE": "C"}, 
        {"LINE_CODE": "KM18", "DIRECTION": "D", "DAY_TYPE": "I"}, 
    ], {"Direction": "D", "Day": "C"})
    output = scheduled_departure_hours.get_specific_timetables(inputs[0], inputs[1])

    expected_output = [{"LINE_CODE": "KM18", "DIRECTION": "D", "DAY_TYPE": "C"}]
    
    assert output == expected_output

def test_get_specific_timetables_multiple_element_list_no_timetable_day():
    with pytest.raises(SystemExit):
        inputs = ([
            {"LINE_CODE": "KM18", "DIRECTION": "G", "DAY_TYPE": "C"}, 
            {"LINE_CODE": "KM18", "DIRECTION": "G", "DAY_TYPE": "I"}, 
            {"LINE_CODE": "KM18", "DIRECTION": "D", "DAY_TYPE": "C"}, 
            {"LINE_CODE": "KM18", "DIRECTION": "D", "DAY_TYPE": "I"}, 
        ], {"Direction": "G", "Day": "P"})
        
        output = scheduled_departure_hours.get_specific_timetables(inputs[0], inputs[1])

def test_print_dictionary_single(capsys):
    input = [
        {"LINE_CODE":"KM18","LINE_NAME":"SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL","ROUTE":"KM18_G_D0","DIRECTION":"G","DAY_TYPE":"I","ROUTE_SIGN":"None","SERVICE_TYPE":"Normal","TIME_INFO":"09:00"},
    ]
    scheduled_departure_hours.print_dictionary(input)
    captured = capsys.readouterr()

    expected_output = str(
        "\nLine Code:  KM18\n" +
        "Line Name:  SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL\n" +
        "Route Code:  KM18_G_D0\n" +
        "Direction:  G\n" +
        "Day Type:  I\n" + 
        "Route Sign:  None\n" +
        "Service Type:  Normal\n" +
        "Time Information:  09:00 \n\n"  
    )

    assert captured.out == expected_output

def test_print_dictionary_multiple(capsys):
    input = [
        {"LINE_CODE":"KM18","LINE_NAME":"SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL","ROUTE":"KM18_G_D0","DIRECTION":"G","DAY_TYPE":"I","ROUTE_SIGN":"None","SERVICE_TYPE":"Normal","TIME_INFO":"09:00"},
        {"LINE_CODE":"KM18","LINE_NAME":"PENDİK/PENDİK YHT-SABİHA GÖKÇEN HAVALİMANI","ROUTE":"KM18_G_D4155","DIRECTION":"G","DAY_TYPE":"I","ROUTE_SIGN":"None","SERVICE_TYPE":"Ara Dinlen","TIME_INFO":"09:30"},
        {"LINE_CODE":"KM18","LINE_NAME":"SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL","ROUTE":"KM18_G_D0","DIRECTION":"G","DAY_TYPE":"I","ROUTE_SIGN":"None","SERVICE_TYPE":"Normal","TIME_INFO":"10:30"},
    ]
    scheduled_departure_hours.print_dictionary(input)
    captured = capsys.readouterr()

    expected_output = str(
        "\nLine Code:  KM18\n" +
        "Line Name:  SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL\n" +
        "Route Code:  KM18_G_D0\n" +
        "Direction:  G\n" +
        "Day Type:  I\n" + 
        "Route Sign:  None\n" +
        "Service Type:  Normal\n" +
        "Time Information:  09:00 \n\n" +

        "Line Code:  KM18\n" +
        "Line Name:  PENDİK/PENDİK YHT-SABİHA GÖKÇEN HAVALİMANI\n" +
        "Route Code:  KM18_G_D4155\n" + 
        "Direction:  G\n" +
        "Day Type:  I\n" +
        "Route Sign:  None\n" +
        "Service Type:  Ara Dinlen\n" + 
        "Time Information:  09:30 \n\n" +

        "Line Code:  KM18\n" +
        "Line Name:  SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL\n"
        "Route Code:  KM18_G_D0\n" +
        "Direction:  G\n" +
        "Day Type:  I\n" +
        "Route Sign:  None\n" +
        "Service Type:  Normal\n" +
        "Time Information:  10:30 \n\n"
    )

    assert captured.out == expected_output

def test_print_dictionary_empty(capsys):
    input = []
    scheduled_departure_hours.print_dictionary(input)
    captured = capsys.readouterr()

    expected_output = "\n"

    assert captured.out == expected_output