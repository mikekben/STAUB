#find ./QF_NIA -type f -name '*-bv.smt2' -delete
#find ./QF_NIA -name '*.smt2' -type f | parallel ./runner-int.sh
#find ./QF_LIA -name '*.smt2' -type f | parallel -j 86 ./runthrough.sh
cat fp-slot-list.txt | parallel -j 64 ./runthrough-solver.sh

#find ./QF_LRA -name '*.smt2' -type f | parallel -j 86 ./runthrough.sh
#find ./QF_NRA -name '*.smt2' -type f | parallel -j 86 ./runthrough.sh




#find ./QF_LIAxt -name '*.smt2' -type f | parallel -j 86 ./runner-int.sh
#find ./QF_NIAxt -name '*.smt2' -type f | parallel -j 86 ./runner-int.sh

#find ./QF_LRAxt -name '*.smt2' -type f | parallel -j 86 ./runner-real.sh
#find ./QF_NRAxt -name '*.smt2' -type f | parallel -j 86 ./runner-real.sh


#find ./QF_NRA -name '*.smt2' -type f | parallel ./runner-real.sh
#find ./QF_LRA -name '*.smt2' -type f | parallel ./runner-real.sh
#cat sorted_pre.csv | parallel ./wrapper.sh


#awk -F "\"*,\"*" '{print $1}' bv-errors.csv | parallel ./wrapper.sh >> bv-error-results.csv

#awk -F "\"*,\"*" '{print $1}' bv-errors.csv | parallel ./dd-sftest.sh >> is_segfault.txt
