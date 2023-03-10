import math
import random
import time

# MAX_BIT は鍵の bit 長
MAX_BIT = 10


# テスト
def key_test(key):
    print("-----テストを開始します-----")

    n = key["n"]
    e = key["e"]
    p = key["p"]
    q = key["q"]
    l = key["l"]
    d = key["d"]

    try:
        if not isPrime(p) or not isPrime(q):
            raise ValueError("p,q error: p の値が素数ではない")
        if n != p * q:
            raise ValueError("n error: n の値が p * q と不一致")
        if l != lcm(p - 1, q - 1):
            raise ValueError("l error: l の値が p-1, q-1 の最小公倍数になっていない")
        if math.gcd(e, l) != 1:
            raise ValueError("e error: e が l と互いに素でない")
        if ((e * d) % l) != 1:
            raise ValueError("d error: e * d mod l の値が 1 にならない")

        message = 100
        enc_result = rsa_enc(key, message)
        dec_result = rsa_dec(key, enc_result)
        if not (message == dec_result):
            print("平文: ", message)
            print("暗号結果: ", enc_result)
            print("復号結果: ", dec_result)
            raise ValueError("復号結果が平文と不一致")

        print("All Test Passed!")
        print("")
    except ValueError as e:
        print(e)
        exit(1)


# 最大公約数を求める関数
def lcm(p, q):
    return p // math.gcd(p, q) * q


# n bit の素数を作成する関数
def isPrime(p):
    count = 0

    while count <= 40:
        a = random.randint(1, p)

        num = pow(a, p - 1, p)
        if num == 1:
            count = count + 1
        else:
            return False

    return True


# a~b の範囲で素数を生成する関数
def make_prime(a, b):
    p = random.randint(a, b)
    while not (isPrime(p)):
        p = random.randint(a, b)
        # print(".", end="")
    # print("!")
    # print("")
    return p


# n bit の素数を二つ作成する関数
def make_p_q(n):
    global MAX_BIT
    key = {"p": make_prime(pow(2, n - 1), pow(2, n) - 1), "q": make_prime(pow(2, n - 1), pow(2, n) - 1)}
    return key


# 秘密鍵 e を作成
# e は l と互いに素
def make_e(l):
    return make_prime(1, l)


# 情報逆元を求める関数1: pow関数で逆元を求める
def make_d_1(e, l):
    return pow(e, -1, l)


# 情報逆元を求める関数2: 自作の関数で逆元を求める
def make_d_2(e, l):
    (A, B) = (l, e)
    (a, b) = (0, 1)
    while True:
        if A % B == 0:
            return l - b
        q = A // B
        (A, B) = (B, A % B)
        (a, b) = (b, a - q * b)


# n bit の秘密鍵・公開鍵を作成する関数
def make_key(n):
    key = make_p_q(n)
    l = lcm(key["p"] - 1, key["q"] - 1)
    key["n"] = key["p"] * key["q"]
    key["l"] = l
    e = make_e(l)
    key["e"] = e
    d = make_d_1(e, l)
    key["d"] = d
    return key


# 鍵を表示する print 関数
def printer(key):
    print("------------公開鍵------------")
    print("n (= p*q ) = ", key["n"])
    print("e          = ", key["e"])
    print("")
    print("------------秘密鍵------------")
    print("d          = ", key["d"])
    print("")
    print("------------その他------------")
    print("p          = ", key["p"])
    print("q          = ", key["q"])
    print("l          = ", key["l"])
    print("")


# 暗号化
def rsa_enc(pub_key, message):
    e = pub_key["e"]
    n = pub_key["n"]
    result = pow(message, e, n)
    return result


# 復号化
def rsa_dec(priv_key, message):
    d = priv_key["d"]
    n = priv_key["n"]
    result = pow(message, d, n)
    return result


def message_to_int(message_str):
    m_byte = bytes(message_str, 'utf-8')
    m_int = int.from_bytes(m_byte, 'big')
    return m_int


def int_to_message(message_int):
    bytelen = math.ceil(math.log2(message_int) / 8)
    m_byte = message_int.to_bytes(bytelen, 'big')
    m_str = m_byte.decode('utf-8')
    return m_str


# main 関数
def main():
    global MAX_BIT

    # if MAX_BIT == 0:
    #     MAX_BIT = 100
    #
    # # 鍵の生成と表示とテスト
    # key = make_key(MAX_BIT)
    # printer(key)
    # key_test(key)
    #
    # # 暗号化・復号化
    # message = message_to_int("hello")
    # enc_result = rsa_enc(key, message)
    # dec_result = rsa_dec(key, enc_result)
    #
    # print("平文　(int)　　　　　: ", message)
    # print("平文　(str)　　　　　: ", int_to_message(message))
    # print("エンコード後　(int)　: ", enc_result)
    # print("デコード後　(int)　　: ", dec_result)
    # print("デコード後　(str)　　: ", int_to_message(dec_result))

    if True:
        # 30 bit から 1024 bit まで、20 bit 幅の鍵を生成し、テストする
        message = 100
        time_list = []
        bit_list = []
        for i in range(30, 1024, 20):
            bit_list.append(i)

            start = time.time()

            for j in range(3):
                key = make_key(i)
                message_enc = rsa_enc(key, message)
                message_enc_dec = rsa_dec(key, message_enc)

            end = time.time()
            print("bit数: ", i, " 暗号化・復号化にかかった時間: ", (end - start)/3, " 秒")
            time_list.append((end - start)/3)
        print(time_list)
        print(bit_list)

if __name__ == "__main__":
    print("実行開始")
    main()
