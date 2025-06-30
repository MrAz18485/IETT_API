import pytest
import os
import sys
import json
sys.path.append('/home/lolundcmd/Desktop/IETT_API_Tools')

import duyurular

def test_singlechar_hatkodu():
    hat_kodu = duyurular.take_hat_kodu('s')
    assert hat_kodu == 'S'

def test_turkishchar_hatkodu():
    hat_kodu = duyurular.take_hat_kodu('ö')
    assert hat_kodu == 'Ö'

def test_mixed_hatkodu():
    hat_kodu = duyurular.take_hat_kodu('kM18')
    assert hat_kodu == 'KM18'


def test_mixed_hatkodu2():
    hat_kodu = duyurular.take_hat_kodu('öK1')
    assert hat_kodu == 'ÖK1'


def test_soap_call():
    soap_call = duyurular.soap_call()
    assert len(soap_call) != 0 # I mean, its possible that there's no announcments


# ive got no idea how to test this atm
# The announcments change constantly, how can you even compare whether if the file is correctly written or not by comparing two text files?

def test_file_writing_valid():
    mock_array = [
        "{'HATKODU': '93M', 'HAT': 'ZEYTINBURNU - MECIDIYEKÖY', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 12:01', 'MESAJ': 'Z.BURNU PERONLARA GIDISTE ZÜBEYDE HANIN CAD.ÇALISMADAN DOLAYI KAPALI ARAÇLARIMIZ SÜMER DURAGINDAN SONRA GÜZERGAHTAN AYRILARAK BOZKURT DURAGINDAN  GÜZERGAHA GIRERLER.'}",
        "{'HATKODU': '93T', 'HAT': 'ZEYTINBURNU - TAKSIM', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 12:01', 'MESAJ': 'Z.BURNU PERONLARA GIDISTE ZÜBEYDE HANIN CAD.ÇALISMADAN DOLAYI KAPALI ARAÇLARIMIZ SÜMER DURAGINDAN SONRA GÜZERGAHTAN AYRILARAK BOZKURT DURAGINDAN  GÜZERGAHA GIRERLER.'}",
        "{'HATKODU': '97GE', 'HAT': '15 TEMMUZ MAHALLESI - EMINÖNÜ', 'TIP': 'Sefer', 'GUNCELLEME_SAATI': 'Kayit Saati: 04:27', 'MESAJ': 'EMINÖNÜ dan Saat 22:10 de hareket etmesi planlanan seferimiz  çesitli nedenlerle yapilamayacaktir.'}",
        "{'HATKODU': '98', 'HAT': 'FENERTEPE/BASAKSEHIR - BAKIRKÖY', 'TIP': 'Sefer', 'GUNCELLEME_SAATI': 'Kayit Saati: 04:27', 'MESAJ': 'BAKIRKÖY dan Saat 22:30 de hareket etmesi planlanan seferimiz  çesitli nedenlerle yapilamayacaktir.'}",
        "{'HATKODU': '98H', 'HAT': 'METROKENT - BAKIRKÖY', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 20:28', 'MESAJ': 'GÜZERGAHTAKI YOGUN TRAFIK NEDENIYLE ARAÇLARIMIZ HER IKI YÖNDE SEFERLERINE 20 DAKIKA VE ÜZERI RÖTARLI HAREKET ETMEKTEDIR.'}",
        "{'HATKODU': '98TB', 'HAT': 'FATIH MAHALLESI - BAKIRKÖY', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 11:50', 'MESAJ': 'FATIH MAHALLESI DURAGINDAKI ÇALISMA NEDENIYLE ARAÇLARIMIZ PAZARYOLU DURAGINDA SEFERLERINI BITIRIP AYNI DURAKTAN SERVISE BASLAR.'}",
        "{'HATKODU': '98TB', 'HAT': 'FATIH MAHALLESI - BAKIRKÖY', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 11:51', 'MESAJ': 'FATIH MAHALLESI DURAGINDAKI ÇALISMA NEDENIYLE ARAÇLARIMIZ PAZARYOLU DURAGINDA SEFERLERINI BITIRIP AYNI DURAKTAN SERVISE BASLAR.'}",
        "{'HATKODU': '98Y', 'HAT': 'GIYIMKENT / YÜZYIL MAHALLESI - BAKIRKÖY', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 07:39', 'MESAJ': 'PARKLANMA NEDENIYLE 42 EVLER KAPALIDIR.ARAÇLARIMIZ SEHIT TÜRKMEN TEKIN DURAGINDAN GÜZERGAH DISINA ÇIKARAK YÜZ YIL DURAGINDAN GÜZERGAHA GIRECEKTIR.(GIDIS-DÖNÜS BU GÜZERGAH KULLANILACAKTIR)'}",
        "{'HATKODU': 'BA-2', 'HAT': 'ÇARSI-LUNAPARK', 'TIP': 'Sefer', 'GUNCELLEME_SAATI': 'Kayit Saati: 04:27', 'MESAJ': 'LUNAPARK dan Saat 22:07 de hareket etmesi planlanan seferimiz  çesitli nedenlerle yapilamayacaktir.'}",
    ]

    duyurular.write_to_tempfile(mock_array, 'test_filewriting_valid_output.txt')

    result_buffer = []
    with open('/home/lolundcmd/Desktop/IETT_API_Tools/tests/duyurular_tests/test_filewriting_valid_output.txt', 'r') as file1:
        for line in file1:
            result_buffer.append(line.strip('\n'))
    
    assert mock_array == result_buffer

def test_file_writing_empty():
    mock_array = []

    duyurular.write_to_tempfile([], 'test_filewriting_empty_output.txt')

    result_buffer = []
    with open('/home/lolundcmd/Desktop/IETT_API_Tools/tests/duyurular_tests/test_filewriting_empty_output.txt', 'r') as file1:
        for line in file1:
            result_buffer.append(line.strip('\n'))
    
    assert mock_array == result_buffer


# too time consuming honestly, not even worth to automate at this point..
def test_reading_valid_hat():
    expected_result = [
        "{'HATKODU': '98TB', 'HAT': 'FATIH MAHALLESI - BAKIRKÖY', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 11:50', 'MESAJ': 'FATIH MAHALLESI DURAGINDAKI ÇALISMA NEDENIYLE ARAÇLARIMIZ PAZARYOLU DURAGINDA SEFERLERINI BITIRIP AYNI DURAKTAN SERVISE BASLAR.'}",
        "{'HATKODU': '98TB', 'HAT': 'FATIH MAHALLESI - BAKIRKÖY', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 11:51', 'MESAJ': 'FATIH MAHALLESI DURAGINDAKI ÇALISMA NEDENIYLE ARAÇLARIMIZ PAZARYOLU DURAGINDA SEFERLERINI BITIRIP AYNI DURAKTAN SERVISE BASLAR.'}"
    ]

    result = duyurular.read_from_tempfile('98TB', 'test_filewriting_valid_output.txt')

    assert expected_result == result


def test_reading_invalid_hat():
    expected_result = []

    result = duyurular.read_from_tempfile('abc', 'test_filewriting_valid_output.txt')

    assert expected_result == result

def test_reading_emptyfile():
    expected_result = []

    results = duyurular.read_from_tempfile('98TB','test_filewriting_empty_output.txt')

    assert expected_result == results

def test_conversion_to_dict_valid(): # basically check if string is converted to dictionary
    expected_result = [{"HATKODU": "93M", "HAT": "ZEYTINBURNU - MECIDIYEKÖY", 
                       "TIP": "Günlük", "GUNCELLEME_SAATI": "Kayit Saati: 12:01", 
                       "MESAJ": "Z.BURNU PERONLARA GIDISTE ZÜBEYDE HANIN CAD.ÇALISMADAN DOLAYI KAPALI ARAÇLARIMIZ SÜMER DURAGINDAN SONRA GÜZERGAHTAN AYRILARAK BOZKURT DURAGINDAN  GÜZERGAHA GIRERLER."}]
    result = duyurular.string_to_dict(
        ["{'HATKODU': '93M', 'HAT': 'ZEYTINBURNU - MECIDIYEKÖY', 'TIP': 'Günlük', 'GUNCELLEME_SAATI': 'Kayit Saati: 12:01', 'MESAJ': 'Z.BURNU PERONLARA GIDISTE ZÜBEYDE HANIN CAD.ÇALISMADAN DOLAYI KAPALI ARAÇLARIMIZ SÜMER DURAGINDAN SONRA GÜZERGAHTAN AYRILARAK BOZKURT DURAGINDAN  GÜZERGAHA GIRERLER.'}"]
    )
    assert expected_result == result


def test_conversion_to_dict_valid2(): # basically check if string is converted to dictionary
    expected_result = [{"ab": "c", "de": "f", "1":"23"}]
    result = duyurular.string_to_dict(
        ["{'ab': 'c', 'de': 'f', '1': '23'}"]
    )
    assert expected_result == result