import re

def make_dict(keys, values):
    dictionary = {}
    for (k, v) in zip(keys, values):
        dictionary[k] = v
    return dictionary

def word_count(fn):
    dictionary = {}
    f = open(fn, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.lower()
        line = line.replace('\t',' ')
        # line = re.sub(r'[^\w\s]','',line)
        for word in re.split('\W+', line):
            if word not in dictionary:
                dictionary[word] = 1
            else:
                dictionary[word] += 1
    print(dictionary['all'])
    print(dictionary['code'])
    print(dictionary['gupta'])
    return dictionary

def load_words(filename,regexp):
    res = []
    prog = re.compile(regexp)
    f = open(filename, 'r')
    lines = f.readlines()
    for word in lines:
        result = prog.match(word)
        if result:
            word = word.replace('\n', '')
            res.append(word)
    return res

def transform_reverse(str):
    reversed_str = ""
    for char in str:
        reversed_str = char + reversed_str
    return [str, reversed_str]

def transform_capitalize(string):
    res = []
    size = len(string)
    for x in range(2**size):
        helper = 1
        temp = list(string)
        for times in range(size):
            if x & helper != 0:
                cap = temp[size-1-times].upper()
                temp[size-1-times] = cap
            helper = helper << 1
        temp = "".join(temp)
        res.append(temp)
    return res

similar ={'o':set([0]), 'i':set([1]), 'l':set([1]), 'z':set([2]), 'e':set([3]), 'a':set([4]), 's':set([5]), 'b':set([6,8]), 't':set([7]), 'g':set([9]), 'q':set([9])}
def transform_digits(string):
    res = [string]
    size = len(string)
    for x in range(size):
        char = string[x].lower()
        cur_size = len(res)
        if char in similar:
            for i in range(cur_size):
                for t in similar[char]:
                    temp = list(res[i])
                    temp[x] = str(t)
                    temp = "".join(temp)
                    res.append(temp)
    return res

def load_passwd(filename):
    res = []
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        dic = {}
        line = line.split(':')
        dic['account'] = line[0]
        dic['password'] = line[1]
        dic['UID'] = line[2]
        dic['GID'] = line[3]
        dic['GECOS'] = line[4]
        dic['directory'] = line[5]
        dic['shell'] = line[6]
        res.append(dic)
    return res


from passlib import hash
def check_pass(plain,enc):
    salt = enc[:2]
    return hash.des_crypt.encrypt(plain,salt=salt) == enc


def crack_pass_file(pass_filename,words_filename,out_filename):
    # create a dictionary : password -> user
    p2u = {}
    f = open(pass_filename, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.split(':')
        p2u[line[1]] = line[0]
    #########################################
    words = load_words(words_filename, r"^\w{6,8}$")
    output = open(out_filename, 'w')
    found = []
    # try original words and reversed version
    for word in words:
        for pair in p2u:
            if check_pass(word, pair):
                output.write(p2u[pair] + "=" + word + '\n')
                output.flush()
                found.append(pair)
            reversed_word = transform_reverse(word)[1]
            if check_pass(reversed_word, pair):
                output.write(p2u[pair] + "=" + reversed_word + '\n')
                output.flush()
                found.append(pair)
    if len(found) > 0:
        for p in found:
            p2u.pop(p)
    found = []
    # try words with capitals and reversed version
    for word in words:
        for new_word in transform_capitalize(word):
            for pair in p2u:
                if check_pass(new_word, pair):
                    output.write(p2u[pair] + "=" + new_word + '\n')
                    output.flush()
                    found.append(pair)
                reversed_word = transform_reverse(new_word)[1]
                if check_pass(reversed_word, pair):
                    output.write(p2u[pair] + "=" + reversed_word + '\n')
                    output.flush()
                    found.append(pair)
    if len(found) > 0:
        for p in found:
            p2u.pop(p)
    found = []
    #try words with digits and reversed version
    for word in words:
        for new_word in transform_digits(word):
            for pair in p2u:
                if check_pass(new_word, pair):
                    output.write(p2u[pair] + "=" + new_word + '\n')
                    output.flush()
                reversed_word = transform_reverse(new_word)[1]
                if check_pass(reversed_word, pair):
                    output.write(p2u[pair] + "=" + reversed_word + '\n')
                    output.flush()
    output.close()
    return

# def crack_pass_file(pass_filename,words_filename,out_filename):
#     # users = load_passwd(pass_filename)
#     # words = load_words(words_filename, r"^\w{6,8}$")
#     # output = open(out_filename, 'w')
#     #
#     # found = []
#     # # start from the easiest password: pure words
#     # for user in users:
#     #     for word in words:
#     #         if check_pass(word, user['password']):
#     #             output.write(user['account'] + "=" + word + '\n')
#     #             output.flush()
#     #             found.append(user)
#     #             break
#     #         # reversed words
#     #         reversed_word = transform_reverse(word)[1]
#     #         if check_pass(reversed_word, user['password']):
#     #             output.write(user['account'] + "=" + reversed_word + '\n')
#     #             output.flush()
#     #             found.append(user)
#     #             break
#     # # update users
#     # if len(found) > 0:
#     #     for elem in found:
#     #         users.remove(elem)
#     # try capitals
#     # if len(users) != 0:
#     #     for user in users:
#     #         for word in words:
#     #             if user in found:
#     #                 break
#     #             for new_word in transform_capitalize(word):
#     #                 if check_pass(new_word, user['password']):
#     #                     output.write(user['account'] + "=" + new_word + '\n')
#     #                     output.flush()
#     #                     found.append(user)
#     #                     break
#     #                 # reversed
#     #                 reversed_word = transform_reverse(new_word)[1]
#     #                 if check_pass(reversed_word, user['password']):
#     #                     output.write(user['account'] + "=" + reversed_word + '\n')
#     #                     output.flush()
#     #                     found.append(user)
#     #                     break
#     #
#     # # update users
#     # if len(found) > 0:
#     #     for elem in found:
#     #         users.remove(elem)
#     # try digits
#     if len(users) != 0:
#         for user in users:
#             for word in words:
#                 if user in found:
#                     break
#                 for new_word in transform_digits(word):
#                     if check_pass(new_word, user['password']):
#                         output.write(user['account'] + "=" + new_word + '\n')
#                         output.flush()
#                         found.append(user)
#                         break
#                     # reversed
#                     reversed_word = transform_reverse(new_word)[1]
#                     if check_pass(reversed_word, user['password']):
#                         output.write(user['account'] + "=" + reversed_word + '\n')
#                         output.flush()
#                         found.append(user)
#                         break
#
#     output.close()
#     return
