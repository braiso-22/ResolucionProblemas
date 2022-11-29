
# import library for sleep
import time  

TorreA = []
TorreB = []
TorreC = []


#dibuja las torres, máximo 10 niveles
def TorresPrint(A, B, C,n=10):
    for i in range(n):
        if len(A) >= (n-i): la = A[n-i-1]
        else: la = 0
        if len(B) >= (n-i): lb = B[n-i-1]
        else: lb = 0
        if len(C) >= (n-i): lc = C[n-i-1]
        else: lc = 0

        sa = " "*(n - la) + "*"*la + "|" + "*"*la + " "*(n - la) + " "
        sb = " "*(n - lb) + "*"*lb + "|" + "*"*lb + " "*(n - lb) + " "
        sc = " "*(n - lc) + "*"*lc + "|" + "*"*lc + " "*(n - lc) + " "
        s = sa + sb + sc

        print(s)
    s = "="*(n + 1 + n) + " " + "="*(n + 1 + n) + " " + "="*(n + 1 + n) 
    print(s)
    print()

def iniciar():
    global TorreA, TorreB, TorreC
    TorreA = []
    TorreB = []
    TorreC = []
    n = int(input("Numero de discos: "))
    for i in range(n):
        TorreA.append(n-i)
    TorresPrint(TorreA,TorreB,TorreC,n)
    print("""
==========================
|  Torres de Hanoi       |
==========================
""")
    return n

def solucion():
    n=3
    mover(TorreA, TorreC)
    TorresPrint(TorreA,TorreB,TorreC,n)
    mover(TorreA,TorreB)
    TorresPrint(TorreA,TorreB,TorreC,n)
    mover(TorreC, TorreB)
    TorresPrint(TorreA,TorreB,TorreC,n)
    mover(TorreA,TorreC)
    TorresPrint(TorreA,TorreB,TorreC,n)
    mover(TorreB,TorreA)
    TorresPrint(TorreA,TorreB,TorreC,n)
    mover(TorreB, TorreC)
    TorresPrint(TorreA,TorreB,TorreC,n)
    mover(TorreA,TorreC)
    TorresPrint(TorreA,TorreB,TorreC,n)

def mover(origen, destino,n):
    destino.append(origen.pop())
    TorresPrint(TorreA,TorreB,TorreC,n)
    time.sleep(0.01)

def solucion_automatica(numero, origen, destino, auxiliar,n):
    if numero == 1:
        mover(origen, destino,n)
        pass
    else:
        solucion_automatica(numero-1, origen, auxiliar, destino,n)
        mover(origen, destino,n)
        solucion_automatica(numero-1, auxiliar, destino, origen,n)


def main():    
    n =iniciar()
    
    solucion_automatica(n, TorreA, TorreC, TorreB,n)
    print((2**n)-1, "movimientos")

if __name__ == "__main__":
    main()
