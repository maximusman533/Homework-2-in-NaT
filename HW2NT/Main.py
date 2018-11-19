from math import factorial


def number_to_bv(number, depth=7):
    vector = [0]*depth
    counter = depth
    while number:
        counter -= 1
        res = number % 2
        number //= 2
        vector[counter] = res
    return vector


def bv_to_number(bit_v):
    power = 0
    number = 0
    for bit in bit_v[::-1]:
        number += bit*pow(2, power)
        power += 1
    return number


def combination(n, k):
    return factorial(n)/(factorial(k)*factorial(n-k))


def multiplicity(vector):
    m = 0
    for i in vector:
        if i == 1:
            m += 1
    return m


def err_synd(v):
    b_v = v[::-1]
    err_s = [0]*3
    err_s[2] = (b_v[0] ^ b_v[2] ^ b_v[4] ^ b_v[6])
    err_s[1] = (b_v[1] ^ b_v[2] ^ b_v[5] ^ b_v[6])
    err_s[0] = (b_v[3] ^ b_v[4] ^ b_v[5] ^ b_v[6])
    return err_s


def err_fix(v, err_s):
    f_err_v = [0] * len(v)
    n_b = bv_to_number(err_s)
    if n_b != 0:
        f_err_v[n_b - 1] = 1
    fixed_v = my_xor(v, f_err_v[::-1])
    return fixed_v


def my_xor(iv, ev):
    return list(map(lambda x: x[0] ^ x[1], zip(iv, ev)))


def print_table(table):
    for header in table[0].keys():
        print(header, end=' ')
    print()
    for table_row in table:
        for res in table_row.items():
            str_l = len(res[0]) - len(res[1].__str__()) + 4
            print(res[1], end=' ' * str_l)
        print()


err = 0
inf_v = [1, 1, 1, 1, 0, 0, 0]
table = [{'Кратность': i,
                 'Число сочетаний': combination(7, i),
                 'Число обнаруженных ошибок': 0,
                 'Обнаруживающаяся способность кода': 0,
                 'Число исправленных ошибок': 0,
                 'Корректирующая способность кода': 0} for i in range(1, 8)]
while True:
    err += 1

    err_v = number_to_bv(err)
    m = multiplicity(err_v)
    e_inf_v = my_xor(inf_v, err_v)
    e_s = err_synd(e_inf_v)

    if any(e_s):
        table[m-1]['Число обнаруженных ошибок'] += 1

    f_inf_v = err_fix(e_inf_v, e_s)

    if inf_v == f_inf_v:
        table[m - 1]['Число исправленных ошибок'] += 1

    if all(number_to_bv(err)):
        break

for t_r in table:
    t_r['Обнаруживающаяся способность кода'] = t_r['Число обнаруженных ошибок'] / t_r['Число сочетаний']
    t_r['Корректирующая способность кода'] = t_r['Число исправленных ошибок'] / t_r['Число сочетаний']

print_table(table)


