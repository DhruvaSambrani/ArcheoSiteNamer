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
'''
    l=len(str)
    disp=[]
    p=str.upper()
    p1=p[1:]
    if len(combinations(str.split("")))>=number:
        rand_letter=False
    else:
        rand_letter=True
    while len(disp)<number:
        loop_completed=True
        cd=str[0]
        if ord("A")<=ord(cd) and ord(cd)<=ord("Z"):
            for i in range(2):
                q=random.choice(p1)
                cd=cd+q
                p1 = p1[(p1.find(q)+1):]
                if len(p1) < 1:
                    loop_completed=False
                    break
            if cd in disp or not loop_completed:
                continue
            else:
                disp.append(cd)
        if len(disp)==len(combinations(str.split(""))) and rand_letter:
            break
    for i in range(number-len(disp)):
        cd=str[0]
        for i in range(2):
            cd=cd+(chr(random.randint(ord("A"),ord("Z"))
        disp.append(cd)

    return (disp)

'''
