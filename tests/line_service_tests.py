import pytest
import os
import sys
from lxml import etree
sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")
from utils.functions import etree_constructor

import line_service

# https://docs.pytest.org/en/stable/reference/reference.html#std-fixture-capsys

def test_soap_invalid1(capsys):
    with pytest.raises(SystemExit):
        line_service.soap_call("kino_severim")
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "Bus line not found\n"

def test_soap_invalid2(capsys):
    with pytest.raises(SystemExit):
        line_service.soap_call("boyle_bir_hat_yok")
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "Bus line not found\n"

def test_print_elements_singletable(capsys):
    mock_tables = [{"AB": "C", "This_is": "Fake", "Good": "Bye"}]
    line_service.print_elements(mock_tables)
    captured = capsys.readouterr()
    expected_output = str(
        "\nAB: C\n" + "This_is: Fake\n" + "Good: Bye\n" 
    )
    assert captured.out == expected_output

def test_print_elements_multipletable(capsys):
    mock_tables = [{"AB": "C", "This_is": "Fake", "Good": "Bye"}, {"This_is": "Table_Two"}]
    line_service.print_elements(mock_tables)
    captured = capsys.readouterr()
    expected_output = str(
        "\nAB: C\n" + "This_is: Fake\n" + "Good: Bye\n" + "\nThis_is: Table_Two\n" 
    )
    assert captured.out == expected_output

def test_print_elements_emptytable(capsys):
    mock_tables = [{}]
    line_service.print_elements(mock_tables)
    captured = capsys.readouterr()
    expected_output = "\n"
    assert captured.out == expected_output

def test_print_elements_no_table(capsys):
    mock_tables = []
    line_service.print_elements(mock_tables)
    captured = capsys.readouterr()
    expected_output = ""
    assert captured.out == expected_output