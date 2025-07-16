import lxml
import pytest
import os
import sys
import zeep
import zeep.exceptions
sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import total_fuel_consumption

wsdl = "https://api.ibb.gov.tr/iett/AracAnaVeri/AracOzellik.asmx?wsdl"

def test_take_inputs_valid1():
    with open("test_take_inputs_valid1.txt", "w") as file1:
        file1.write("2025 02\n")
    sys.stdin = open("test_take_inputs_valid1.txt", "r")
    output = total_fuel_consumption.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_valid1.txt")

    expected_output = {"Year": "2025", "Month": "02"}
    assert output == expected_output

def test_take_inputs_valid2():
    with open("test_take_inputs_valid2.txt", "w") as file1:
        file1.write("2024 5\n")
    sys.stdin = open("test_take_inputs_valid2.txt", "r")
    output = total_fuel_consumption.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_valid2.txt")
    
    expected_output = {"Year": "2024", "Month": "5"}
    assert output == expected_output

def test_take_inputs_invalid_format1():
    with pytest.raises(ValueError):
        with open("test_take_inputs_invalid_format1.txt", "w") as file1:
            file1.write("abc\n")
        sys.stdin = open("test_take_inputs_invalid_format1.txt", "r")
        output = total_fuel_consumption.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_invalid_format1.txt")

def test_take_inputs_invalid_format2():
    with pytest.raises(ValueError):
        with open("test_take_inputs_invalid_format2.txt", "w") as file1:
            file1.write("ab c\n")
        sys.stdin = open("test_take_inputs_invalid_format2.txt", "r")
        output = total_fuel_consumption.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_invalid_format2.txt")

def test_take_inputs_invalid_format3():
    with pytest.raises(ValueError):
        with open("test_take_inputs_invalid_format3.txt", "w") as file1:
            file1.write("1 a\n")
        sys.stdin = open("test_take_inputs_invalid_format3.txt", "r")
        output = total_fuel_consumption.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_invalid_format3.txt")

def test_take_inputs_invalid_format4():
    with pytest.raises(ValueError):
        with open("test_take_inputs_invalid_format4.txt", "w") as file1:
            file1.write("a 1\n")
        sys.stdin = open("test_take_inputs_invalid_format4.txt", "r")
        output = total_fuel_consumption.take_inputs()
    sys.stdin = sys.__stdin__
    os.remove("test_take_inputs_invalid_format4.txt")

def test_convert_dict_strings_to_int_valid_with_zero_at_start_of_month(): # with 0 in front of month
    input_dict = {"Year": "2025", "Month": "02"}
    output = total_fuel_consumption.convert_dict_strings_to_int(input_dict)
    expected_output = {"Year": 2025, "Month": 2}
    assert output == expected_output

def test_convert_dict_strings_to_int_valid_without_zero_at_start_of_month(): # without 0 in front of month
    input_dict = {"Year": "2025", "Month": "5"}
    output = total_fuel_consumption.convert_dict_strings_to_int(input_dict)
    expected_output = {"Year": 2025, "Month": 5}
    assert output == expected_output

def test_convert_dict_strings_to_int_invalid_month(): 
    with pytest.raises(ValueError):
        input_dict = {"Year": "2025", "Month": "a"}
        output = total_fuel_consumption.convert_dict_strings_to_int(input_dict)

def test_convert_dict_strings_to_int_invalid_year(): 
    with pytest.raises(ValueError):
        input_dict = {"Year": "a", "Month": "2025"}
        output = total_fuel_consumption.convert_dict_strings_to_int(input_dict)

def test_convert_dict_strings_to_int_empty_year(): 
    with pytest.raises(ValueError):
        input_dict = {"Year": "", "Month": "2025"}
        output = total_fuel_consumption.convert_dict_strings_to_int(input_dict)

def test_soap_call_before_2019():
    with pytest.raises(zeep.exceptions.Fault):
        input_dict = {"Year": 2018, "Month": 1}
        output = total_fuel_consumption.soap_call(input_dict)

def test_soap_call_incorrect_date(capsys):
    with pytest.raises(SystemExit): # when exit() gets called we exit with pytest.raises()
        input_dict = {"Year": 2020, "Month": 15}
        output = total_fuel_consumption.soap_call(input_dict)
    captured = capsys.readouterr()
    assert captured.out == "No data found\n" # Yes it exited, but with what message? It must be this message

def test_convert_to_dictionary_valid():
    input = '[{"ToplamAkarYakit":2043555.95,"Gun":2,"Ay":5,"Yil":2025}, {"ToplamAkarYakit":288769.82,"Gun":3,"Ay":5,"Yil":2025}]'
    output = total_fuel_consumption.convert_soap_response_to_dictionary(input)
    expected_output = [{"ToplamAkarYakit":2043555.95,"Gun":2,"Ay":5,"Yil":2025}, {"ToplamAkarYakit":288769.82,"Gun":3,"Ay":5,"Yil":2025}]
    assert output == expected_output

def test_convert_to_dictionary_empty():
    input = '[]'
    output = total_fuel_consumption.convert_soap_response_to_dictionary(input)
    expected_output = []
    assert output == expected_output

def test_print_dictionary_single_line(capsys):
    input = [
        {"Total_Fuel": 10, "Day": 10, "Month": 10, "Year": 2023}
    ]
    total_fuel_consumption.print_dictionary(input)
    captured = capsys.readouterr()

    expected_output = str(
        "Total_Fuel: 10L\n" +
        "Day: 10\n" + 
        "Month: 10\n" +
        "Year: 2023\n\n" 
    )
    assert captured.out == expected_output

def test_print_dictionary_multiple_line(capsys):
    input = [
        {"Total_Fuel": 10, "Day": 10, "Month": 10, "Year": 2023},
        {"Total_Fuel": 20, "Day": 11, "Month": 10, "Year": 2023}
    ]
    total_fuel_consumption.print_dictionary(input)
    captured = capsys.readouterr()

    expected_output = str(
        "Total_Fuel: 10L\n" +
        "Day: 10\n" + 
        "Month: 10\n" +
        "Year: 2023\n\n" +
        "Total_Fuel: 20L\n" +
        "Day: 11\n" + 
        "Month: 10\n" +
        "Year: 2023\n\n" 
    )
    assert captured.out == expected_output

def test_print_dictionary_empty_input(capsys):
    input = []
    total_fuel_consumption.print_dictionary(input)
    captured = capsys.readouterr()

    expected_output = str()
    assert captured.out == expected_output