"""
Simple script that runs floorplan.py against all the problems
stored in the ./problems folder.

The solutions will be saved in the ./solutions folder using
the same filename of the corresponding solved problem.
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

           



