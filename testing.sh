#!/bin/bash
for i in `seq 2 12`;
  do
    time mpiexec -n $i python solver_launcher.py $1
  done
echo Done testing distributed solver, moving to local
time python solve_local.py $1
