
if __name__ == '__main__':
    shift_value = 2
    mask = 3
    not_mask = ~mask
    tile = [118,118,119,119]

    sign = 46
    for z in range (0, 4):
        print(format(tile[z], '08b'), end=" ")

    print("\n"+format(sign, '08b'))
    print("Tile New-Mask Bits-ex-1 Bits-ex-2 New-tile-1 New-tile-2")
    for i in range(0,4):
        print(format(tile[i], '08b'), end=" ")

        new_mask = mask << (shift_value * i)
        print(format(new_mask, '08b'), end=" ")

        bits_extract = sign & new_mask
        print(format(bits_extract, '08b'), end=" ")

        bits_extract = bits_extract >> (shift_value*i)
        print(format(bits_extract, '08b'), end=" ")

        tile[i] &= not_mask
        print(format(tile[i], '08b'), end=" ")

        tile[i] |= bits_extract
        print(format(tile[i], '08b'))


    print ("final singnature--")

    for j in range(0,4):
        print ( format(tile[j],'08b'), end=" ")
