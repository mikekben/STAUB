#!/bin/bash
Z3=/nethome/bmikek3/z3/build/z3
BOOLECTOR=/nethome/bmikek3/boolector/build/bin/boolector
CVC5=/nethome/bmikek3/cvc5/build/bin/cvc5

TIMEOUT=60
MEMORY_LIMIT=10000

FILE=$1


SLOT_OUT=$( { /usr/bin/time -f "tmr%e" timeout $TIMEOUT ./main -r 15,113 -s $FILE -o $FILE-128.smt2 -t fp-stats.csv; } 2>&1 > /dev/null )
if [[ $? == 124 ]]
then
    SLOT_GOOD=false
    SLOT_TIME=$TIMEOUT
else
    SLOT_TIME=$(echo "$SLOT_OUT" | grep -Po 'tmr*.*' | tr -dc '.0-9')
fi

#echo "$FILE,$Z3_RESULT,$Z3_TIME,$CV_RESULT,$CV_TIME,$BL_RESULT,$BL_TIME"
echo "$FILE,$SLOT_TIME" >> fp-times.csv