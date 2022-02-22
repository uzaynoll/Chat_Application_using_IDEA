from Operations.ascii_conversion import ascii_to_string
from Operations.additive_modulo import additive_modulo, addition_inverse
from Operations.multiplication_modulo import multiplication_modulo, multiplication_inverse
from Operations.bitwise_XOR import bitwise_XOR

def decrypt(input_ascii, key):
    print("\t"+"-"*80+f"\n\tDecrypting the message: "+ascii_to_string(input_ascii)+"\n")
    plaintext_ascii = list()
    
    iterations = int(len(input_ascii) / 8)
    print(f"\n\t'{iterations}' 64 bit blocks to be computed \n")
    for j in range(0,iterations):
        p1 = [input_ascii[(j*8)+0], input_ascii[(j*8)+1]]
        p2 = [input_ascii[(j*8)+2], input_ascii[(j*8)+3]]
        p3 = [input_ascii[(j*8)+4], input_ascii[(j*8)+5]]
        p4 = [input_ascii[(j*8)+6], input_ascii[(j*8)+7]]

        print("\t"+"#"*80+f"\n\t"+str(j+1)+"TH ITERATION\n")
        print(f"\n\t64 bit TEXT: '"+ascii_to_string(p1+p2+p3+p4)+"'\n")

        for i in range(8):
            k1 = multiplication_inverse([key[i][0], key[i][1]])
            k2 = addition_inverse([key[i][2], key[i][3]])
            k3 = addition_inverse([key[i][4], key[i][5]])
            k4 = multiplication_inverse([key[i][6], key[i][7]])
            k5 = [key[i+1][8], key[i+1][9]]
            k6 = [key[i+1][10], key[i+1][11]]
            
            print("\n\t\t"+str(i+1)+f"TH ROUND KEYS: "+ascii_to_string(k1+k2+k3+k4+k5+k6)+"\n")

            d1 = multiplication_modulo(p1, k1)
            d2 = additive_modulo(p2, k2)
            d3 = additive_modulo(p3, k3)
            d4 = multiplication_modulo(p4, k4)
            d5 = bitwise_XOR(d1, d3)
            d6 = bitwise_XOR(d2, d4)
            d7 = multiplication_modulo(d5, k5)
            d8 = additive_modulo(d6, d7)
            d9 = multiplication_modulo(d8, k6)
            d10 = additive_modulo(d7, d9)
            d11 = bitwise_XOR(d1, d9)
            d12 = bitwise_XOR(d3, d9)
            d13 = bitwise_XOR(d2, d10)
            d14 = bitwise_XOR(d4, d10)

            p1 = d11
            p2 = d13
            p3 = d12
            p4 = d14
            
            print("\n\t\t"+str(i+1)+f"TH ROUND OUTPUT: "+ascii_to_string(p1+p2+p3+p4)+"\n")
        
        k1 = multiplication_inverse([key[8][0], key[8][1]])
        k2 = addition_inverse([key[8][2], key[8][3]])
        k3 = addition_inverse([key[8][4], key[8][5]])
        k4 = multiplication_inverse([key[8][6], key[8][7]])
        
        print(f"\n\t\t9TH ROUND KEYS: "+ascii_to_string(k1+k2+k3+k4)+"\n")

        d1 = multiplication_modulo(p1, k1)
        d2 = additive_modulo(p2, k2)
        d3 = additive_modulo(p3, k3)
        d4 = multiplication_modulo(p4, k4)
        
        print(f"\n\t\t9TH ROUND OUTPUT:"+ascii_to_string(d1+d2+d3+d4)+"\n")

        plaintext_ascii.extend(d1+d2+d3+d4)

    plaintext = ascii_to_string(plaintext_ascii)
    print("\n\tPLAIN TEXT: "+plaintext+"\n")
    
    return plaintext