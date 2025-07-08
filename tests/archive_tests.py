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


def etree_constructor(tables): # helper for test_parse_xml. 
    root_elem = lxml.etree.Element("NewDataSet")
    for i in range(len(tables)):
        root_elem.append(lxml.etree.Element("Table"))
    curr_table_index = 0
    for table in tables:
        for key, value in table.items():
            element = lxml.etree.Element(key)
            element.text = value
            root_elem[curr_table_index].append(element)
        curr_table_index += 1
    return root_elem

def test_parse_xml_single_element_tree():
    input = etree_constructor([{"AB": "C", "D":"EF"}])
    output = archive.parse_xml(input)
    
    expected_output = [{"AB": "C", "D": "EF"}]
    assert output == expected_output

def test_parse_xml_multiple_element_tree():
    input = etree_constructor([{"AB": "C", "D":"EF"}, {"HATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}])
    output = archive.parse_xml(input)
    
    expected_output = [{"AB": "C", "D":"EF"}, {"HATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_parse_xml_empty_tree():
    input = etree_constructor([])
    output = archive.parse_xml(input)

    expected_output = []
    assert output == expected_output

def test_parse_xml_invalid_input():
    with pytest.raises(TypeError) as type_exc:
        output = archive.parse_xml(["abc", "def"])
    expected_exception_message_header = "Invalid type <class 'str'> passed to parse_xml function"
    assert expected_exception_message_header == type_exc.value.args[0]


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
    input = ([{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}], "")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_get_specific_bus_line_data_single_element_existing_buslinecode():
    input = ([{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}], "KM18")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_get_specific_bus_line_data_single_element_nonexistent_buslinecode():
    input = ([{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}], "abc")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = []
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_empty_buslinecode_multiple_element_output_case():
    input = ([{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"SHATKODU": "16D", "HATADI": "ALTKAYNARCA / PENDİK - KADIKÖY"}], "")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"SHATKODU": "16D", "HATADI": "ALTKAYNARCA / PENDİK - KADIKÖY"}]
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_existing_buslinecode_single_element_output_case():
    input = ([{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"SHATKODU": "16D", "HATADI": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"SHATKODU": "133AK", "HATADI": "TEPEÖREN - KARTAL"}], "133AK")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"SHATKODU": "133AK", "HATADI": "TEPEÖREN - KARTAL"}]
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_existing_buslinecode_multiple_element_output_case():
    input = ([{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"SHATKODU": "16D", "HATADI": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"SHATKODU": "133AK", "HATADI": "TEPEÖREN - KARTAL"},
              {"SHATKODU": "133AK", "HATADI": "TEPEÖREN - KARTAL"},
              {"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}], "KM18")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"},
                       {"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_nonexistent_buslinecode():
    input = ([{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"SHATKODU": "16D", "HATADI": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"SHATKODU": "133AK", "HATADI": "TEPEÖREN - KARTAL"}], "defg")
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
    input = [{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}]
    archive.print_elements(input)
    captured = capsys.readouterr()
    expected_output = str(
        "\nSHATKODU: KM18\n" +
        "HATADI: SABANCI ÜNİ - KURTKÖY METRO\n\n"
    )
    assert captured.out == expected_output

def test_print_elements_multiple_element_input(capsys):
    input = [{"SHATKODU": "KM18", "HATADI": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"SHATKODU": "16D", "HATADI": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"SHATKODU": "133AK", "HATADI": "TEPEÖREN - KARTAL"}]
    archive.print_elements(input)
    captured = capsys.readouterr()
    expected_output = str(
        "\nSHATKODU: KM18\n" +
        "HATADI: SABANCI ÜNİ - KURTKÖY METRO\n\n" +
        "SHATKODU: 16D\n" +
        "HATADI: ALTKAYNARCA / PENDİK - KADIKÖY\n\n" +
        "SHATKODU: 133AK\n" +
        "HATADI: TEPEÖREN - KARTAL\n\n" 
    )
    assert captured.out == expected_output