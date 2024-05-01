import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')


def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))


def isDot(string: str):
    return string == '.'


def isInverseSignal(string: str):
    return string == '+/-'


def isEmpty(string: str):
    if string == 'None' or string is None or len(string) == 0:
        return True
    else:
        return False


def convertToNumber(string: str):
    number = float(string)

    if number.is_integer():
        number = int(number)
    return number


def isValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except (ValueError, TypeError):
        valid = False
    return valid


def isZero(string: str):
    valid = False
    try:
        if abs(float(string)) == 0:
            valid = True
    except ValueError:
        valid = False
    return valid
