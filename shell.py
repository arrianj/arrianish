import arrianish

while True:
    text = input('arrianish > ')
    # parses trimmed input to prevent an incorrect invalid syntax exception in the event of empty inputs
    if text.strip() == "": continue
    result, error = arrianish.run('<stdin>', text)

    if error: print(error.as_string())
    elif result:
        # prevents result being shown in a list if it is the only element in the result
        if len(result.elements) == 1:
            print (repr(result.elements[0]))
        else:
            print(repr(result))