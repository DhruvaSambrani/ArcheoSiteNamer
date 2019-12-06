import random
def findabbrs(str, number=20):
    l=len(str)
    disp=[]
    p=str.upper()
    while len(disp)<number:
        loop_completed=True
        p1=p[1:]
        cd=str[0]
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
    return (disp)
