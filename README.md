# Naive Floorplanner

This is an example of a simple floorplanning algorithm for FPGA designs written in python.
It is meant to be a starting point for more complex algorithms to be developed in the context
of the [RAW Floorplanning Design Contest](http://raw-floorplanning-contest.necst.it/).

In order to run the floorplanner you need python version 2.7 or 3.x installed in your system.
To execute the floorplanner run:

```shell
python floorplan.py < problems/10001.txt > solutions/10001.txt
```

This command will read the problem file *problems/10001.txt*, compute the floorplan and store the solution in *solutions/10001.txt*.

To execute the floorplanner on all the problems stored in the *problem* folder, you can use the solve-all.py script as follow:

```shell
python solve-all.py
```

The script will loop over all the problem files, run the floorplanner on each of them and store the final results in the *solutions* folder.

We suggest to use the following workflow for the floorplanning design contest:
1. download all problems from http://raw-floorplanning-contest.necst.it/ and save them in the ./problems folder
2. Modify floorplan.py with your floorplanning algorithm *or* write your own floorplanner in a different programming language (in this case you might still leverage the solve-all.py script with minor changes to the Popen command)
3. Run python solve-all.py
4. Verify that all the solutions to the problems have been generated in the folder ./solutions
5. Zip folder ./solutions
6. Zip your floorplanner source code
7. Submit both the solution archive and the code archive to http://raw-floorplanning-contest.necst.it/
8. The solutions will be validated online, check the score of your submission and possible violeted constraints on the website
