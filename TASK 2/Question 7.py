import math

x1=int(input('Enter value of X1:'))
y1=int(input('Enter value of Y1:'))
x2=int(input('Enter value of X2:'))
y2=int(input('Enter value of Y2:'))
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

print("The distance between the two points is:", distance)
