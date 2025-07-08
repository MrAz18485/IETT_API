import pytest
import os
import sys
from lxml import etree
sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import line_service

# https://docs.pytest.org/en/stable/reference/reference.html#std-fixture-capsys

def test_soap_invalid1(capsys):
    with pytest.raises(SystemExit):
        line_service.soap_call("kino_severim")
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "Hat bulunamadı / Bus line not found\n"

def test_soap_invalid2(capsys):
    with pytest.raises(SystemExit):
        line_service.soap_call("boyle_bir_hat_yok")
        print("this aint getting printed bro")
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "Hat bulunamadı / Bus line not found\n"

def etree_constructor(tables): # helper for methods below. 
    root_elem = etree.Element("NewDataSet")
    for i in range(len(tables)):
        root_elem.append(etree.Element("Table"))
    curr_table_index = 0
    for table in tables :
        for key, value in table.items():
            element = etree.Element(key)
            element.text = value
            root_elem[curr_table_index].append(element)
        curr_table_index += 1
    return root_elem

def test_print_etree_singletable(capsys):
    mock_tables = [{"AB": "C", "This_is": "Fake", "Good": "Bye"}]
    mock_etree = etree_constructor(mock_tables)
    line_service.print_etree(mock_etree)
    captured = capsys.readouterr()
    expected_output = str(
        "\nAB : C\n" + "This_is : Fake\n" + "Good : Bye\n" 
    )
    assert captured.out == expected_output

def test_print_etree_multipletable(capsys):
    mock_tables = [{"AB": "C", "This_is": "Fake", "Good": "Bye"}, {"This_is": "Table_Two"}]
    mock_etree = etree_constructor(mock_tables)
    line_service.print_etree(mock_etree)
    captured = capsys.readouterr()
    expected_output = str(
        "\nAB : C\n" + "This_is : Fake\n" + "Good : Bye\n" + "\nThis_is : Table_Two\n" 
    )
    assert captured.out == expected_output

def test_print_etree_emptytable(capsys):
    mock_tables = [{}]
    mock_etree = etree_constructor(mock_tables)
    line_service.print_etree(mock_etree)
    captured = capsys.readouterr()
    expected_output = str("\n")
    assert captured.out == expected_output