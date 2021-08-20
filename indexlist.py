import argparse
import os

# This script convert gro to cpmd

parser = argparse.ArgumentParser()
parser.add_argument('-i',nargs='*',help='1111.ndx  222.ndx   333.ndx .....') 
parser.add_argument('-n_ind',help='number of [ mol_atom ]')
args = parser.parse_args()
ndxfile = args.i
num_index = args.n_ind

for i in range(len(ndxfile)):
    with open(ndxfile[i]) as f:
        lines = f.readlines()
        flag = 0
        sel_index = []
        for p in range(len(lines)):
            if lines[p] == "\n":
                pass
            elif lines[p].split()[0] == "[":
                flag = flag + 1
            elif flag == int(num_index):
                for q in range(len(lines[p].split())):
                    sel_index.append(lines[p].split()[q])
    with open("indexlist.dat",mode='a') as f:
        for p in range(len(sel_index)):
            f.write(sel_index[p]+"\n")

