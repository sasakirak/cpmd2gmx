import argparse
import os

# This script convert gro to cpmd

parser = argparse.ArgumentParser()
parser.add_argument('-p',help='gromacs .top file') ; parser.add_argument('-f',help='gromacs .gro file')
args = parser.parse_args()

topfile = args.p
grofile = args.f

with open("g2c_temp.mdp",mode='w') as f:
    f.write("integrator              = steep\n")
    f.write("nsteps                  = 0\n")
    f.write("emtol                   = 100.0\n")
    f.write("emstep                  = 0.01\n")
    f.write("pbc                     = xyz\n")
    f.write("coulombtype             = Cut-off \n")
    f.write("rcoulomb                = 0.01\n")
    f.write("vdwtype                 = Cut-off\n")
    f.write("rvdw                    = 0.01\n")

os.system("gmx grompp -f g2c_temp.mdp -p "+ topfile + " -c " + grofile + " -o " + "g2c_temp.tpr")

tprfile = "g2c_temp.tpr"

os.system("gmx make_ndx -f "+ tprfile + "<<EOF > resname.log   \n l \n q \n EOF")



with open("resname.log") as f:
    lines = f.readlines()
    molline = lines[len(lines)-3]
    numline = lines[len(lines)-13]
    num_index = str(int(numline.split()[0]) + 1)
    print(num_index)
    mol = []
    for i in range(int(len(molline.split())/4)):
        mol.append(molline.split()[4*i+3])

atomtype = [[] for i in range(len(mol))]

with open(topfile) as f:
    lines = f.readlines()
    mol_i = 0
    flag_atomtypes = 0
    for i in range(len(lines)):
        if mol_i == len(mol) and flag_atomtypes == 0:
            exit
        elif lines[i] == "\n" or lines[i][0] == ";":
            pass
        elif lines[i].strip() == "[ atomtypes ]":
            mol_i = mol_i + 1
            flag_atomtypes = 1
        elif lines[i].split()[0] == "[":
            flag_atomtypes = 0
        elif flag_atomtypes == 1:
            atomtype[mol_i-1].append(lines[i].split()[0])

print(mol)
print(atomtype)

with open("cpmd.in",mode='w') as f:
    print("Creating cpmd input file")

with open("indexlist.dat",mode='w') as f:
    print("")

os.system("rm -r temp_cpmd ; mkdir temp_cpmd")

for i in range(len(mol)):
    for j in range(len(atomtype[i])):
        molatom = mol[i] + "_" + atomtype[i][j] 
        makendx = "gmx make_ndx -f " + tprfile + " -o " + molatom +".ndx" + "<<EOF \n"+"r " + mol[i] + " & t " + atomtype[i][j] + " \nq\nEOF"
        # print(makendx)
        os.system(makendx)

        trjconv = "echo " + num_index + " | gmx trjconv -f "+ grofile + " -s " + tprfile + " -n " + molatom + ".ndx" + " -pbc mol -o " + molatom +".gro"
        os.system(trjconv)

        obabel = "obabel -igro " + mol[i] + "_" + atomtype[i][j] +".gro -O " + mol[i] + "_" + atomtype[i][j] +".xyz"
        os.system(obabel)
        with open(mol[i]+"_"+atomtype[i][j]+".xyz") as f:
            lines = f.readlines()
        with open("cpmd.in",mode='a') as f:
            f.write("*"+lines[2].split()[0]+"_SG_PBE.psp \n")
            f.write("   "+"LMAX= \n")
            f.write("   "+lines[0])
            for p in range(2,len(lines)):
                f.write("{:12.5f}".format(float(lines[p].split()[1]))+"{:12.5f}".format(float(lines[p].split()[2]))+"{:12.5f}".format(float(lines[p].split()[3]))+"\n")
        
        with open(molatom+".ndx") as f:
            lines = f.readlines()
            flag = 0
            sel_index = []
            for p in range(len(lines)):
                if lines[p] == "\n":
                    pass
                elif lines[p].split()[0] == "[":
                    flag = flag + 1
                elif flag == int(num_index)+1:
                    for q in range(len(lines[p].split())):
                        sel_index.append(lines[p].split()[q])
        print(sel_index)
        with open("indexlist.dat",mode='a') as f:
            for p in range(len(sel_index)):
                f.write(sel_index[p]+"\n")
        os.system("mv "+molatom+"*  temp_cpmd")
os.system("rm resname.log index.ndx g2c_temp.tpr g2c_temp.top g2c_temp.mdp  mdout.mdp")
