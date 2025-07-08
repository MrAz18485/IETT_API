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

    expected_result = [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}]
    
    assert result == expected_result

def test_get_specific_bus_lines_announcments_busline_exists_multiple_element_response():
    input = ["1", [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}, {"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage2"}, {"HATKODU": "2", "HAT": "NA", "MESAJ": "TestMessage3"}]]
    result = announcments.get_specific_bus_lines_announcments(input[0], input[1])

    expected_result = [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}, {"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage2"}]
    
    assert result == expected_result

def test_get_specific_bus_lines_announcments_busline_exists_invalid_busline():
    input = ["3", [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}, {"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage2"}, {"HATKODU": "2", "HAT": "NA", "MESAJ": "TestMessage3"}]]
    result = announcments.get_specific_bus_lines_announcments(input[0], input[1])

    expected_result = []
    
    assert result == expected_result


def test_print_elements_single_element_input(capsys):
    input = [
        {"HATKODU": "93M", "HAT": "ZEYTINBURNU - MECIDIYEKÖY", "TIP": "Günlük", "GUNCELLEME_SAATI": "Kayit Saati: 12:01", "MESAJ": "mock"}
    ]
    announcments.print_elements(input)
    captured = capsys.readouterr()
    assert captured.out == str(
        "\n" +
        "Hat Kodu: 93M\n" +
        "Hat: ZEYTINBURNU - MECIDIYEKÖY\n" +
        "Tip: Günlük\n" + 
        "Güncelleme Saati: Kayit Saati: 12:01\n" +
        "Mesaj: mock\n\n"
    )

def test_print_elements_multiple_element_input(capsys):
    input = [
        {"HATKODU": "93M", "HAT": "ZEYTINBURNU - MECIDIYEKÖY", "TIP": "Günlük", "GUNCELLEME_SAATI": "Kayit Saati: 12:01", "MESAJ": "mock"},
        {'HATKODU': '93T', 'HAT': 'ZEYTINBURNU - TAKSIM', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 12:01', 'MESAJ': ''},
        {'HATKODU': '97GE', 'HAT': '15 TEMMUZ MAHALLESI - EMINÖNÜ', 'TIP': 'Sefer', 'GUNCELLEME_SAATI': 'Kayit Saati: 04:27', 'MESAJ': 'nock'},
    ]
    announcments.print_elements(input)
    captured = capsys.readouterr()
    assert captured.out == str(
        "\n" +
        "Hat Kodu: 93M\n" +
        "Hat: ZEYTINBURNU - MECIDIYEKÖY\n" +
        "Tip: Günlük\n" + 
        "Güncelleme Saati: Kayit Saati: 12:01\n" +
        "Mesaj: mock\n\n" +

        "Hat Kodu: 93T\n" +
        "Hat: ZEYTINBURNU - TAKSIM\n" +
        "Tip: Günlük\n" + 
        "Güncelleme Saati: Kayit Saati: 12:01\n" +
        "Mesaj: \n\n" +

        "Hat Kodu: 97GE\n" +
        "Hat: 15 TEMMUZ MAHALLESI - EMINÖNÜ\n" +
        "Tip: Sefer\n" + 
        "Güncelleme Saati: Kayit Saati: 04:27\n" +
        "Mesaj: nock\n\n"
    )

def test_print_elements_empty_input(capsys):
    input = []
    announcments.print_elements(input)
    captured = capsys.readouterr()
    assert captured.out == str("\n")
