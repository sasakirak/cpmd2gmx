# cpmd2gro gro2cpmd
Preliminary converter between GROMACS and CPMD format
<br>
<br>

## 環境構築 (by anaconda)
### anaconda install
1. [anacondaの公式サイト](https://www.anaconda.com/products/individual)から、command line installerをダウンロード
1. Installerの実行
    ```
    $ bash ./Anaconda3-2021.05-MacOSX-x86_64.sh
    ```
    指示にしたがってInstall    


### Package install
1. GROMACS  
    ```
    conda install -c bioconda gromacs
    ```
1. Openbabel  
    ```
    $ conda install -c conda-forge openbabel
    $ obabel -V
    Open Babel 3.1.0 -- May  8 2020 -- 19:21:06
    ``` 

## Usage
#### GROMACS &rarr; CPMD
```
python3 gro2cpmd.py -p hoge.top -f fuga.gro
```
*Output file*
- cpmd.in  
    Force Fieldのassignmentに基づいた原子ごとのxyz coordinate.
- indexlist.dat  
    .groでの原子のindex <-> cpmd.inでの原子のindex. 行数が.groのindexに相当、i行目の数字がcpmd.inに変換したときのindex.

#### CPMD &rarr; GROMACS
```
python3 cpmd2gro.py -p hoge.top -f fuga.gro -c cpmd.xyz -dt [Timestep of trajectory] -cell Lx Ly Lz
```

## 補足
AMBERを使ってる場合は、AntechamberのparmedでAMBER&rarr;GROMACSの変換ができる。  
(参考: https://github.com/ParmEd/ParmEd)
```
import parmed as pmd

# convert GROMACS topology to AMBER format
gmx_top = pmd.load_file('pmaawaterFE20mer2.top', xyz='pmaawaterFE20mer2.gro')
gmx_top.save('pmaa.top', format='amber')
gmx_top.save('pmaa.crd', format='rst7')
```

