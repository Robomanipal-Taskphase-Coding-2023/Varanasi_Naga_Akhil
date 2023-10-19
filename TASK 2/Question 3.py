n=int(input('Enter number of entries:'))
a=[]
for i in range(n):
    b=int(input('Enter Number:'))
    a.append(b)


print(a)
a.sort(reverse=True)
print(a[1])
