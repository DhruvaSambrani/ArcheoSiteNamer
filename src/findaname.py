import random
from itertools import combinations
def findabbrs(str, max_number=20):
    cleanStr = []
    disp = []

    # Remove non alpha numeric
    for i in str[1:]:
        if i.isalnum():
            cleanStr.append(i.upper())

    # Make a unique list of atmost max_number combinations of 2 chars
    for i in list(set(combinations(cleanStr, 2)))[:max_number]:
        t = list(i)
        # Add first character
        t.insert(0,str[0].upper())
        disp.append("".join(t))
    return disp
