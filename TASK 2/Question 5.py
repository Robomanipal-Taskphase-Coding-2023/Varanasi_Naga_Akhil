def decimal_to_binary(decimal_num):
    if decimal_num <= 0:
        return "0"
    elif decimal_num == 1:
        return "1"
    else:
        
        return decimal_to_binary(decimal_num // 2) + str(decimal_num % 2)

decimal_num = int(input("Enter a decimal number: "))

binary_num = decimal_to_binary(decimal_num)
print("Binary representation:", binary_num)
