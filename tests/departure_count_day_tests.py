import pytest
import os
import sys
import zeep
from datetime import date
from lxml import etree
import zeep.exceptions

sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import departure_count_day

def test_ms_to_date_converter_1_month():
    input = 2592000000 # 30 days
    output = departure_count_day.ms_to_date_converter(input)

    expected_output = date.fromisoformat('1970-02-01') # January 1970 has 31 days, we start from second day. January 2 -> February 1 (30 days)

    assert output == expected_output

def test_ms_to_date_converter_1_day():
    input = 86400000 # 1 day (in ms)
    output = departure_count_day.ms_to_date_converter(input)

    expected_output = date.fromisoformat('1970-01-03') # January 2 -> January 3

    assert output == expected_output

def test_validate_inputs_valid_date():
    input = "2025-06-30"
    output = departure_count_day.validate_inputs(input)
    
    expected_output = True
    assert output == expected_output

def test_validate_inputs_outofbounds_year_low():
    with pytest.raises(ValueError) as exc:
        input = "2018-11-30"
        output = departure_count_day.validate_inputs(input)
    assert exc.value.args[0] == "Year cannot be less than 2019"

def test_validate_inputs_outofbounds_month_high():
    with pytest.raises(ValueError) as exc:
        input = "2025-13-30"
        output = departure_count_day.validate_inputs(input)
    assert exc.value.args[0] == "Invalid month"

def test_validate_inputs_outofbounds_month_low():
    with pytest.raises(ValueError) as exc:
        input = "2025-0-30"
        output = departure_count_day.validate_inputs(input)
    assert exc.value.args[0] == "Invalid month"

def test_validate_inputs_outofbounds_day_high():
    with pytest.raises(ValueError) as exc:
        input = "2025-01-32"
        output = departure_count_day.validate_inputs(input)
    assert exc.value.args[0] == "Invalid day"

def test_validate_inputs_outofbounds_day_low():
    with pytest.raises(ValueError) as exc:
        input = "2025-01-0"
        output = departure_count_day.validate_inputs(input)
    assert exc.value.args[0] == "Invalid day"

def test_validate_inputs_alpabetic_char_in_yearfield():
    with pytest.raises(ValueError):
        input = "abc-01-10"
        output = departure_count_day.validate_inputs(input)
        
def test_validate_inputs_alpabetic_char_in_monthfield():
    with pytest.raises(ValueError):
        input = "2025-as-0"
        output = departure_count_day.validate_inputs(input)

def test_validate_inputs_alpabetic_char_in_datefield():
    with pytest.raises(ValueError):
        input = "2025-01-ccb"
        output = departure_count_day.validate_inputs(input)

def test_validate_inputs_invalid_format_less_hyphen():
    with pytest.raises(ValueError) as exc:
        input = "2025-0118"
        output = departure_count_day.validate_inputs(input)
    assert exc.value.args[0] == "Incorrect format"

def test_validate_inputs_invalid_format_more_hyphen():
    with pytest.raises(ValueError) as exc:
        input = "2025-01-1-8"
        output = departure_count_day.validate_inputs(input)
    assert exc.value.args[0] == "Incorrect format"

def test_validate_inputs_invalid_format_empty_year():
    with pytest.raises(ValueError) as exc:
        input = "-01-18"
        output = departure_count_day.validate_inputs(input)

def test_validate_inputs_invalid_format_empty_month():
    with pytest.raises(ValueError) as exc:
        input = "2025--18"
        output = departure_count_day.validate_inputs(input)

def test_validate_inputs_invalid_format_empty_day():
    with pytest.raises(ValueError) as exc:
        input = "2025-01-"
        output = departure_count_day.validate_inputs(input)

def test_soap_call_date_with_no_data(capsys):
    with pytest.raises(SystemExit):
        input = "2100-01-01" # UPDATE WHEN WE REACH 2100
        response = departure_count_day.soap_call(input)
    captured = capsys.readouterr()
    expected_response = "No data for given date found!\n"

    assert captured.out == expected_response

def test_soap_call_empty_date():
    with pytest.raises(zeep.exceptions.Fault) as zeep_exc:
        input = "" 
        response = departure_count_day.soap_call(input)
    
    expected_exception_message = "Server was unable to process request. ---> Tarih Zorunlu girilmelidir."
    assert zeep_exc.value.args[0] == expected_exception_message

def test_soap_call_invalid_date():
    with pytest.raises(zeep.exceptions.Fault) as zeep_exc:
        input = "abc" 
        response = departure_count_day.soap_call(input)

def test_soap_call_valid_date():
    input = "2025-06-02"
    response = departure_count_day.soap_call(input)
    assert len(response) > 2

# Copied from scheduled_departure_hours_tests.py

def test_convert_soap_response_to_list_single_element():
    input = '[{"AB": "C", "D": "ef"}]'
    output = departure_count_day.convert_soap_response_to_list(input)

    expected_output = [{"AB": "C", "D": "ef"}]

    assert output == expected_output

def test_convert_soap_response_to_list_multiple_elements():
    input = '[{"AB": "C", "D": "ef"}, {"this": "is", "mock": "data"}]'
    output = departure_count_day.convert_soap_response_to_list(input)

    expected_output = [{"AB": "C", "D": "ef"}, {"this": "is", "mock": "data"}]

    assert output == expected_output

def test_convert_soap_response_to_list_empty():
    input = '[]'
    output = departure_count_day.convert_soap_response_to_list(input)

    expected_output = []

    assert output == expected_output

def test_get_data_of_specific_bus_line_valid():
    response_list = [
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"34","Yolculuk":"687300"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"34A","Yolculuk":"126385"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"500T","Yolculuk":"31175"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"null","Yolculuk":"30093"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"KM18","Yolculuk":"150"},
    ]
    input = ("KM18", response_list)
    output = departure_count_day.get_data_of_specific_bus_line(input[0], input[1])

    expected_output = [{"DAY":"\\/Date(1748811600000)\\/","LINE":"KM18","PASSENGERS":"150"}]
    
    assert output == expected_output

def test_get_data_of_specific_bus_line_busline_doesnt_exist_in_list():
    response_list = [
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"34","Yolculuk":"687300"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"34A","Yolculuk":"126385"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"500T","Yolculuk":"31175"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"null","Yolculuk":"30093"},
    ]
    input = ("KM18", response_list)
    output = departure_count_day.get_data_of_specific_bus_line(input[0], input[1])

    expected_output = []
    
    assert output == expected_output

def test_get_data_of_specific_bus_line_empty_response_list():
    response_list = []
    input = ("KM18", response_list)
    output = departure_count_day.get_data_of_specific_bus_line(input[0], input[1])

    expected_output = []
    
    assert output == expected_output


def test_get_data_of_specific_bus_line_busline_is_empty():
    response_list = [
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"34","Yolculuk":"687300"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"34A","Yolculuk":"126385"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"500T","Yolculuk":"31175"},
        {"Gun":"\\/Date(1748811600000)\\/","Hat":"null","Yolculuk":"30093"},
    ]

    input = ("", response_list)
    output = departure_count_day.get_data_of_specific_bus_line(input[0], input[1])

    expected_output = [
        {"DAY":"\\/Date(1748811600000)\\/","LINE":"34","PASSENGERS":"687300"},
        {"DAY":"\\/Date(1748811600000)\\/","LINE":"34A","PASSENGERS":"126385"},
        {"DAY":"\\/Date(1748811600000)\\/","LINE":"500T","PASSENGERS":"31175"},
        {"DAY":"\\/Date(1748811600000)\\/","LINE":"null","PASSENGERS":"30093"},
    ]
    
    assert output == expected_output

def test_print_elements_single_element(capsys):
    input = [
        {"DAY":"\\/Date(1748811600000)\\/","LINE":"34","PASSENGERS":"687300"}
    ]

    departure_count_day.print_elements(input)
    captured = capsys.readouterr()

    expected_output = str(
        "\nDay: 2025-06-02\n" +
        "Line: 34\n" + 
        "Passengers: 687300\n\n"
    )

    assert captured.out == expected_output

def test_print_elements_multiple_element(capsys):
    input = [
        {"DAY":"\\/Date(1748811600000)\\/","LINE":"34","PASSENGERS":"687300"},
        {"DAY":"\\/Date(1748811600000)\\/","LINE":"34A","PASSENGERS":"126385"},
        {"DAY":"\\/Date(1748811600000)\\/","LINE":"500T","PASSENGERS":"31175"},
        {"DAY":"\\/Date(1748811600000)\\/","LINE":"null","PASSENGERS":"30093"},
    ]

    departure_count_day.print_elements(input)
    captured = capsys.readouterr()

    expected_output = str(
        "\nDay: 2025-06-02\n" +
        "Line: 34\n" + 
        "Passengers: 687300\n\n" + 
        
        "Day: 2025-06-02\n" +
        "Line: 34A\n" + 
        "Passengers: 126385\n\n" + 
        
        "Day: 2025-06-02\n" +
        "Line: 500T\n" + 
        "Passengers: 31175\n\n" + 
                
        "Day: 2025-06-02\n" +
        "Line: null\n" + 
        "Passengers: 30093\n\n" 
    )

    assert captured.out == expected_output

def test_print_elements_no_elements(capsys):
    input = []

    departure_count_day.print_elements(input)
    captured = capsys.readouterr()

    expected_output = str(
        "\n"
    )

    assert captured.out == expected_output
