import random
from itertools import combinations 
def findabbrs(str, number=20):
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
