import re
from flask import flash


# User's fullname validation
def name_correct(data: str) -> bool:
    if 3 <= len(data) <= 32:
        return True
    else:
        #flash("Wrong fullname format", category='error')
        return False


# Email validation
def email_correct(email: str) -> bool:
    """
    Validation email with regEx
    :param email:
    :return:
    """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email):
        return True
    else:
        #flash("Wrong email format", category='error')
        return False


# Password validation with regEx
def password_correct(data: str) -> bool:
    """
    Conditions for a valid password are:
        Should have at least one number.
        Should have at least one uppercase and one lowercase character.
        Should have at least one special symbol.
        Should be between 6 to 20 characters long.
    :param data:
    :return:
    """
    # regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    # pat = re.compile(regex)
    #
    # if re.search(pat, data):
    #     return True
    # else:
    #     flash("Wrong password format", category='error')
    #     return False

    if 6 < len(data) < 25:
        return True
    else:
        return False


def password_equal(str1, str2) -> bool:
    if str1 == str2:
        return True
    else:
        #flash("Passwords not equal", category='error')
        return False


def input_form_correct(data) -> bool:
    res = name_correct(data['name'])
    res &= password_correct(data['password'])
    res &= email_correct(data['email'])
    res &= password_equal(data['password'], data['password2'])

    return res
