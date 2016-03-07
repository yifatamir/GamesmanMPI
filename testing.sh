#!/bin/bash
echo Beginning testing for $1 from $2 to $3 > tests/time_results.txt
echo Beginning testing for $1 from $2 to $3 > tests/solve_results.txt
SYM="#"
for i in `seq $2 $3`;
  do
    prog=""
    for j in `seq $2 $i`;
      do
        prog=$prog$SYM
      done
    echo -ne "$prog\r"
    echo -ne "\n" >> tests/time_results.txt
    echo -ne "\n" >> tests/solve_results.txt
    echo Testing with $i processes >> tests/time_results.txt
    echo Testing with $i processes >> tests/solve_results.txt
    echo --------- >> tests/time_results.txt
    echo --------- >> tests/solve_results.txt
    (time mpiexec -n $i python solver_launcher.py $1) >> tests/solve_results.txt 2>> tests/time_results.txt
  done
echo Done testing distributed solver

if [ "$4" = "-l" ]; then
  echo Testing with local solver
  echo -ne "\n" >> tests/time_results.txt
  echo -ne "\n" >> tests/solve_results.txt
  echo Testing with local, non-distributed solver >> tests/time_results.txt
  echo Testing with local, non-distributed solver >> tests/solve_results.txt
  echo --------- >> tests/time_results.txt
  echo --------- >> tests/solve_results.txt
  (time python solve_local.py $1) >> tests/solve_results.txt 2>> tests/time_results.txt

fi
echo Done with all tests
