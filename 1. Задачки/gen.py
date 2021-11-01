from random import randint, choice
f=open("gen3.txt","w")
for i in range(100):
    sign=choice([True, False])
    a=randint(10,50)
    b=randint(1,9)
    if sign:
        c=a+b
    else:
        c=randint(1,50)
    f.write(str(a)+"+"+str(b)+"="+str(c)+"\t"+str(int(sign))+"\n")
f.close()

