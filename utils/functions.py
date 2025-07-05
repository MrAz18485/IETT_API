# to convert some of the turkish lowercase characters to their corresponding upper case pairs
def special_char_upper_func(param):
    special_chars = {"ğ":"Ğ", "ü":"Ü", "i":"İ", "ş":"Ş", "ö":"Ö", "ç":"Ç"}
    for key, value in special_chars.items():
        param = param.replace(key, value)
    return param.upper()

# converts given input to ms
# Example: /DateTime(number)/, extracts number
def ms_parser(line):
    startidx = -1
    endidx = -1

    for i in range(len(line)):
        if (line[i] == '('):
            startidx = i
        elif (line[i] == ')'):
            endidx = i
    date_to_ms = int(line[startidx+1:endidx])
    return date_to_ms