def compress_string(s):
    compressed = []
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            if count > 1:
                compressed.append(f'({count}, {s[i - 1]})')
            else:
                compressed.append(s[i - 1])
            count = 1

    if count > 1:
        compressed.append(f'({count}, {s[-1]})')
    else:
        compressed.append(s[-1])

    return ''.join(map(str, compressed))

s =input('Enter String:')
compressed_s = compress_string(s)
print(compressed_s)
