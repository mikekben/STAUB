#!/bin/bash
Z3=/nethome/bmikek3/z3/build/z3
BOOLECTOR=/nethome/bmikek3/boolector/build/bin/boolector
CVC5=/nethome/bmikek3/cvc5/build/bin/cvc5

TIMEOUT=300
MEMORY_LIMIT=10000

FILE=$1


#SLOT_OUT=$( { /usr/bin/time -f "tmr%e" timeout $TIMEOUT ./main -r aix -s $FILE -o $FILE-aix.smt2 -t nra-slot-stats.csv; } 2>&1 > /dev/null )
#if [[ $? == 124 ]]
#then
#    SLOT_GOOD=false
#    SLOT_TIME=$TIMEOUT
#else
#    SLOT_TIME=$(echo "$SLOT_OUT" | grep -Po 'tmr*.*' | tr -dc '.0-9')
#fi


#Z3----------------
PRE_SOL_OUT=$( { /usr/bin/time -f "tmr%e" $Z3 $FILE-slot.smt2 -T:$TIMEOUT -model > $FILE-slot-z3.smt2; } 2>&1 )
if [[ "$PRE_SOL_OUT" == "timeout" ]]
then
    Z3_TIME=$TIMEOUT
else
    Z3_TIME=$(echo "$PRE_SOL_OUT" | grep -Po 'tmr*.*' | tr -dc '.0-9')
fi



CV_OUT=$( { /usr/bin/time -f "tmr%e" $CVC5 $FILE-slot.smt2 -q  --tlimit=$(( 1000 * TIMEOUT )) --fp-exp --dump-models > $FILE-slot-cvc.smt2; } 2>&1 )
if [[ "$CV_OUT" == *"timeout"* ]]
then
    CV_TIME=$TIMEOUT
else
    CV_TIME=$(echo "$CV_OUT" | grep -Po 'tmr*.*' | tr -dc '.0-9')
fi


#echo "$FILE,$Z3_RESULT,$Z3_TIME,$CV_RESULT,$CV_TIME,$BL_RESULT,$BL_TIME"
echo "$FILE,$Z3_TIME,$CV_TIME" >> fp-slot-solver-times.csv