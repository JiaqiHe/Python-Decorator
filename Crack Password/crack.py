
from misc import *
import crypt
import re

# Load the words from the file filename that match the regular
#    expression regexp.  Returns a list of matching words in the order
#    they are in the file.
def load_words(filename,regexp):
    res = [] # create a list to store output
    prog = re.compile(regexp) # compile the regular expression
    f = open(filename, 'r') # open the target file
    lines = f.readlines() # read lines
    for word in lines:
        result = prog.match(word) # check if this word matches the regular expression
        if result:
            word = word.replace('\n', '') # if this word matches, eliminates the '\n' and put into res
            res.append(word)
    return res

def transform_reverse(str):
    reversed_str = ""
    for char in str:
        reversed_str = char + reversed_str # each time put char at the top
    return [str, reversed_str]

def transform_capitalize(string):
    res = []
    size = len(string) # get the length of the string
    for x in range(2**size): # use binary version of number to indicate which char needs to be capitalized
        helper = 1 # helper integer 00000001
        temp = list(string) # convert string to list so as to modify one specific char
        for times in range(size):
            if x & helper != 0: # if the certain position is "1", then we need to capitalize it
                cap = temp[size-1-times].upper()
                temp[size-1-times] = cap
            helper = helper << 1
        temp = "".join(temp) # convert list back to string and store it
        res.append(temp)
    return res

# create a dictionary from lowercase letters to set of digits
similar ={'o':set([0]), 'i':set([1]), 'l':set([1]), 'z':set([2]), 'e':set([3]),
'a':set([4]), 's':set([5]), 'b':set([6,8]), 't':set([7]), 'g':set([9]), 'q':set([9])}
def transform_digits(string):
    res = [string]
    size = len(string)
    for x in range(size): # for each letter, check if it has similar digits
        char = string[x].lower()
        cur_size = len(res)
        if char in similar: # if there are any similar digits, take 'em and substitute the original letter
            for i in range(cur_size):
                for t in similar[char]:
                    temp = list(res[i])
                    temp[x] = str(t)
                    temp = "".join(temp)
                    res.append(temp)
    return res

# Check to see if the plaintext plain encrypts to the encrypted
#    text enc
# Unix version
def check_pass(plain,enc):
    salt = enc[:2]
    hashed = crypt.crypt(plain, salt)
    return hashed == enc

# Windows version
# from passlib import hash
# def check_pass(plain,enc):
#     salt = enc[:2]
#     return hash.des_crypt.encrypt(plain,salt=salt) == enc

# Load the password file filename and returns a list of
#    dictionaries with fields "account", "password", "UID", "GID",
#    "GECOS", "directory", and "shell", each mapping to the
#    corresponding field of the file.
def load_passwd(filename):
    res = []
    f = open(filename, 'r')
    lines = f.readlines() # read info from file
    for line in lines:
        dic = {}
        line = line.split(':') # split every line by ':' and set info seperately
        dic['account'] = line[0]
        dic['password'] = line[1]
        dic['UID'] = line[2]
        dic['GID'] = line[3]
        dic['GECOS'] = line[4]
        dic['directory'] = line[5]
        dic['shell'] = line[6]
        res.append(dic)
    return res

# Crack as many passwords in file fn_pass as possible using words
#    in the file words
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
    # try combinations of digits and capitals
    for word in words:
        for new_word in transform_capitalize(word):
            for this_word in transform_digits(new_word):
                for pair in p2u:
                    if check_pass(this_word, pair):
                        output.write(p2u[pair] + "=" + this_word + '\n')
                        output.flush()
                    reversed_word = transform_reverse(this_word)[1]
                    if check_pass(reversed_word, pair):
                        output.write(p2u[pair] + "=" + reversed_word + '\n')
                        output.flush()
    output.close()
    return
