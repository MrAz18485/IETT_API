import pytest
import sys
from lxml import etree

sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

from utils.functions import special_char_upper_func, replace_keyword, convert_etree_tags_to_english, convert_dict_keys_to_english, etree_constructor

def test_special_char_upper_func_input_singlechar():
    line_code = special_char_upper_func('s')
    assert line_code == 'S'

def test_special_char_upper_func_input_turkishchar():
    line_code = special_char_upper_func('ö')
    assert line_code == 'Ö'

def test_special_char_upper_func_input_mix_lower_upper_noturkishchar():
    line_code = special_char_upper_func('kM18')
    assert line_code == 'KM18'

def test_special_char_upper_func_input_mix_lower_upper_turkishchar():
    line_code = special_char_upper_func('öK1')
    assert line_code == 'ÖK1'

def test_special_char_upper_func_input_empty():
    response = special_char_upper_func("")
    expected_response = ""
    assert response == expected_response

def test_special_char_upper_func_input_special_char():
    response = special_char_upper_func("!.'1")
    expected_response = "!.'1"
    assert response == expected_response

def test_replace_keyword_key_exists_in_dictionary():
    inputs = ("ABC", {"ABC": "DEF", "FGH":"1"})
    response = replace_keyword(inputs[0], inputs[1])
    expected_response = "DEF"
    assert response == expected_response

def test_replace_keyword_multiple_key_exists_in_dictionary():
    inputs = ("ABC", {"ABC": "DEF", "ABC":"1"})
    response = replace_keyword(inputs[0], inputs[1])
    expected_response = "1"
    assert response == expected_response

def test_replace_keyword_key_not_in_dictionary():
    with pytest.raises(KeyError) as key_err:
        inputs = ("", {"ABC": "DEF", "ABC":"1"})
        response = replace_keyword(inputs[0], inputs[1])
    expected_exception_message = "Matching key not found! This shouldn't have happened, there could be an issue with SOAP response, or dictionary passed as parameter."
    assert key_err.match(expected_exception_message) # regex match


def test_convert_etree_tags_to_english_single_element():
    mock_tables = [{"HAT_KODU": "KM18", "HAT_ADI": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO", 
                    "TAM_HAT_ADI": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO", "HAT_DURUMU": "1", "BOLGE": "Anadolu2",
                    "SEFER_SURESI": "71.04"}]
    keys_dictionary = {"HAT_KODU": "LINE_CODE", "HAT_ADI": "LINE_NAME", "TAM_HAT_ADI": "FULL_LINE_NAME", "HAT_DURUMU": "LINE_STATUS", "BOLGE": "ZONE", "SEFER_SURESI": "TRAVEL_TIME"}
    mock_etree = etree_constructor(mock_tables)
    result = convert_etree_tags_to_english(mock_etree, keys_dictionary)
    expected_result = [{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO",
                    "FULL_LINE_NAME": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO", "LINE_STATUS": "1", "ZONE": "Anadolu2",
                    "TRAVEL_TIME": "71.04"}]
    assert result == expected_result

def test_convert_etree_tags_to_english_multiple_element():
    mock_tables = [{"HAT_KODU": "KM18", "HAT_ADI": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO", 
                    "TAM_HAT_ADI": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO", "HAT_DURUMU": "1", "BOLGE": "Anadolu2",
                    "SEFER_SURESI": "71.04"}, {"HAT_KODU": "16D", "HAT_ADI": "ALTKAYNARCA / PENDİK - KADIKÖY", 
                    "TAM_HAT_ADI": "16D/ALTKAYNARCA / PENDİK - KADIKÖY", "HAT_DURUMU": "1", "BOLGE": "Anadolu2",
                    "SEFER_SURESI": "142.25"}]
    keys_dictionary = {"HAT_KODU": "LINE_CODE", "HAT_ADI": "LINE_NAME", "TAM_HAT_ADI": "FULL_LINE_NAME", "HAT_DURUMU": "LINE_STATUS", "BOLGE": "ZONE", "SEFER_SURESI": "TRAVEL_TIME"}
    mock_etree = etree_constructor(mock_tables)
    result = convert_etree_tags_to_english(mock_etree, keys_dictionary)
    expected_result = [{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO",
                    "FULL_LINE_NAME": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO", "LINE_STATUS": "1", "ZONE": "Anadolu2",
                    "TRAVEL_TIME": "71.04"}, {"LINE_CODE": "16D", "LINE_NAME": "ALTKAYNARCA / PENDİK - KADIKÖY", 
                    "FULL_LINE_NAME": "16D/ALTKAYNARCA / PENDİK - KADIKÖY", "LINE_STATUS": "1", "ZONE": "Anadolu2",
                    "TRAVEL_TIME": "142.25"}]
    assert result == expected_result

def test_convert_etree_tags_to_english_no_element():
    mock_tables = []
    keys_dictionary = {"HAT_KODU": "LINE_CODE", "HAT_ADI": "LINE_NAME", "TAM_HAT_ADI": "FULL_LINE_NAME", "HAT_DURUMU": "LINE_STATUS", "BOLGE": "ZONE", "SEFER_SURESI": "TRAVEL_TIME"}
    mock_etree = etree_constructor(mock_tables)
    result = convert_etree_tags_to_english(mock_etree, keys_dictionary)
    expected_result = []
    assert result == expected_result


def test_convert_dict_keys_to_english_single_element_input():
    input = [
        {"SHATKODU":"KM18","HATADI":"SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL","SGUZERAH":"KM18_G_D0","SYON":"G","SGUNTIPI":"I","GUZERGAH_ISARETI":"None","SSERVISTIPI":"Normal","DT":"09:00"}
    ]
    keys_dictionary = {"SHATKODU": "LINE_CODE", "HATADI": "LINE_NAME", "SGUZERAH": "ROUTE", "SYON": "DIRECTION", "SGUNTIPI": "DAY_TYPE", 
                                     "GUZERGAH_ISARETI": "ROUTE_SIGN", "SSERVISTIPI": "SERVICE_TYPE", "DT": "TIME_INFO"}
    output = convert_dict_keys_to_english(input, keys_dictionary)

    expected_output = [
        {"LINE_CODE":"KM18","LINE_NAME":"SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL","ROUTE":"KM18_G_D0","DIRECTION":"G","DAY_TYPE":"I","ROUTE_SIGN":"None","SERVICE_TYPE":"Normal","TIME_INFO":"09:00"}
    ]

    assert output == expected_output

def test_change_tags_to_english_multiple_element_input():
    input = [
        {"SHATKODU":"KM18","HATADI":"SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL","SGUZERAH":"KM18_G_D0","SYON":"G","SGUNTIPI":"I","GUZERGAH_ISARETI":"None","SSERVISTIPI":"Normal","DT":"09:00"},
        {"SHATKODU":"KM18","HATADI":"PENDİK/PENDİK YHT-SABİHA GÖKÇEN HAVALİMANI","SGUZERAH":"KM18_G_D4155","SYON":"G","SGUNTIPI":"I","GUZERGAH_ISARETI":"None","SSERVISTIPI":"Ara Dinlen","DT":"09:30"},
        {"SHATKODU":"KM18","HATADI":"SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL","SGUZERAH":"KM18_G_D0","SYON":"G","SGUNTIPI":"I","GUZERGAH_ISARETI":"None","SSERVISTIPI":"Normal","DT":"10:30"},
    ]
    keys_dictionary = {"SHATKODU": "LINE_CODE", "HATADI": "LINE_NAME", "SGUZERAH": "ROUTE", "SYON": "DIRECTION", "SGUNTIPI": "DAY_TYPE", 
                                     "GUZERGAH_ISARETI": "ROUTE_SIGN", "SSERVISTIPI": "SERVICE_TYPE", "DT": "TIME_INFO"}
    output = convert_dict_keys_to_english(input, keys_dictionary)

    expected_output = [
        {"LINE_CODE":"KM18","LINE_NAME":"SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL","ROUTE":"KM18_G_D0","DIRECTION":"G","DAY_TYPE":"I","ROUTE_SIGN":"None","SERVICE_TYPE":"Normal","TIME_INFO":"09:00"},
        {"LINE_CODE":"KM18","LINE_NAME":"PENDİK/PENDİK YHT-SABİHA GÖKÇEN HAVALİMANI","ROUTE":"KM18_G_D4155","DIRECTION":"G","DAY_TYPE":"I","ROUTE_SIGN":"None","SERVICE_TYPE":"Ara Dinlen","TIME_INFO":"09:30"},
        {"LINE_CODE":"KM18","LINE_NAME":"SABANCI ÜNİ./MEDENİYET ÜNİ. - PENDİK METRO/KARTAL","ROUTE":"KM18_G_D0","DIRECTION":"G","DAY_TYPE":"I","ROUTE_SIGN":"None","SERVICE_TYPE":"Normal","TIME_INFO":"10:30"},
    ]
    
    assert output == expected_output

def test_change_tags_to_english_no_element_input():
    input = []
    keys_dictionary = {"SHATKODU": "LINE_CODE", "HATADI": "LINE_NAME", "SGUZERAH": "ROUTE", "SYON": "DIRECTION", "SGUNTIPI": "DAY_TYPE", 
                                     "GUZERGAH_ISARETI": "ROUTE_SIGN", "SSERVISTIPI": "SERVICE_TYPE", "DT": "TIME_INFO"}
    output = convert_dict_keys_to_english(input, keys_dictionary)

    expected_output = []
    
    assert output == expected_output

def test_change_tags_to_english_invalid_element_input():
    with pytest.raises(KeyError) as key_exc:
        input = [{"abc":"def"}]
        keys_dictionary = {"SHATKODU": "LINE_CODE", "HATADI": "LINE_NAME", "SGUZERAH": "ROUTE", "SYON": "DIRECTION", "SGUNTIPI": "DAY_TYPE", 
                           "GUZERGAH_ISARETI": "ROUTE_SIGN", "SSERVISTIPI": "SERVICE_TYPE", "DT": "TIME_INFO"}
        output = convert_dict_keys_to_english(input, keys_dictionary)
    expected_exception_message = "Matching key not found! This shouldn't have happened, there could be an issue with SOAP response, or dictionary passed as parameter."
    assert key_exc.match(expected_exception_message)

class etree_element_with_text(etree.ElementBase): # extending etree._Element class
    # we defined a __init__ method here, now the __init__ method of parent class
    # will not be invoked. So we should call __init__ of parent class here explicitly.
    etree.Element()
    # It turns out we shouldn't override __init__ method (suggested by docs of lxml)
    def _init(self, text=None):
        if text:
            self.text = text
     
def test_etree_constructor_single_table():
    input = [{"LINE_CODE": "KM18", "LINE_NAME": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO", 
            "FULL_LINE_NAME": "SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO", "LINE_STATUS": "1", "REGION": "Anadolu2",
            "TRAVEL_TIME": "71.04"}]
    output = etree_constructor(input)

    expected_output = etree.Element("NewDataSet")
    expected_output.append(etree.Element("Table"))
    expected_output[0].append(etree_element_with_text(tag="LINE_CODE", text="KM18"))
    expected_output[0].append(etree_element_with_text(tag="LINE_NAME", text="SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO"))
    expected_output[0].append(etree_element_with_text(tag="FULL_LINE_NAME", text="SABANCI ÜNİ./MEDENİYET ÜNİ. - KURTKÖY METRO"))
    expected_output[0].append(etree_element_with_text(tag="LINE_STATUS", text="1"))
    expected_output[0].append(etree_element_with_text(tag="REGION", text="Anadolu2"))
    expected_output[0].append(etree_element_with_text(tag="TRAVEL_TIME", text="71.04"))
    assert etree.tostring(output) == etree.tostring(expected_output)