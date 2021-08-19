#!/Users/sasaki/anaconda3/bin/python3
import argparse
import os
from pathlib import Path

# This script align cpmd .xyz file

parser = argparse.ArgumentParser()
parser.add_argument('-i',help='gromacs index list')
parser.add_argument('-f',help='CPMD .xyz file')
parser.add_argument('-p',help='gromacs .top file')
parser.add_argument('-c',help='gromacs .gro file')
parser.add_argument('-box',nargs=3,default=[100,100,100],help='cell length Lx Ly Lz (A)')
parser.add_argument('-dt',help='time step between input frames (fs)',default=0.1)
args = parser.parse_args()
indlistfile = args.i
cpmdxyz = args.f
topfile = args.p
grofile = args.c

cellinfo = [str(float(i)/10) for i in args.box]
timestep = str(args.dt)

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



with open(indlistfile) as f:
    indlist = f.readlines()

with open(cpmdxyz) as f:
    traj = f.readlines()

convtrj = []
i = 0
while i < len(traj):
    num_atom = int(traj[i]) ; convtrj.append(traj[i]) ; i = i + 1
    convtrj.append(traj[i]) ; i = i + 1 ; beg_coord_i = i
    for atom_i in range(1,num_atom+1):
        convtrj.append(traj[indlist.index(str(atom_i)+"\n")+beg_coord_i])
        i = i + 1

with open(Path(cpmdxyz).stem+"_temp.xyz",mode='w') as f:
    for i in range(len(convtrj)):
        f.write(convtrj[i])

os.system("obabel -ixyz "+Path(cpmdxyz).stem+"_temp.xyz -O "+Path(cpmdxyz).stem+"_temp.gro")

os.system("echo 0 | gmx trjconv -f "+Path(cpmdxyz).stem+"_temp.gro -s "+tprfile+" -pbc mol -box "+cellinfo[0]+" "+cellinfo[1]+" "+cellinfo[2]+" -tu fs -timestep "+timestep+" -o "+Path(cpmdxyz).stem+".gro")

os.system("rm "+Path(cpmdxyz).stem+"_temp.gro "+Path(cpmdxyz).stem+"_temp.xyz"+ "  g2c_temp.mdp  g2c_temp.tpr mdout.mdp")
