a = []
for num in range(2000, 3201):
   
    if num % 7 == 0 and num % 5 != 0:
        a.append(str(num))

result_str = ",".join(a)

print(result_str)
