import ogkush


def random_bytes(seed, n_bytes):
    out = ""
    # Constantes de control
    ps = (0,1) # cuatro valores distintos entre 0 y 31 si es par usa uno si es impar el otro
    ps2 = (31,30)


    ns = n_bytes*2
    sup = True
    i=ogkush.ogkush(seed)
    while 1:
        if sup: # variantes logicas (variación de seleción extraida de hash)
            pos = (int(i[ps[0]],16)+1 + int(i[ps[1]],16)+1 ) -1
        else:
            pos = (int(i[ps2[0]],16)+1 + int(i[ps2[1]],16)+1 ) -1
        nible = int(i[pos],16)
        bin_nible = str(('0000' + format(nible, 'b'))[-4:])
        
        if not sup: # variantes logicas (reordenación a nivel de bit de seleción)
            out += bin_nible
        else:
            out += bin_nible[2:3]+bin_nible[0:1]

        ns -=1
        if ns == 0:
            break       
        i=ogkush.ogkush(i)
        sup=not sup
    return ogkush.bin_to_hex(out)


def random_bytes_iterator(seed):
    # Constantes de control
    l = 10
    i, j = 0,2


    while 1:
        i=(i+1)%l
        j=(j+1)%l
        seed = random_bytes(seed, l)
        yield (seed[i]+seed[j])


if __name__ == "__main__":
    seed="23"
    for b in random_bytes_iterator("23"):
        print(b)


"""
 o==[]::::::::::::::::>         [̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅]    [̲̅$̲̅(̲̅5̲̅)̲̅$̲̅]
"""
