def B10aB2(num : int):
    if num== 0:
        return 0
    elif num == 1:
        return 1
    elif num < 2:
        return str(num) + str(resto)
    resto = num % 2
    convertido = B10aB2(num // 2)
    return str(convertido) + str(resto)

def B2aB10(num : int):
    pass