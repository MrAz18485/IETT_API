import pytest
import os
import sys
import json

sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import announcments

def test_soap_call():
    soap_call = announcments.soap_call()
    assert len(soap_call) != 0 # I mean, its possible that there's no announcments


def test_soap_response_to_list_nonempty_response_single_dictionary():
    input = '[{"A": "BC", "D": "ef"}]'

    result = announcments.soap_response_to_list(input)
    expected_output = [{"A": "BC", "D": "ef"}]

    assert result == expected_output

def test_soap_response_to_list_nonempty_response_multiple_dictionary():
    input = '[{"A": "BC", "D": "ef"}, {"B": "CD", "E": "fg"}]'

    result = announcments.soap_response_to_list(input)
    expected_output = [{"A": "BC", "D": "ef"}, {"B": "CD", "E": "fg"}]

    assert result == expected_output

def test_soap_response_to_list_empty_response():
    input = "[]"

    result = announcments.soap_response_to_list(input)
    expected_output = []

    assert result == expected_output


def test_get_specific_bus_lines_announcments_busline_exists_single_element_response():
    input = ["1", [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}, {"HATKODU": "2", "HAT": "NA", "MESAJ": "TestMessage3"}]]
    result = announcments.get_specific_bus_lines_announcments(input[0], input[1])

    expected_result = [{"LINE_CODE": "1", "LINE": "NA", "MESSAGE": "TestMessage1"}]
    
    assert result == expected_result

def test_get_specific_bus_lines_announcments_busline_exists_multiple_element_response():
    input = ["1", [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}, {"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage2"}, {"HATKODU": "2", "HAT": "NA", "MESAJ": "TestMessage3"}]]
    result = announcments.get_specific_bus_lines_announcments(input[0], input[1])

    expected_result = [{"LINE_CODE": "1", "LINE": "NA", "MESSAGE": "TestMessage1"}, {"LINE_CODE": "1", "LINE": "NA", "MESSAGE": "TestMessage2"}]
    
    assert result == expected_result

def test_get_specific_bus_lines_announcments_busline_exists_invalid_busline(capsys):
    with pytest.raises(SystemExit):
        input = ["3", [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}, {"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage2"}, {"HATKODU": "2", "HAT": "NA", "MESAJ": "TestMessage3"}]]
        result = announcments.get_specific_bus_lines_announcments(input[0], input[1])
    captured = capsys.readouterr()
    expected_result = "Announcments not found\n"
    assert captured.out == expected_result


def test_print_elements_single_element_input(capsys):
    input = [
        {"LINE_CODE": "93M", "LINE": "ZEYTINBURNU - MECIDIYEKÖY", "TYPE": "Günlük", "UPDATE_TIME": "Kayit Saati: 12:01", "MESSAGE": "mock"}
    ]
    announcments.print_elements(input)
    captured = capsys.readouterr()
    assert captured.out == str(
        "\n" +
        "Line Code: 93M\n" +
        "Line: ZEYTINBURNU - MECIDIYEKÖY\n" +
        "Type: Günlük\n" + 
        "Update Time: Kayit Saati: 12:01\n" +
        "Message: mock\n\n"
    )

def test_print_elements_multiple_element_input(capsys):
    input = [
        {"LINE_CODE": "93M", "LINE": "ZEYTINBURNU - MECIDIYEKÖY", "TYPE": "Günlük", "UPDATE_TIME": "Kayit Saati: 12:01", "MESSAGE": "mock"},
        {'LINE_CODE': '93T', 'LINE': 'ZEYTINBURNU - TAKSIM', 'TYPE': 'Günlük', 'UPDATE_TIME': 'Kayit Saati: 12:01', 'MESSAGE': ''},
        {'LINE_CODE': '97GE', 'LINE': '15 TEMMUZ MAHALLESI - EMINÖNÜ', 'TYPE': 'Sefer', 'UPDATE_TIME': 'Kayit Saati: 04:27', 'MESSAGE': 'nock'},
    ]
    announcments.print_elements(input)
    captured = capsys.readouterr()
    assert captured.out == str(
        "\n" +
        "Line Code: 93M\n" +
        "Line: ZEYTINBURNU - MECIDIYEKÖY\n" +
        "Type: Günlük\n" + 
        "Update Time: Kayit Saati: 12:01\n" +
        "Message: mock\n\n" +

        "Line Code: 93T\n" +
        "Line: ZEYTINBURNU - TAKSIM\n" +
        "Type: Günlük\n" + 
        "Update Time: Kayit Saati: 12:01\n" +
        "Message: \n\n" +

        "Line Code: 97GE\n" +
        "Line: 15 TEMMUZ MAHALLESI - EMINÖNÜ\n" +
        "Type: Sefer\n" + 
        "Update Time: Kayit Saati: 04:27\n" +
        "Message: nock\n\n"
    )

def test_print_elements_empty_input(capsys):
    input = []
    announcments.print_elements(input)
    captured = capsys.readouterr()
    assert captured.out == str("\n")
