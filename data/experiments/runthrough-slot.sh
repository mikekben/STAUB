#!/bin/bash
Z3=/nethome/bmikek3/z3/build/z3
BOOLECTOR=/nethome/bmikek3/boolector/build/bin/boolector
CVC5=/nethome/bmikek3/cvc5/build/bin/cvc5

TIMEOUT=300
MEMORY_LIMIT=10000

FILE=$1
STATS="fp-slot-stats.csv"


SLOT_OUT=$( { /usr/bin/time -f "tmr%e" timeout $TIMEOUT ./slot -m -pall -s $FILE-alo.smt2 -o $FILE-slot.smt2 -t $STATS; } 2>&1 > /dev/null )
if [[ $? == 124 ]]
then
    echo "$FILE,Timeout" >> $STATS
fi


#SLOT_OUT=$( { /usr/bin/time -f "tmr%e" timeout $TIMEOUT ./main -r aix -s $FILE -o $FILE-aix.smt2 -t nra-slot-stats.csv; } 2>&1 > /dev/null )
#if [[ $? == 124 ]]
#then
#    SLOT_GOOD=false
#    SLOT_TIME=$TIMEOUT
#else
#    SLOT_TIME=$(echo "$SLOT_OUT" | grep -Po 'tmr*.*' | tr -dc '.0-9')
#fi



#echo "$FILE,$Z3_RESULT,$Z3_TIME,$CV_RESULT,$CV_TIME,$BL_RESULT,$BL_TIME"
#echo "$FILE,$Z3_TIME,$CV_TIME" >> lra-solver-times.csv