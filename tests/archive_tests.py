import sys
import pytest
import zeep
import lxml

sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import archive

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"


def test_validate_date_input_valid():
    input = "20250601"
    response = archive.validate_date_input(input)
    assert response == True

def test_validate_date_input_invalid_year(capsys):
    with pytest.raises(ValueError) as val_exc:
        input = "abcd0601"
        response = archive.validate_date_input(input)
    expected_exc_message = "Incorrect format"
    assert val_exc.value.args[0] == expected_exc_message

def test_validate_date_input_valid_date_invalid_length_missing_leading_zero_at_month_field(capsys):
    with pytest.raises(ValueError) as val_exc:
        input = "2025601" # should be 20250611 instead of 2025611
        response = archive.validate_date_input(input) 
    expected_exc_message = "Incorrect format"
    assert val_exc.value.args[0] == expected_exc_message

def test_validate_date_input_valid_date_invalid_length_missing_leading_zero_at_day_field(capsys):
    with pytest.raises(ValueError) as val_exc:
        input = "2025061" # should be 20250601 instead of 2025061
        response = archive.validate_date_input(input)
    expected_exc_message = "Incorrect format"
    assert val_exc.value.args[0] == expected_exc_message


def test_soap_call_invalid_date(capsys):
    with pytest.raises(zeep.exceptions.Fault) as zeep_exc:
        input = "abcdefgh"
        response = archive.soap_call(input)
    expected_message_substring = "Server was unable to process request."
    assert expected_message_substring in zeep_exc.value.args[0]

def test_soap_call_date_with_no_data(capsys):
    with pytest.raises(SystemExit):
        input = "20190101"
        response = archive.soap_call(input)
    captured = capsys.readouterr()
    expected_message = "No data found\n"
    assert captured.out == expected_message

def test_get_specific_bus_line_data_no_element_empty_buslinecode():
    input = ([], "")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = []
    assert output == expected_output

def test_get_specific_bus_line_data_no_element_nonempty_buslinecode():
    input = ([], "abc")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = []
    assert output == expected_output

def test_get_specific_bus_line_data_single_element_empty_buslinecode():
    input = ([{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}], "")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_get_specific_bus_line_data_single_element_existing_buslinecode():
    input = ([{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}], "KM18")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_get_specific_bus_line_data_single_element_nonexistent_buslinecode():
    input = ([{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}], "abc")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = []
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_empty_buslinecode_multiple_element_output_case():
    input = ([{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"LINE_CODE": "16D", "LINE_NAME": "ALTKAYNARCA / PENDİK - KADIKÖY"}], "")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"LINE_CODE": "16D", "LINE_NAME": "ALTKAYNARCA / PENDİK - KADIKÖY"}]
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_existing_buslinecode_single_element_output_case():
    input = ([{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"LINE_CODE": "16D", "LINE_NAME": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"LINE_CODE": "133AK", "LINE_NAME": "TEPEÖREN - KARTAL"}], "133AK")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"LINE_CODE": "133AK", "LINE_NAME": "TEPEÖREN - KARTAL"}]
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_existing_buslinecode_multiple_element_output_case():
    input = ([{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"LINE_CODE": "16D", "LINE_NAME": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"LINE_CODE": "133AK", "LINE_NAME": "TEPEÖREN - KARTAL"},
              {"LINE_CODE": "133AK", "LINE_NAME": "TEPEÖREN - KARTAL"},
              {"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}], "KM18")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"},
                       {"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_nonexistent_buslinecode():
    input = ([{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"LINE_CODE": "16D", "LINE_NAME": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"LINE_CODE": "133AK", "LINE_NAME": "TEPEÖREN - KARTAL"}], "defg")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = []
    assert output == expected_output


def test_print_elements_empty_input(capsys):
    input = []
    archive.print_elements(input)
    captured = capsys.readouterr()
    expected_output = str("\n")
    assert captured.out == expected_output

def test_print_elements_single_element_input(capsys):
    input = [{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}]
    archive.print_elements(input)
    captured = capsys.readouterr()
    expected_output = str(
        "\nLINE_CODE: KM18\n" +
        "LINE_NAME: SABANCI ÜNİ - KURTKÖY METRO\n\n"
    )
    assert captured.out == expected_output

def test_print_elements_multiple_element_input(capsys):
    input = [{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"LINE_CODE": "16D", "LINE_NAME": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"LINE_CODE": "133AK", "LINE_NAME": "TEPEÖREN - KARTAL"}]
    archive.print_elements(input)
    captured = capsys.readouterr()
    expected_output = str(
        "\nLINE_CODE: KM18\n" +
        "LINE_NAME: SABANCI ÜNİ - KURTKÖY METRO\n\n" +
        "LINE_CODE: 16D\n" +
        "LINE_NAME: ALTKAYNARCA / PENDİK - KADIKÖY\n\n" +
        "LINE_CODE: 133AK\n" +
        "LINE_NAME: TEPEÖREN - KARTAL\n\n" 
    )
    assert captured.out == expected_output