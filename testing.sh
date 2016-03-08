#!/bin/bash
echo Beginning testing for $1 from $2 to $3 > tests/time_results.txt
echo Beginning testing for $1 from $2 to $3 > tests/solve_results.txt
TOTAL=`expr $3 - $2`
for i in `seq $2 $3`;
  do
    step=`expr $i - $2`
    sp=`expr $step \* 100`
    percent=$((sp / TOTAL))
    pc=$((percent / 5))

    echo -ne "$percent%\r"
    echo -ne "\n" >> tests/time_results.txt
    echo -ne "\n" >> tests/solve_results.txt
    echo Testing with $i processes >> tests/time_results.txt
    echo Testing with $i processes >> tests/solve_results.txt
    echo --------- >> tests/time_results.txt
    echo --------- >> tests/solve_results.txt
    if [[ "$4" = "-np" || "$5" = "-np" ]]; then
      (time mpiexec -n $i python solver_launcher.py $1 -np) >> tests/solve_results.txt 2>> tests/time_results.txt
    else
      (time mpiexec -n $i python solver_launcher.py $1) >> tests/solve_results.txt 2>> tests/time_results.txt
    fi
  done
echo Done testing distributed solver

if [[ "$4" = "-l" || "$5" = "-l" ]]; then
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
