import pytest
import sys

sys.path.append("/home/lolundcmd/Desktop/IETT_API_Tools")

import utils.functions

def test_input_singlechar():
    line_code = utils.functions.special_char_upper_func('s')
    assert line_code == 'S'

def test_input_turkishchar():
    line_code = utils.functions.special_char_upper_func('ö')
    assert line_code == 'Ö'

def test_input_mix_lower_upper_noturkishchar():
    line_code = utils.functions.special_char_upper_func('kM18')
    assert line_code == 'KM18'

def test_input_mix_lower_upper_turkishchar():
    line_code = utils.functions.special_char_upper_func('öK1')
    assert line_code == 'ÖK1'

def test_input_empty():
    response = utils.functions.special_char_upper_func("")
    expected_response = ""
    assert response == expected_response

def test_input_special_char():
    response = utils.functions.special_char_upper_func("!.'1")
    expected_response = "!.'1"
    assert response == expected_response