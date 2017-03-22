#!/usr/bin/python
# coding:utf-8
import string
import random
import re
import py_compile


def hide_strings(content):
    # WARNING PAS de ''' STRINGS SUR PLUSIEURS LIGNES !
    # pas prise en charge quand " et ' sur même ligne
    data = content.split('\n')
    temp = []
    for line in data:
        temp.append(line + '\n')
    data = temp
    output_without_strings = data
    ind = 0
    for line in data:
        if (len(line.split('\'')) == 1 and len(line.split('"')) == 1) or ('"' in line and "'" in line):
            pass
        else:
            a = b = None
            try:
                a = line.index('\'')
            except ValueError:
                try:
                    b = line.index('"')
                except ValueError:
                    pass
            output = line
            if not a:
                x = len(line.replace('\\"', '').replace('\\\'', '').split('"'))
                number_strings = (x - 1) / 2
                i, y, x = 1, 0, 0
                while x != number_strings:
                    strings_index = []
                    y = 0
                    special = False
                    for caract in output:
                        if caract == '\\':
                            special = True
                        elif special:
                            special = False
                        elif caract == '"':
                            strings_index.append(y)
                        y += 1
                    target = [output[:strings_index[0]], output[strings_index[0] + 1:strings_index[1]],
                              output[strings_index[1] + 1:]]
                    out = target[0] + 'str('
                    special = False
                    if target[1] == '':
                        out += '('
                    for caract in target[1]:
                        if caract == '\\':
                            out += '\'\\'
                            special = True
                        elif special:
                            out += caract + '\'+'
                            special = False
                        else:
                            out += 'unichr({})+'.format(str(ord(caract)))
                    out = out[:-1] + ')'
                    output = out + target[2]
                    i += 2
                    x += 1

            elif not b:
                x = len(line.split('\''))
                number_strings = (x - 1) / 2
                i = 0
                while i != number_strings:
                    target = output.split('\'', 2)
                    out = target[0] + 'str('
                    special = False
                    if target[1] == '':
                        out += '('
                    for caract in target[1]:
                        if caract == '\\':
                            out += '"\\'
                            special = True
                        elif special:
                            out += caract + '"+'
                        else:
                            out += 'unichr({})+'.format(str(ord(caract)))
                    out = out[:-1] + ')'
                    output = out + target[2]
                    i += 1

            output_without_strings[ind] = output

        ind += 1
    # detect where strings are and put them in unichr
    final = ''
    for line in output_without_strings:
        final += line
    return final


def invert_bool(content):
    """Inverse les booléens False et True"""

    i = 0
    output = ''
    for line in content.split('\n'):
        if i == 2:
            output += 'True,False=False,True\n' + line.replace('False', 'TEMP').replace('True', 'False').replace('TEMP',
                                                                                                                 'True')
        else:
            output += line.replace('False', 'TEMP').replace('True', 'False').replace('TEMP', 'True')
        output += '\n'
        i += 1
    return output


def gen_string(longueur):
    """Génère une chaine de caractère aléatoire de la longueur 'longueur' """

    charset = string.ascii_lowercase + string.uppercase
    output = ''
    for i in range(longueur):
        output += random.choice(charset)

    return output


def find_max(content, target):
    """Trouve le nombre maximum de IMP, CLASS ou autre"""

    out = None
    for i in re.finditer(target, content):
        test = int(content[i.end():i.end() + 3])
        if test > out:
            out = test
    return out


def replace_names(content, target, max_targ, l):
    """Remplace les noms comme par exemple IMP001 ou VAR016"""
    if max_targ:
        targ_names = []
        for i in range(1, max_targ + 1):
            gen = gen_string(l)
            while gen in targ_names:
                gen = gen_string(l)

            targ_names.append(gen)
            if i < 10:
                content = content.replace(target + '00' + str(i), gen)

            elif 9 < i < 100:
                content = content.replace(target + '0' + str(i), gen)

            else:
                content = content.replace(target + str(i), gen)

    return content


def decomp_nbr(nbr):
    d = 2
    output = []
    while d <= nbr:
        if nbr % d == 0:
            output.append(d)
            nbr = nbr / d
        else:
            d += 1
    return output


def generate_and(number):
    target = bin(number)[2:]
    tar_iter = iter(target)
    found_1 = ''
    found_2 = ''
    while 1:
        try:
            a = tar_iter.next()
            if a == '1':
                found_1 += '1'
                found_2 += '1'

            else:
                x = str(random.randint(0, 1))
                found_1 += x
                if x == '1':
                    found_2 += '0'
                else:
                    found_2 += str(random.randint(0, 1))

        except StopIteration:
            break

    return '(' + str(int(found_1, 2)) + '&' + str(int(found_2, 2)) + ')'


def generate_or(number):
    target = bin(number)[2:]
    tar_iter = iter(target)
    found_1 = ''
    found_2 = ''
    while 1:
        try:
            a = tar_iter.next()
            if a == '1':
                x = str(random.randint(0, 1))
                found_1 += x
                if x == '0':
                    found_2 += '1'
                else:
                    found_2 += str(random.randint(0, 1))
            else:
                found_1 += '0'
                found_2 += '0'
        except StopIteration:
            break
    return '(' + str(int(found_1, 2)) + '|' + str(int(found_2, 2)) + ')'


def generate_xor(number):
    target = bin(number)[2:]
    tar_iter = iter(target)
    found_1 = ''
    found_2 = ''
    while 1:
        try:
            a = tar_iter.next()
            if a == '1':
                x = str(random.randint(0, 1))
                found_1 += x
                if x == '0':
                    found_2 += '1'
                else:
                    found_2 += '0'
            else:
                x = str(random.randint(0, 1))
                found_1 += x
                if x == '0':
                    found_2 += '0'
                else:
                    found_2 += '1'
        except StopIteration:
            break
    return '(' + str(int(found_1, 2)) + '^' + str(int(found_2, 2)) + ')'


def obf_nbr(content):
    """Pour cacher les nombres entre balises [NBR][NBR]
    exemple :
    a=[NBR]2048[NBR]"""
    target_nbr = []
    law = {1: generate_and, 2: generate_or, 3: generate_xor}
    data = content.split('[NBR]')
    for x in range(1, len(data), 2):
        target_nbr.append(data[x].replace(' ', ''))
    targ_iter = iter(target_nbr)
    iter_in = iter(target_nbr)
    while 1:
        try:
            targ = targ_iter.next()
        except StopIteration:
            break
        negatif = False
        out = ''
        if targ[0] == '-':
            out = '-1*('
            negatif = True
            targ = targ[1:]
        if '.' in targ:
            targ1 = targ.split('.')[0]
            targ2 = targ.split('.')[1]
            decomp_targ1 = decomp_nbr(int(targ1))
            decomp_targ2 = decomp_nbr(int(targ2))

            out1 = out2 = '('
            decomp_targ1_iter = iter(decomp_targ1)
            decomp_targ2_iter = iter(decomp_targ2)
            while 1:
                try:
                    out1 += law[random.randint(1, 3)](decomp_targ1_iter.next()) + '*'
                except StopIteration:
                    break

            out1 = out1[:-1] + ')'
            while 1:
                try:
                    out2 += law[random.randint(1, 3)](decomp_targ2_iter.next()) + '*'
                except StopIteration:
                    break

            out2 = out2[:-1] + ')'
            out += "float(str({})+unichr(46)+str({}))".format(out1, out2)
        else:
            if len(targ) > 10 or targ == 1:
                one = False
                if targ == 1:
                    one = True
                    targ1 = random.randint(1000, 999999)
                    targ2 = targ1 + 1
                else:
                    targ1 = targ[:-10]
                    targ2 = targ[-10:]
                decomp_targ1 = decomp_nbr(int(targ1))
                decomp_targ2 = decomp_nbr(int(targ2))

                out += '(('
                decomp_targ1_iter = iter(decomp_targ1)
                decomp_targ2_iter = iter(decomp_targ2)
                while 1:
                    try:
                        out += law[random.randint(1, 3)](decomp_targ1_iter.next()) + '*'
                    except StopIteration:
                        break
                if one:
                    out = out[:-1] + ')-('
                else:
                    out = out[:-1] + ')+('

                while 1:
                    try:
                        out += law[random.randint(1, 3)](decomp_targ2_iter.next()) + '*'
                    except StopIteration:
                        break

                out = out[:-1] + '))'

            else:
                decomp_targ = decomp_nbr(int(targ))
                out += '('
                decomp_targ_iter = iter(decomp_targ)
                while 1:
                    try:
                        out += law[random.randint(1, 3)](decomp_targ_iter.next()) + '*'
                    except StopIteration:
                        break
                out = out[:-1] + ')'

        if negatif:
            out += ")"

        targ_in = iter_in.next()
        x = content.index("[NBR]" + targ_in + "[NBR]")
        content = content[:x] + out + content[x + len("[NBR]" + targ_in + "[NBR]"):]
    return content


def bytecode_file(filename):
    py_compile.compile(filename)
    print('[+] Généré avec succès')


def protect(content):
    out = ''
    nbr = 0
    original = content
    content = content.split('\n')
    if ('#' in content[0] and '!' in content[0].replace(' ', '')) or ('#' in content[0] and 'coding' in content[0]):
        nbr += 1
    if ('#' in content[1] and '!' in content[1].replace(' ', '')) or ('#' in content[1] and 'coding' in content[1]):
        nbr += 1

    content = content[nbr:]
    tmp = content[nbr+1]
    original=original.split('\n')
    for i in range(nbr):
        out += original[i] + '\n'

    if len(original[original.index(tmp):]) > 2500:
        tmp = '#' + gen_string(1242)
        out += 'exec(str('
        for caract in tmp:
            out += 'unichr({})+'.format(ord(caract))
        out = out[:-1] + "))\n"
        for line in content:
            out += line + "\n"
    else:
        if len(content)<1243:
            content+="#"+gen_string(1243-len(content))
        out += "exec(str("
        for line in content:
            special = False
            for caract in line:
                if caract == '\\':
                    special = True
                    out += "'\\"
                elif special:
                    out += caract + "'+"
                    special = False
                else:
                    out += "unichr({})+".format(ord(caract))
            out += "unichr({})+".format(ord("\n"))
        out = out[:-1] + "))"
    return out


def obf(filename, output_file=None, protect_it=False, bytecode=False):
    fich = None
    try:
        fich = open(filename, 'r')
    except IOError:
        print('Error, file not found...')
        exit(1)
    if not output_file:
        output_file = 'obf_' + filename
    content = fich.read()

    content = invert_bool(content)

    print('[+] Boolean inversion done')

    max_IMP = find_max(content, 'IMP')
    max_LOC = find_max(content, 'LOC')
    max_VAR = find_max(content, 'VAR')
    max_FUNC = find_max(content, 'FUNC')
    max_CLASS = find_max(content, 'CLASS')

    content = replace_names(content, 'IMP', max_IMP, 4)
    content = replace_names(content, 'LOC', max_LOC, 5)
    content = replace_names(content, 'VAR', max_VAR, 6)
    content = replace_names(content, 'FUNC', max_FUNC, 3)
    content = replace_names(content, 'CLASS', max_CLASS, 2)

    print('[+] Variable obfuscation done')

    content = hide_strings(content)
    print('[+] Strings obfuscation done')
    content = obf_nbr(content)
    print('[+] Numbers obfuscation done')
    if protect_it:
        content = protect(content)
        print('[+] Protected !')
    content.replace('\\', '\\\\')
    outfich = open(output_file, 'w')
    outfich.write(content)
    outfich.close()
    if bytecode:
        bytecode_file(output_file)
    if bytecode:
        print('Saved to : ' + output_file + 'c')
    else:
        print('Saved to : ' + output_file)

    return


if __name__ == "__main__":
    try:
        infile = raw_input('Template file : ')
        outfile = raw_input('Output file : ')
        ans = raw_input('Protect the file from bytecode decoders ? (Y/N) : ')
        if ans.upper() == 'Y':
            obf(infile, outfile, True, True)
            print("The protected file is saved as : {}\nGenerated source file saved as : {}".format(outfile + 'c',outfile))
        else:
            ans = raw_input('Obfuscate even more the script ? (Y/N) : ')
            if ans.upper()=='Y':
                obf(infile, outfile, False, False)
            else:
                obf(infile, outfile, False, False)
            print("New file is saved as : {}".format(outfile))
    except KeyboardInterrupt:
        print('Exiting...')
        exit(0)