#!/bin/bash
for i in `seq $2 $3`;
  do
    echo Testing with $i processes
    time mpiexec -n $i python solver_launcher.py $1
  done
echo Done testing distributed solver

if [ "$4" = "-l" ]; then
  echo Testing with local, non-distributed solver
  time python solve_local.py $1
fi
