#!/usr/bin/env python
# -*- coding: utf-8 -*-

nbit_out= 128

def str_to_bin(st):
    return ''.join(('00000000' + format(ord(x), 'b'))[-8:] for x in st)

def bin_to_str(st):
    out=""
    for i in range(int(len(st)/8)):
        out+=chr(int("0b"+st[8 * i: (8 * i) + 8], 2 ))
    return out

def bin_to_hex(st):
    out=""
    for i in range(int(len(st)/4)):
        out+=(str(hex(int("0b"+st[4 * i: (4 * i) + 4], 2 )))[2:])
    return out


import binascii

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def d0(h):
	def round(inp):
		b = inp
		out=""
		j = 1
		for i in range(len(b)):
		    if j == len(b):
		        break
		    out+=str( int(b[i]) ^ int(b[j]) )

		    j+=1

		out1=""
		j = len(out)-2
		k = len(out)-1
		for i in range(len(out)):
		    if k == 0:
		        break
		    out1=str( int(out[j]) ^ int(out[k]) )+out1
		    j-=1
		    k-=1


		return out1

	def mix(inp):
		b = inp
		out=""
		j = 1
		out+=str( int(b[len(b)-1]) ^ int(b[0]) ) # extra bit

		for i in range(len(b)):
		    out+=str( int(b[i]) ^ int(b[j]) )
		    j+=1
		    if j == len(b):
		        break

		out1= str( int(out[len(out)-1]) ^ int(out[0]) ) # extra bit

		j = len(out)-2
		k = len(out)-1
		for i in range(len(out)):
		    out1=str( int(out[j]) ^ int(out[k]) )+out1
		    if j == 0:
		        break
		    j-=1
		    k-=1

		return out1

	def expand(inp,c):
		b = inp
		out=""
		j = 1
		out+=str( int(c) ^ int(b[0]) ) # extra bit

		for i in range(len(b)):
		    out+=str( int(b[i]) ^ int(b[j]) )
		    j+=1
		    if j == len(b):
		        break

		c2 = str(int(c) ^ int(b[len(b) - 1]) ^ int(b[0]))  # acarreo intermedio bit

		out1= str( int(c2) ^ int(out[0]) ) # extra bit

		j = len(out)-2
		k = len(out)-1
		for i in range(len(out)):
		    out1=str( int(out[j]) ^ int(out[k]) )+out1
		    if j == 0:
		        break
		    j-=1
		    k-=1
		out1 += str(int(out[len(out) - 1]) ^ int(out[0])) # extra bit

		c3 = str( int(c2) ^ int(out[len(out)-1]) ^ int(out[0]) ) # acarreo de salida bit

		return out1, c3

	def hash_block(s, n):
		h=s
		for i in range(n):
		    h=round(h)
		return h

	def hash_4_bytes(input):
		b1 = hash_block(input,12)
		b2 = hash_block(input[8:16],3)+hash_block(input[16:24],3)+hash_block(input[24:32],3)+hash_block(input[0:8],3)
		out = ""
		for i in range(len(b1)):
		    out+=str( int(b1[i]) ^ int(b2[i]) )
		return out

# contar el numero de operaciones para evitar colisiones por expansion en la fase de absorcion, usar el numero de operaciones en la fase de estrujado


	def absorver(inp, ops=0):        
		# si es menor que el numero de bloques expandir hasta nbits*4
		c=int(inp[0])
		while len(inp)<nbit_out*4:
		    inp, c = expand(inp,c)
		    ops+=1

		# si es mayor expandimos hasta llegar a un multiplo de 32 bits
		while len(inp) % 32 != 0:
		    inp, c = expand(inp, c)
		    ops+=1

		#print(len(inp))

		# calcula el estado
		while len(inp) > nbit_out:
			nblocks = int(len(inp)/32)
			out = ""
			for i in range(nblocks):
				block = inp[32 * i:(32 * i) + 32]
				pro_block = hash_4_bytes (block)
				out+=pro_block
				ops+=1
			inp = out            

		#print(len(out))
		return out, ops


	def extrujar(state2):
		state, ops = state2
		def op_displacement(b, op): # prueba de combinación de numero de operaciones con jugo de estado interno
            # posibilidad de aplicar solo a medio byte %128
			x = (8*"0"+ (str(bin(op%256))[2:]) )[-8:]
			o = ""

			for i in range(8):
				o+= str( int(b[i]) ^ int(x[i]) ) # posibles variaciones de operacion
			#print(b, x, o)
			return o

		out = ""
		while len(out) < nbit_out:
		    # reducir estado a mitad y sacar primeros 8bits
#		    its = int ( len(state) - (len(state)/2) )
		    #print(its)
		    out += op_displacement( str(hash_block(state, 1))[:8], ops)
		    # mezclar estado
		    state = mix(state)
		    ops +=1

		return out


	return extrujar(absorver(h))

#a="11111011001001000101010110010011"


def main():
    import sys, os
    if len(sys.argv) > 1:
        f = sys.argv[1]
        try:
            with open(f, "r") as fi:
                s = str_to_bin(str(fi.read()))
        except:
            s=sys.argv[1]

        #print (text_from_bits(d0(text_to_bits(s))))
        print (bin_to_hex(d0(str_to_bin(s))))


def ogkush(s):
    return (bin_to_hex(d0(str_to_bin(s))))

if __name__ == "__main__":
    main()
