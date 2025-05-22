def shift(_input, shift_amnt, _output):
    _output = _output + chr(int(_input) + int(shift_amnt)).encode(encoding="utf-8")

def encryption(_input, shift_amnt):
    shifted = ''

    for line in _input:
        for char in line:
            shift(char, shift_amnt, shifted)
    
    return shifted
 
def caesar_encrypt(_in, shifts):
    out = encryption(_in, shifts)

    return out
