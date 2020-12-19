#!/usr/bin/python3
import string
import sys


dict_dest = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}
dict_jump = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

dict_comp_0 = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '110000',
    '!D': '001101',
    '!A': '110001',
    '-D': '001111',
    '-A': '110011',
    'D+1': '011111',
    'A+1': '110111',
    'D-1': '001110',
    'A-1': '110010',
    'D+A': '000010',
    'D-A': '010011',
    'A-D': '000111',
    'D&A': '000000',
    'D|A': '010101',
}

dict_comp_1 = {
    'M': '110000',
    '!M': '110001',
    '-M': '110011',
    'M+1': '110111',
    'M-1': '110010',
    'D+M': '000010',
    'D-M': '010011',
    'M-D': '000111',
    'D&M': '000000',
    'D|M': '010101'
}

symbol_dict = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4
}

def get_symbols(file):
    i = 0
    for line in file:
        if  line.find('@') >=0 or line.find(';') >=0 or line.find('=') >= 0:
            i+=1
        start = line.find('(')
        if start >= 0 :
            res = line[start+1:line.find(')')]
            symbol_dict[res] = i




def get_variables(file):
    ram = 16
    for line in file:
        start = line.find('@')
        if start >= 0:
            res = line[start+1:]
            if not res.isdigit() and symbol_dict.get(res) < 0:
                symbol_dict[res] = ram
                ram+=1

def get_symbol(sym):
    res = symbol_dict.get(sym, -1)
    if res < 0:
        return int(sym)
    else:
        return res



def c_handle(line):
    res = "111"
    dest_ind = line.find("=") 
    if dest_ind < 0:
        dest = "0"*3
        dest_ind = -1
    else:
        dest = dict_dest[line[:dest_ind]]

    jump_ind = line.find(";") 
    if jump_ind < 0:
        jump = "0"*3
        jump_ind = len(line)
    else:
        jump = dict_jump[line[jump_ind+1:]]
    
    comp = dict_comp_0.get(line[dest_ind+1:jump_ind], -1)
    if  comp >= 0:
        comp = '0' + comp
    else:
        comp = dict_comp_1.get(line[dest_ind+1:jump_ind], -1)
        if comp > 0 :
            comp = '1' + comp
        else:
            comp = "0"*7

    res = res + comp + dest + jump
    return res

def a_handle(line):
    #print("a_handle: "+line)
    return "0" + '{:015b}'.format(get_symbol(line))

def convert(line):
    if line.find("=") >=0 or line.find(";") >=0:
        return c_handle(line)
    elif "@" in line:
        return a_handle(line[1:])
    return ""

def remove_junk(line):
    line = line[:line.find('//')]
    line = line.replace(' ','')
    line = line.replace('\n','')
    line = line.replace('\t','')
    line = line.replace('\r','')


    return line


def translate(asm, hack):
    for line in asm:
        line = convert(line)
        if len(line) > 0:
            #print(line)
            hack.write(line + '\n')

def parse(asm):
    i = 0
    arr = []
    for line in asm:
        line = remove_junk(line)
        arr.append(line)
        i+=1
    return arr

def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        if file[len(file) - 4:] != ".asm":
            print("File format incorrect")
            sys.exit()
        asm = open(file , "r")
        hack = open(file[:len(file) - 4] + ".hack" , "w+")
    else:
        print("Usage: python Assembler.py <filename.asm>")
        sys.exit()
    arr = parse(asm)
    get_symbols(arr)
    get_variables(arr)
    translate(arr, hack)
    asm.close()
    hack.close()

if __name__ == "__main__":
  main()