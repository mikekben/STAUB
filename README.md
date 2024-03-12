# STAUB Readme

## Getting Started

STAUB (SMT Theory Arbitrage, from Unbounded to Bounded) speeds up SMT solving of unbounded constraints by converting them to a bounded theory. For ease of use, we provide a pre-built Docker image for testing, and at the end of this file include instructions for a local build, if necessary. We strongly recommend using the Docker image, since building using the dockerfile involves a fresh build of LLVM, which may be time consuming.

To perform simple tests:

+ Run the docker image from https://hub.docker.com/repository/docker/mikekben/staub in interactive mode:
```
docker run -it mikekben/staub
```
Docker should pull the necessary docker image from Dockerhub with the above command, but you may also pull it using `docker pull mikekben/staub`

+ Run STAUB on a sample input using the provided script (this may take up to 1-2 minutes, depending on hardware):
```
./run-sample.sh -int samples/motivating.smt2
-int
doing!
samples/motivating.smt2,integer,855,8551462050,23,
Running Z3 on unbounded original ...
sat
 :total-time              27.94)
Running Z3 on transformed bounded constraint ...
sat
 :total-time              1.22)
Running SLOT on bounded constraint ...
samples/motivating.smt2,integer,855,8551462050,23,
samples/motivating.smt2-temp.smt2,true,1,1,1,1,1,1,1,1,0.0298969,0.00441312,0.00536189,0,0,0,0,0,0,0,0
Running Z3 on bounded constraint after SLOT application ...
sat
 :total-time              0.14)

```
The observed absolute running times may vary across different hardware, but as long as the output matches the form above (and, in particular, the second and third solver runs take substantially less time than the first), STAUB has run correctly, and you have also verified that SLOT runs correctly on your system.

+ Inspect ``samples/motivating.smt2-bounded.smt2`` to see that the transformation has taken place:
```
cat samples/motivating.smt2-bounded.smt2
```
The contents of the file should match in substance that shown in Figure 1b of the submitted paper (note that several anti-overflow constraints have been omitted in the submitted paper, and a let expression simplified for ease of presentation).

If all three steps listed above execute correctly, then STAUB runs as expected on your system and you should have no technical difficulties with the rest of the artifact.



## Step-by-Step Instructions

This step-by-step guide is organized in two parts. The experiments embodied in the submitted paper invove runs of more than 100,000 SMT constraints, which took more than one week of running time on a server with 512 GB memory using 64 cores. Since it would be impractical to re-run the entire set of experiments during artifact evaluation, we provide here a guide for replicating our results on small examples to support the functionality of the submitted artifact source. This demonstrates each of the claims made in the paper on smaller examples. In addition, we provide the raw data generated during our experimental runs, and the analysis script used to generate the tables and graphs in the submitted paper.

The source code of STAUB is provided in ``src``, including a makefile to build the binary (we provide a pre-built binary in the docker container as well). The source code is C++, using the Z3 API to parse and write SMT constraints. We use LLVM's APInt and APFloat libraries during abstract interpretation, thus the docker container includes a custom build of LLVM to support these libraries, and SLOT. STAUB's source code includes comments and clear naming conventions to facilitate modification, reuse, and adaptation in future research.

Running ``./staub -h`` produces a help menu which documents STAUB's terminal options. The examples below show how these options are used.



### List of claims directly supported through reproduction:
+ The motivating example, Figure 1. In particular:
  + STAUB produces the constraint in Figure 1b when given the constraint in Figure 1a as input. 
  + The constraint in Figure 1a takes substantially longer for Z3 to solve than the constraint in Figure 1b. 
  + The constraint in Figure 1c takes approximately the same amount of time as Figure 1a.

### List of claims supported by smaller examples and raw experimental data:
+ Table 2: Constraints with larger widths take longer to solve, but are more likely to be correct.
+ Table 3: STAUB achieves tractability improvements.
+ Figure 6 and Table 4: STAUB speeds up constraints as shown in the figures and table; moreover, it unlocks further speedup from the related work SLOT.
+ Figure 7: STAUB speeds up constraints from the Ultimate Automizer client analysis.

### Setup

No further setup is required beyond that described in the Getting Started guide; simply run the referenced docker image in interactive mode:

```
docker run -it mikekben/staub
```

### Motivating example:
The motivating example in the submitted paper is given in Figure 1. Figure 1a gives a constraint taken from the SMT-LIB benchmark set for nonlinear integer arithmetic; this constraint is in ``samples/motivating.smt2`` (this is benchmark ``QF_NIA/20220315-MathProblems/STC_0855.smt2`` in the SMT-LIB benchmark set, which can be obtained from https://clc-gitlab.cs.uiowa.edu:2443/SMT-LIB-benchmarks/QF_NIA).

**Claim 1**: STAUB produces the constraint in Figure 1b when given the constraint in Figure 1a as input.

Run STAUB on the example:
```
./staub -i 12 -s samples/motivating.smt2 -o samples/motivating-bounded.smt2
```
Then the file ``samples/motivating-bounded.smt2`` should match Figure 1b in the paper, modulo let expressions. Note that, as described in the caption of Figure 1b, some anti-overflow constraints are omitted in the paper for space; these are included in the full STAUB output. In addition, automatically generated constraints typically include many let bindings, which we have simplified for presentation in Figure 1b. The substance of the constraints (three multiplications added together) should match.

**Claim 2**: The constraint in Figure 1a takes substantially longer for Z3 to solve than the constraint in Figure 1b.

Run Z3 on the original constraint (the -st flag collects statistics about the Z3 run):
```
z3 -st samples/motivating.smt2
```
Run Z3 on the new bounded constraint (Note: as documented in Footnote 3 of the paper, the anti-overflow predicates bvsaddo, bvsmulo, etc. are supported by Z3 but not yet incorporated into the SMT-LIB standard. The below sed command is therefore a temporary workaround to remove the *declarations* of these functions from the constraint, but not their applications):
```
sed -i '/declare-fun bvnego/d;/declare-fun bvsaddo/d;/declare-fun bvssubo/d;/declare-fun bvsmulo/d;/declare-fun bvsdivo/d' samples/motivating-bounded.smt2
z3 -st samples/motivating-bounded.smt2
```

The second run of Z3 should be much faster than the first. SMT solving times vary widely based on hardware, the use of docker, memory availability, and caching, so absolute solving times may differ from machine to machine. However, in all cases, the bounded constraint should take much less time to solve than the first, as documented in the paper.

**Claim 3**: The constraint in Figure 1c takes approximately the same amount of time as Figure 1a.

The constraint in Figure 1c is manually constructed to provide motivation; that constraint is contained in ``/samples/motivating-manually-bounded.smt2``. Run Z3 on this constraint:

```
z3 -st samples/motivating-manually-bounded.smt2
```
This constraint should also take much longer to solve than that produced by STAUB.

### Table 2: Constraints with larger widths take longer to solve, but are more likely to be correct.

**Small example**: Run the example given above with two different fixed widths, and compare the running time as below:

```
./staub -i 16 -s samples/motivating.smt2 -o samples/motivating-16.smt2
sed -i '/declare-fun bvnego/d;/declare-fun bvsaddo/d;/declare-fun bvssubo/d;/declare-fun bvsmulo/d;/declare-fun bvsdivo/d' samples/motivating-16.smt2
z3 -st samples/motivating-16.smt2
```

```
./staub -i 128 -s samples/motivating.smt2 -o samples/motivating-128.smt2
sed -i '/declare-fun bvnego/d;/declare-fun bvsaddo/d;/declare-fun bvssubo/d;/declare-fun bvsmulo/d;/declare-fun bvsdivo/d' samples/motivating-128.smt2
z3 -T:60 -st samples/motivating-128.smt2
```
The expected outcome is that the second, with a 128-bit width, takes longer to solve than the first, with a 16-bit width. Now, if we set the width to 8 bits, the bounded constraint becomes unsatisfiable, which is incorrect:
```
./staub -i 8 -s samples/motivating.smt2 -o samples/motivating-8.smt2
sed -i '/declare-fun bvnego/d;/declare-fun bvsaddo/d;/declare-fun bvssubo/d;/declare-fun bvsmulo/d;/declare-fun bvsdivo/d' samples/motivating-8.smt2
z3 -st samples/motivating-8.smt2
```

**Experimental data**: The raw data used to generate Table 2 is provided in ``data/fixed-width``. File ``uni-list.txt`` contains a random sample of programs from the SMT-LIB benchmark set, 500 from each logic. The files ``uni-res-<N>.csv`` store the solving times using Z3 *after transformation* for each benchmark, while ``solver-res.csv`` contains the original solving times. File ``analysis.py`` is a script to analyze the collected data.

To replicate Table 2, run:
```
cd data/fixed-width
python3 analysis.py
```
The output is in the form of three tables, one for each width; these have been consolidated into one table in the submitted paper.


### Table 3: STAUB achieves tractability improvements.

**Small example**: Run STAUB on ``samples/timeout.smt2`` (A copy of ``QF_NIA/20170427-VeryMax/CInteger/Ton_Chanh_15__Hanoi_3vars_false-termination.c__p26981_terminationG_0.smt2`` from the benchmark set); before the transformation this constraint times out, while after, it is solved in under 1 second. Note that we here use a timeout of 60 seconds to speed up evaluation, but in our testing, the constraint did not finish within 300 seconds, as reported in the submitted paper. You can set a higher timeout, time permitting.

```
z3 -T:60 -st samples/timeout.smt2

./staub -i aix -s samples/timeout.smt2 -o samples/timeout-bounded.smt2
sed -i '/declare-fun bvnego/d;/declare-fun bvsaddo/d;/declare-fun bvssubo/d;/declare-fun bvsmulo/d;/declare-fun bvsdivo/d' samples/timeout-bounded.smt2
z3 -T:60 -st samples/timeout-bounded.smt2
```

**Experimental data**: See below; Table 3, Figure 6, Table 4, and Figure 7 are all supported by the same underlying data, analyzed in the last subsection.

### Figure 6 and Table 4: STAUB speeds up constraints as shown in the figures and table; moreover, it unlocks further speedup from the related work SLOT.

**Small example**: The data presented in Figure 6 and Table 4 are supported by the two examples already provided. To run these examples with SLOT, you can use the provided ``run-sample.sh`` script:

```
./run-sample.sh -int samples/motivating.smt2
```
In addition, we provide a real number example to demonstrate STAUB's ability to transform constraints over real numbers (``samples/nra.smt2`` is the benchmark ``QF_NRA/zankl/matrix-2-all-8.smt2``). Note that, as documented in the paper, because SLOT only supports 4 fixed floating point widths, the script rounds up to a 16-bit floating point value for use with SLOT.
```
./run-sample.sh -real samples/nra.smt2
```

**Experimental data**: See below; Table 3, Figure 6, Table 4, and Figure 7 are all supported by the same underlying data, analyzed in the last subsection.


### Figure 7: STAUB speeds up constraints from the Ultimate Automizer client analysis.

**Small example**: Again, we can use the ``run-sample.sh`` script to test a small example for the Ultimate Automizer:

```
./run-sample.sh -int samples/ultimate.smt2
```


**Experimental data**: To produce Table 3, Figure 6, and Table 4, we ran STAUB (and the existing tool SLOT, in the case of Table 4) on the entire SMT-LIB benchmark set, using both Z3 and CVC5. The benchmark sets for each logic are publicly available from https://smtlib.cs.uiowa.edu/benchmarks.shtml, and at the end of this readme, we provide additional instructions on how to re-run large scale experiments. In the case of Table 7, we run STAUB on constraints produced by the Ultimate Automizer. As documented in Section 5.4, we use benchmarks from the SV-COMP (https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks) as the source programs for the Ultimate Automizer, and then run STAUB rather than a vanilla solver on its constraints. As noted in the submitted paper, we restrict our consideration to the 97 cases for which Ultimate does not produce constraints with arrays, since STAUB does not support arrays We provide the raw data collected during our experimental runs in ``/data/experiments``. The files are organized as follows, with a copy for each of the 4 logics:

+ ``pre-<logic>.csv`` gives the time taken to solve each benchmark in original form (control experiments); the columns represent NAME, Z3, CVC5.
+ ``<logic>-tool-times.csv`` gives the amount of time spent to run STAUB on each benchmark. This time is offset against any speedup.
+ + ``<logic>-tool-stats.csv`` gives some diagnostic outputs of STAUB for each benchmark; the columns represent integer/real, the largest constant, the largest possible computation value, and the width produced by abstract interpretation (as documented in Section 4). This data is not directly used in the tables in the paper.
+ ``<logic>-check-results.csv`` includes the verification results as described in Section 4.4.
+ ``<logic>-solver-times.csv`` gives the running time of each solver (the columns are in the order NAME, Z3, CVC5) after STAUB has been applied.
+ ``<logic>-slot-stats.csv`` gives SLOT's running statistics for each benchmark. Only columns 9-11 are used, to compute SLOT's running time on the benchmark, and offset it against the overall speedup.
+ ``<logic>-slot-solver-times.csv`` gives the solving time of each benchmark *after* the application of SLOT. Note that SLOT is only useful for the verified constraints.
+ ``ultimate-res.csv`` gives the results of the Ultimate benchmark tests; the columns are in the order name, running time, result, pre solver time, post solver time, verification result (1 for verified, 0 for not verified)

We provide the analysis script ``anlaysis.py`` which analyzes all of the collected data. The script takes an argument for which logic to analyze (`nia`, `lia`, `nra`, `lra`) as below:
```
cd data/experiments
python3 analysis.py -t nia
```

The first three lines of the output reproduce the results in Table 3; note that Table 3 is amalgamated from all four logics. Next, the script outputs the rows of Table 4 corresponding to the selected theory; again, Table 4 consists of combining the results for all four logics. The script also produces images (two for each logic), ``data/experiments/plots/scatter-<logic>-<solver>.png``, which replicate Figure 6. Finally, the last output in the nia case is Table 7, an analysis of ``ultimate-res.csv``.







## Additional information: Re-running large scale experiments 

Re-running the large scale experiments embodied in the data directory of this repository requires a fresh build of STAUB, and takes more than 1 week on server-level hardware. We therefore understand that it is impractical during artifact evaluation; however, we provide here instructions for use by future researchers.

First, clone the four benchmark sets from SMTLIB. **Note that some constraints require Git LFS**.
```
git clone https://clc-gitlab.cs.uiowa.edu:2443/SMT-LIB-benchmarks/QF_NIA
git clone https://clc-gitlab.cs.uiowa.edu:2443/SMT-LIB-benchmarks/QF_LIA
git clone https://clc-gitlab.cs.uiowa.edu:2443/SMT-LIB-benchmarks/QF_NRA
git clone https://clc-gitlab.cs.uiowa.edu:2443/SMT-LIB-benchmarks/QF_LRA
```

Then, builds of both Z3 and LLVM are required to build STAUB.  LLVM can be built using the instructions here: https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm. Z3 can be built according to the instructions located here: https://github.com/Z3Prover/z3. In addition, if you wish to test with CVC5 as well, that solver can be built by following the instructions here: https://github.com/cvc5/cvc5. Note that building LLVM can take several hours and has substantial memory requirements, depending on machine hardware.

In ``data/experiments`, we have included several shell scripts used for large scale testing. The first step is to produce lists of files from each benchmark set:

```
find ./QF_NIA -name '*.smt2' -type f >> list-nia.txt
```
Then, use the ``test-all.sh`` script to run, in order
+ ``runthrough-solver.sh`` on the plain benchmarks (without any STAUB transformation)
+ ``runthrough-tool.sh`` to apply STAUB to each benchmark
+ ``runthrough-solver.sh`` on each transformed benchmark (after STAUB has been applied)
+ ``runthrough-checker.sh`` to verify the results for each benchmark
+ ``runthrough-slot.sh`` on only the verificed benchmarks (creating an intermediate list is recommended), to apply SLOT
+ ``runthrough-solver.sh`` again on each transformed benchmark (after SLOT has been applied)

The results can then be collated into single data files for use with ``analysis.py``. Tuning the number of threads in ``test-all.sh`` may be required, depending on hardware and available memory. SMT solving has substantial memory requirements. During our experiments running with 64 threads on a server, memory usage never exceeded ~400 GB.