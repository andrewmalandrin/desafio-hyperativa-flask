import re

def validate_email_and_pwd(email: str, pwd: str):
    '''Validate email and password structure'''
    valid_email = False
    valid_pwd = False
    if re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$', email):
        valid_email = True
    # Password must have 8 - 10 chars, 1 upper letter,
    # 1 lower letter, 1 number and 1 special char at least
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$', pwd):
        valid_pwd = True
    if valid_email and valid_pwd:
        return True
    else:
        return False
