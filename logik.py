# Функция генерации случайного пароля
def random_key(length=10):
    from string import ascii_lowercase, ascii_uppercase, digits, punctuation
    from random import choice, shuffle, randint
    key = []                 # Массив для формирования ключа
    key.append(choice(ascii_lowercase))
    key.append(choice(ascii_uppercase))
    key.append(choice(digits))
    key.append(choice(punctuation))
    while len(key) <= length:
        value = randint(1, 4)
        if value == 1:
            key.append(choice(ascii_lowercase))
        elif value == 2:
            key.append(choice(ascii_uppercase))
        elif value == 3:
            key.append(choice(digits))
        elif value == 4:
            key.append(choice(punctuation))
    shuffle(key)
    out = ''.join(key)
    return out

# Функция простого шифрования и дешифровки
def simple_code(s_input, key):
    from itertools import cycle
    out = ''
    shift = 50  # Смещение, чтобы не попасто в непечатные символы (это первые 30) должно быть одинаковым и у функции simple_decode !!!!
    for x, y in zip(s_input, cycle(key)):
        out += chr((ord(x) ^ ord(y)) + shift)
    return out

# Функция простого дешифрования
def simple_decode(s_input, key):
    from itertools import cycle
    out = ''
    shift = 50
    for x, y in zip(s_input, cycle(key)):
        out += chr((ord(x) - shift) ^ ord(y))
    return out

