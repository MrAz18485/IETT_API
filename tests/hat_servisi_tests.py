import pytest
import os
import sys
sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import hat_servisi


# https://docs.pytest.org/en/stable/reference/reference.html#std-fixture-capsys

def test_soap_invalid1(capsys):
    hat_servisi.soap_call("Ö")

    captured = capsys.readouterr()
    print(captured)
    assert captured.out == "Hat bulunamadı / Bus line not found\n"

def test_soap_invalid2(capsys):
    hat_servisi.soap_call("Ö")

    captured = capsys.readouterr() # for capturing stdout
    print(captured)
    assert captured.out == "Hat bulunamadı / Bus line not found\n"

def test_soap_valid1():
    expected_result = {}
    result = hat_servisi.soap_call("UM73")
    for table in result:
        for element in table:
            expected_result[element.tag] = element.text

    assert expected_result == {"HAT_KODU" : "UM73", "HAT_ADI" : "SABİHA GÖKÇEN H.L./ SULTANBEYLİ - SAMANDIRA MERKEZ METRO",
                                                                               "TAM_HAT_ADI" : "UM73/SABİHA GÖKÇEN H.L./ SULTANBEYLİ - SAMANDIRA MERKEZ METRO", "HAT_DURUMU" : "1",
                                                                               "BOLGE" : "Anadolu2", "SEFER_SURESI" : "76.46"}

def test_soap_valid2():
    expected_result = {}
    result = hat_servisi.soap_call("KM18")
    for table in result:
        for element in table:
            expected_result[element.tag] = element.text
    assert expected_result == {"HAT_KODU" : "KM18", "HAT_ADI" : "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO",
                                                                               "TAM_HAT_ADI" : "KM18/SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO", "HAT_DURUMU" : "1",
                                                                               "BOLGE" : "Anadolu2", "SEFER_SURESI" : "71.04"}