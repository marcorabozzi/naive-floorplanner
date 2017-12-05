"""
Simple script that runs floorplan.py against all the problems
stored in the ./problems folder.

The solutions will be saved in the ./solutions folder using
the same filename of the corresponding solved problem.

We suggest to use the following workflow for the floorplan contest:
1) 	download all problems from http://caos-fpl-contest.necst.it/ and
	save them in the ./problems folder
2)  Modify floorplan.py with your floorplanning algorithm
3)  Run this script with command: python solve-all.py
4)  Verify that all the solutions to the problems have been generated
	in the folder ./solutions
5) 	Zip folder ./solutions
6) 	Zip your floorplanner source code
7)	Submit both the solution archive and the code archive to 
	http://caos-fpl-contest.necst.it/
8)	The solutions will be validated online, check the score of your submission 
	and possible violeted constraints on the website
"""

import sys
import os
import subprocess

problems_folder = './problems'
solutions_folder = './solutions'

for filename in os.listdir(problems_folder):
    problem_path = os.path.join(problems_folder, filename)
    solution_path = os.path.join(solutions_folder, filename)
    
    if filename.endswith('.txt'):

        print("solving: ", problem_path)
        with open(problem_path, "rt") as input_file, open(solution_path, "wt") as output_file:
                process = subprocess.Popen(['python', 'floorplan.py'], stdout=output_file, stdin=input_file)
                process.wait()
                print("solved!")

           



