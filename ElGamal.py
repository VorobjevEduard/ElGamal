import math
import matplotlib.pyplot as plt
import random
import hashlib
import hmac


# код для генерации эллиптической кривой
p = 31991
t = int(math.log2(p))
s = int((t-1)/160)
v = t - s*160
g = 1024


def gen_rand(string):
    "Функция, шифрующая пароль и возвращающая битовую строку"
    sign = hmac.new(bytearray('text','utf-8'), bytearray(str(string),'utf-8'), hashlib.sha512).hexdigest()
    return bin(int(sign,16))

def get_seedE(lens):
    "Возвращает seed"
    return bin(random.getrandbits(lens)),random.getrandbits(lens)

def alg():
    "Алгоритм генерации случайной кривой"
    while True:
        r = 0
        while True:
            seedE, z = get_seedE(g)
            h = gen_rand(seedE)
            W0 = '0' + h[-v+1:]
            W = W0
            for i in range(1, s+1):
                si = (z+i)%(2**g)
                Wi = gen_rand(bin(-si))
                W += Wi[2:]
            r = int(W,2)
            if r != 0 and (4*r + 27)%p!=0:
                break
        a = 0
        b = 1
        # print("r = {}".format(r))
        while b < p:
            A = (r * (b**2))%p
            if A != 0 and b != 0 and (A**(1/3) == int(A**(1/3))):
                a = A**(1/3)
                break
            b += 1
        if b == p:
            continue
        print("Полученная кривая: y^2 = x^3 + {a}x + {b}".format(a=int(a),b=b))
        return int(a), int(b)

koef_a, koef_b = alg()

def checkpoint(p_1,p_2):
    "проверка условия р1 и р2"
    if p_1['x'] == p_2['x'] and p_1['y'] == -p_2['y']%p:
        return True
    else:
        return False

def get_lmbd(p_1,p_2):
    "подсчет лямбды"
    if p_1==p_2:
        lmbd = (3*(p_1['x']**2)+koef_a)%p
        lmbd2 = (2*p_1['y'])%p
        rev = pow(lmbd2,p-2,p)
        result_lmbd = (lmbd*rev)%p
        return result_lmbd
    else:
        lmbd = (p_2['y'] - p_1['y'])%p
        lmbd2 = (p_2['x'] - p_1['x'])%p
        rev = pow(lmbd2,p-2,p)
        result_lmbd = (lmbd*rev)%p
        return result_lmbd

def get_ny(p_1,p_2):
    "подсчет ню"
    ny = (p_1['y']*p_2['x'] - p_2['y']*p_1['x'])%p
    ny2 = (p_2['x']-p_1['x'])%p
    rev = pow(ny2,p-2,p)
    result_ny = (ny*rev)%p
    return result_ny

def get_X_Y(p_1,p_2):
    "подсчет х и у"
    x = get_lmbd(p_1,p_2)**2-p_1['x'] - p_2['x']
    y = get_lmbd(p_1,p_2)*(p_1['x'] - x) - p_1['y']
    result_X_Y = {'x' : x % p,'y' : y % p}
    return result_X_Y

def get_point(sec,point = {'x': 0,'y': 5585}, out = None):
    # if not check(point):
    #    return {'x': 0,'y': 5585}
    p_1 = point
    p_2 = point
    l=1
    if out:
        out.write(str(p_1) + '\n')
    while True:
        l+=1
        if checkpoint(p_1,p_2):
            p_3 = {'x':0,'y':0}
        else:
            p_3 = get_X_Y(p_1,p_2)
        if out:
            out.write(str(p_3)+"\n")    
        if l==sec:
            return p_3
        p_2 = p_3

results = []

def check(point):
    "проверка уравнения кривой в точке"
    if point == None:
        return False
    if point['y']**2%p == (point['x']**3+point['x']*koef_a + koef_b)%p:
        return True
    else:
        return False
    
if __name__ == "__main__":
    x = [0,]
    y = [5585,]
    p_1 = {'x':0,'y':5585}
    p_2 = {'x':0,'y':5585}
    l=0
    results.append(p_2)
    f = open('text.txt', 'w')
    for i in range(1, 32089): # перебор точек на кривой
        if checkpoint(p_1,p_2):
            p_3 = {'x':0,'y':0}
        else:
            p_3 = get_X_Y(p_1,p_2)
        f.write(str(p_3) + '\n')
        
        if p_3 not in results:
            x.append(p_3['x'])
            y.append(p_3['y'])
            results.append(p_3)
        p_2 = p_3

    f.close()
    plt.plot(x,y,'+')
    plt.grid()
    plt.show()

    # код, реализующий шифрование по алгоритму Эль-Гамаля
    c = 5103
    k = 523
    m = int(input("Введите сообщение (в числовой форме) для зашифрования: "))

    def El_Gam():
        "функция реализующая алгоритм Эль-Гамаля"
        print("Открытый ключ: ", get_point(c)) # открытый ключ в виде х и у
        P = get_point(k,get_point(c))
        R = get_point(k)
        e = m*P['x']%p  # шифр-ключ в виде х и у
        print("Шифртекст: ",R,e)
        Q = get_point(c,R)
        rev = pow(Q['x'],p-2,p)
        opentext = e*rev%p
        print("Расшированный текст: ", opentext)
    
    El_Gam()
