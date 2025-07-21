import lxml.etree
import pytest
import zeep
import sys
import lxml
from unittest.mock import patch
import zeep.client
import zeep.exceptions

sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import get_crash_info

def test_validate_input_valid():
    input = "2025-06-11"
    output = get_crash_info.validate_date_input(input)
    expected_output = True

    assert output == expected_output

def test_validate_input_invalid_length():
    with pytest.raises(ValueError) as val_exc:
        input = "2025-06-11-1"
        output = get_crash_info.validate_date_input(input)
    
    exception_message = str(val_exc.value) 
    expected_message = "Incorrect format"
    assert exception_message == expected_message 

def test_validate_input_year_lessthan_2019():
    with pytest.raises(ValueError) as val_exc:
        input = "2018-06-11"
        output = get_crash_info.validate_date_input(input)
    
    exception_message = str(val_exc.value) 
    expected_message = "Year cannot be less than 2019"
    assert exception_message == expected_message 

def test_validate_input_month_lessthan_1():
    with pytest.raises(ValueError) as val_exc:
        input = "2021-00-11"
        output = get_crash_info.validate_date_input(input)
    
    exception_message = str(val_exc.value) 
    expected_message = "Invalid month"
    assert exception_message == expected_message 

def test_validate_input_month_morethan_12():
    with pytest.raises(ValueError) as val_exc:
        input = "2021-15-11"
        output = get_crash_info.validate_date_input(input)
    
    exception_message = str(val_exc.value) 
    expected_message = "Invalid month"
    assert exception_message == expected_message 

def test_validate_input_day_negative():
    with pytest.raises(ValueError) as val_exc:
        input = "2021-01--1"
        output = get_crash_info.validate_date_input(input)
    
    exception_message = str(val_exc.value) 
    expected_message = "Incorrect format"
    assert exception_message == expected_message 

def test_validate_input_day_lessthan_1():
    with pytest.raises(ValueError) as val_exc:
        input = "2021-01-00"
        output = get_crash_info.validate_date_input(input)
    
    exception_message = str(val_exc.value) 
    expected_message = "Invalid day"
    assert exception_message == expected_message 

def test_validate_input_day_morethan_31():
    with pytest.raises(ValueError) as val_exc:
        input = "2021-01-35"
        output = get_crash_info.validate_date_input(input)
    
    exception_message = str(val_exc.value) 
    expected_message = "Invalid day"
    assert exception_message == expected_message 

def test_validate_input_integer_input():
    with pytest.raises(AttributeError) as attr_exc:
        input = 12
        output = get_crash_info.validate_date_input(input)
    assert True

def test_validate_input_boolean_input():
    with pytest.raises(AttributeError) as attr_exc:
        input = True
        output = get_crash_info.validate_date_input(input)
    assert True

# To avoid making real API calls, I'm using the pytest_mock library
def test_make_soap_call_nonempty_response(mocker):
    patch_return_value = lxml.etree.Element("NewDataSet"); patch_return_value.extend([lxml.etree.Element("Table"), lxml.etree.Element("Table")])
    with patch("get_crash_info.make_soap_call", return_value=patch_return_value):
        response = get_crash_info.make_soap_call("2025-07-19", zeep.Client(wsdl='xml/departure.xml'))
        expected_response = lxml.etree.Element("NewDataSet"); expected_response.extend([lxml.etree.Element("Table"), lxml.etree.Element("Table")])
        assert lxml.etree.tostring(response) == lxml.etree.tostring(expected_response)
    
def test_make_soap_call_empty_response(mocker):
    with patch("get_crash_info.make_soap_call", return_value=lxml.etree.Element("NewDataSet")):
        response = get_crash_info.make_soap_call("2025-07-19", zeep.Client(wsdl='xml/departure.xml'))
        expected_response = lxml.etree.Element("NewDataSet")
        assert lxml.etree.tostring(response) == lxml.etree.tostring(expected_response)

def test_make_soap_call_fault_response(mocker):
    with patch("get_crash_info.make_soap_call", side_effect= zeep.exceptions.Fault("")): # exception message is not really important here
        with pytest.raises(zeep.exceptions.Fault) as fault_exc:
            response = get_crash_info.make_soap_call("2025-07-19", zeep.Client(wsdl='xml/departure.xml'))

def test_validate_soap_response_nonempty_response():
    input = lxml.etree.Element("NewDataSet"); input.extend([lxml.etree.Element("Table"), lxml.etree.Element("Table")])
    output = get_crash_info.validate_soap_response(input)
    expected_output = True
    assert output == expected_output 

def test_validate_soap_response_empty_response():
    with pytest.raises(SystemExit):
        input = lxml.etree.Element("NewDataSet")
        output = get_crash_info.validate_soap_response(input)

def test_print_elements_single_element(capsys):
    input = [{"AB": "C", "DE": "FG"}]
    get_crash_info.print_elements(input)
    captured = capsys.readouterr()
    expected_output = str(
        "\n" + "AB: C\n" + "DE: FG\n" + "\n"
    )
    assert captured.out == expected_output

def test_print_elements_multiple_element(capsys):
    input = [{"AB": "C", "DE": "FG"}, {"This is": "made for", "Testing": "purposes"}]
    get_crash_info.print_elements(input)
    captured = capsys.readouterr()
    expected_output = str(
        "\n" + "AB: C\n" + "DE: FG\n" + "\n" + "This is: made for\n" + "Testing: purposes\n" + "\n"
    )

    assert captured.out == expected_output
    