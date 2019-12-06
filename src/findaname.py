import random
str=input("Enter name of site: ")
l=len(str)
disp,p=[],[]
for i in range(l):
    p.append((ord(str[i].upper())))
while len(disp)<5:
    n=0
    p1=p.copy()
    cd=""
    for i in range(3):
        q=random.choice(p1)
        cd=cd+(chr(q))
        del p1[:(p1.index(q)+1)]
        if len(p1)<1:
            n=1 
            break
    if cd in disp or n==1:
        continue
    else:
        disp.append(cd)
 print("Suggested codes: ")
 print(disp)
    
    
