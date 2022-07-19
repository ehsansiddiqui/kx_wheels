import re

def is_valid_cc(s):
    #http://atlee.ca/blog/2008/05/27/validating-credit-card-numbers-in-python/
    s = re.sub("[^0-9]", "", str(s))
    regexps = [
            "^4\d{15}$",
            "^5[1-5]\d{14}$",
            "^3[4,7]\d{13}$",
            "^3[0,6,8]\d{12}$",
            "^6011\d{12}$",
            ]

    if not any(re.match(r, s) for r in regexps):
        return False

    chksum = 0
    x = len(s) % 2

    for i, c in enumerate(s):
        j = int(c)
        if i % 2 == x:
            k = j*2
            if k >= 10:
                k -= 9
            chksum += k
        else:
            chksum += j

    return chksum % 10 == 0
