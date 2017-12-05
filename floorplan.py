"""
Simple floorplanning algorithm for demo purposes.

The algorithm reads the problem file from standard input and generate the 
output file to standard output.

In order to run the floorplanner on the example problem execute the following
command from a shell:

python3 floorplan.py < problem.txt > solution.txt

solution.txt will contain the result of the execution
"""

# ensures compatibility with python2 and python3.
# python2 raw_input() as been renamed as input() in python3.
try:
    input = raw_input
except NameError:
    pass

# ----------------------------------------------------------------------------- 
# ----------------------------- PARSE INPUT PROBLEM ---------------------------
# -----------------------------------------------------------------------------

# Id of the problem to be reported in the final solution.
problemId = int(input())

# The total score is computed as:
#
# P - Aw * area - Ww * wirelength
#
# Where:
# area = #CLB * CLBw + #BRAM * BRAMw + #DSP * DSPw
# #CLB = total number of CLB tiles covered by all regions
# #DSP = total number of DSP tiles covered by all regions
# #BRAM = total number of BRAM tiles covered by all regions
#
# wirelength = SUM ( wires_i_j * ( |cx_i - cx_j| + |cy_i - cy_j| ) )
# cx = x coordinate of region center = start_column + covered_columns/2
# cy = y coordinate of region center = start_row + covered_rows/2
#
# read P, Aw, Ww, CLBw, BRAMw and DSPw
P, Aw, Ww = [int(val) for val in input().split(' ')]
CLBw, BRAMw, DSPw = [int(val) for val in input().split(' ')]

# R = FPGA rows
# C = FPGA columns
R, C = [int(val) for val in input().split(' ')]

# The FPGA matrix is composed of R rows and C columns.
# Each entry/tile of the FPGA matrix is a single character with the following 
# meaning:
#
# C = CLB tile
# B = BRAM tile
# D = DSP tile
# F = forbidden tile: regions cannot cover this tile
# - = null tile: no resources available within this tile
#
# Build the fpgaMatrix as a list of lists so that an entry within the matrix
# can be accessed as fpgaMatrix[r][c] where r (in range [0, R-1]) is the row 
# of the FPGA matrix and c (in range [0, C-1]) is the column of the 
# FPGA matrix.
fpgaMatrix = []
for r in range(R):
	fpgaMatrix.append([val for val in input().split(' ')])

# The valid FPGA columns at which the left column of a region can be placed.
# Builds fpgaValidLeft so that fpgaValidLeft[c] is either 1 or 0 depending 
# if a region can have column c as its left side or not respectively. 
fpgaValidLeft = [int(val) for val in input().split(' ')]

# The valid FPGA columns at which the right column of a region can be placed.
# Builds fpgaValidRight so that fpgaValidRight[c] is either 1 or 0 depending 
# if a region can have column c as its right side or not respectively. 
fpgaValidRight = [int(val) for val in input().split(' ')]

# N = number of regions to floorplan.
N = int(input())

# Reads the set of resources required by each region.
#
# creates the data structure 'regionsResourceRequirements' as a list of 
# dictionaries so that the number of resources of type 't' required by region
# 'n' can be retreived as:
#
# numRes = regionsResourceRequirements[n][t]
#
# Where t is either 'C' (CLB), 'B' (BRAM) or 'D' (DSP),
# n is the region id (in range [0, N-1]) and numRes is the number of resources
# of type t required by region n.
regionsResourceRequirements = []

for n in range(N):
	resources = [int(val) for val in input().split(' ')]
	regionsResourceRequirements.append({
		'C' : resources[0],
		'B' : resources[1],
		'D' : resources[2]
	})

# Reads the communication matrix.
#
# Creates a data structure 'commMatrix' so that the number of wires from
# region n1 (in range [0, N-1]) and region n2 [in range [0, N-1]] can be
# retrieved as:
#
# wires = commMatrix[n1][n2]
commMatrix = []
for n in range(N):
	commMatrix.append([int(val) for val in input().split(' ')])

# ----------------------------------------------------------------------------- 
# --------------------------- PERFORM FLOORPLANNING ---------------------------
# -----------------------------------------------------------------------------

# Floorplan the regions on the FPGA, i.e.: for each region, determine 
# the start column, start row, columns covered and rows coverd.
#
# NOTE: this is the section of the code that you want to modify to implement
# a better algorithm :)
floorplan = []

# For this demo we use the following naive floorplanning strategy:
# we try to floorplan each region on a separate row of the fpgaMatrix.
# If the region does not fit into the FPGA row currently considered or
# if there are not enough FPGA rows to store all the regions, the floorplan
# will fail.
# Notice also that this strategy does not take into account the 
# interconnections between the regions and it is not performing any 
# optimization with respect to the given objective function.
for n in range(N):
	# Try to place region n at row r of the FPGA matrix.
	if n >= R:
		# Not enough rows, fail floorplan.
		floorplan = []
		break
	startRow = n;

	# Places the current region at the first valid left column.
	# NOTE: a valid left column must exist.
	for c in range(C):
		if fpgaValidLeft[c] == 1:
			startColumn = c
			break

	# Extends the region horizontally up to the last valid right column.
	# NOTE: a valid right column must exist and must be after the first valid 
	# left column.
	for c in range(C-1,-1,-1):
		if fpgaValidRight[c] == 1:
			endColumn = c
			break

	# The region starts at row 'startRow' and column 'startColumn',
	# covers 1 row and extends for (endColumn - startColumn + 1) columns.
	height = 1
	width = endColumn - startColumn + 1

	# Computes the number of tiles covered by this region for each tile type.
	coveredTiles = {
		'C' : 0, 'B' : 0, 'D' : 0, '-' : 0, 'F' : 0
	}
	for c in range(startColumn, endColumn + 1):
		tileType = fpgaMatrix[startRow][c]
		coveredTiles[tileType] += 1

	# Checks that the region does not cover any forbidden tile, otherwise fail
	# the floorplan.
	# NOTE: better heuristics could be applied instead of failing without
	# backtracking.
	if coveredTiles['F'] > 0:
		floorplan = []
		break

	# Checks that the region covers the required resources, otherwise fail.
	# NOTE: no backtracking is performed.
	if 	coveredTiles['C'] < regionsResourceRequirements[n]['C'] or \
		coveredTiles['B'] < regionsResourceRequirements[n]['B'] or \
		coveredTiles['D'] < regionsResourceRequirements[n]['D']:
		floorplan = []
		break

	# All check passed, stores region floorplan.
	floorplan.append([startColumn, startRow, width, height])

# ----------------------------------------------------------------------------- 
# ------------------------------- WRITE SOLUTION ------------------------------
# -----------------------------------------------------------------------------

# The solution format requires to write the problemId in the first line
# and write the regions coordinates in the subsequent lines.
# Row numbers must be in range [1,R], while column numbers in range [1,C],
# so we need to add 1 to both the startColumn and startRow.
#
# NOTE: if the floorplanner fails, the 'floorplan' list is empty and we do not 
# write any region coordinate.
print(problemId)
for regionPlacement in floorplan:
	startColumn, startRow, width, height = regionPlacement
	startColumn += 1
	startRow += 1
	print(
		str(startColumn) + ' ' + str(startRow) + ' ' +
		str(width) + ' ' + str(height)
	)
