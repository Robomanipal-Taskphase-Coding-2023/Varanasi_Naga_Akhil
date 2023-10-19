import itertools
n=int(input('Enter:'))
square=map(pow,range(1,n+1),itertools.repeat(2))
a=[]
for i in range(1,n+1):
    a.append(i)

b=dict(zip(a,square))
print(b)