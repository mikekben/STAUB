FILE=$2
BOUNDED_FILE=$FILE-bounded.smt2
SLOT_FILE=$FILE-slot.smt2


if [ "$1" = "-int" ]; then
    ./staub -i aix -s $FILE -o $BOUNDED_FILE
else
    ./staub -r aix -s $FILE -o $BOUNDED_FILE
fi

#Run STAUB on the sample file


#Remove the unnecessary declarations of anti-overflow constraints
#This step is a workaround, since these constraints have not been added to SMT-LIB
sed -i '/declare-fun bvnego/d;/declare-fun bvsaddo/d;/declare-fun bvssubo/d;/declare-fun bvsmulo/d;/declare-fun bvsdivo/d' $BOUNDED_FILE

#Run Z3 on the original constraint
echo "Running Z3 on unbounded original ..."
#echo "   [expected output: sat, after several seconds]"
z3/build/z3 -T:10 -st $FILE | grep -E "^sat$|unsat|unknown|total-time"


#Run Z3 on the final constraint
echo "Running Z3 on transformed bounded constraint ..."
#echo "   [expected output: sat, faster than the unbounded form]"
z3/build/z3 -T:10 -st $BOUNDED_FILE | grep -E "^sat$|unsat|unknown|total-time"

#Run STAUB with SLOT
echo "Running SLOT on bounded constraint ..."
if [ "$1" = "-int" ]; then
    ./staub -l -i aix -s $FILE -o $FILE-temp.smt2
else
    ./staub -l -r 5,11 -s $FILE -o $FILE-temp.smt2
fi
sed -i '/declare-fun bvnego/d;/declare-fun bvsaddo/d;/declare-fun bvssubo/d;/declare-fun bvsmulo/d;/declare-fun bvsdivo/d' $FILE-temp.smt2
./slot -m -pall -s $FILE-temp.smt2 -o $SLOT_FILE
rm $FILE-temp.smt2

echo "Running Z3 on bounded constraint after SLOT application ..."
#echo "   [expected output: sat, with no change in running time]"
z3/build/z3 -T:10 -st $SLOT_FILE | grep -E "^sat$|unsat|unknown|total-time"


