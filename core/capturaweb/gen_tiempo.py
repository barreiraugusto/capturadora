import time


def contar():
    contador = 0
    with open('/home/augusto/Documentos/CODIGOS/CAPTURADORA/capturadora/cuenta.txt', 'w') as cuenta:
        while contador < 10000:
            contador += 1
            print(contador)
            linea = f'frame=   135 q= -1.0 f_size=     95 s_size=      260kB time= {contador}.00 br=    19.0kbits/s avg_br=   388.5kbits/s type= P\n'
            #cuenta.seek(0)
            cuenta.write(linea)
            time.sleep(1)
            #cuenta.truncate()


if __name__ == '__main__':
    contar()
