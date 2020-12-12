import arrianish

while True:
    text = input('arrianish > ')
    result, error = arrianish.run('<stdin>', text)

    if error: print(error.as_string())
    elif result: print(result)