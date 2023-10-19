def parse_encoded_string(encoded_string):
    parts = encoded_string.split('0')
    first_name = parts[0]
    last_name = parts[1]
    id_number = parts[-1]

    result = {
        "first_name": first_name,
        "last_name": last_name,
        "id": id_number
    }

    return result

encoded_string =input('Enter encoded string:')
parsed_data = parse_encoded_string(encoded_string)
print(parsed_data)
