from collections import defaultdict
from copy import deepcopy
from itertools import permutations
import math 

import clipboard


def day01():
	def fuel_required(mass):
		if mass < 7:
			return 0
		fuel = mass // 3 - 2
		return fuel + fuel_required(fuel)

	return sum((fuel_required(int(x)) for x in d1_in))


def day02():
	d2_in = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,2,19,9,23,1,23,5,27,2,6,27,31,1,31,5,35,1,35,5,39,2,39,6,43,2,43,10,47,1,47,6,51,1,51,6,55,2,55,6,59,1,10,59,63,1,5,63,67,2,10,67,71,1,6,71,75,1,5,75,79,1,10,79,83,2,83,10,87,1,87,9,91,1,91,10,95,2,6,95,99,1,5,99,103,1,103,13,107,1,107,10,111,2,9,111,115,1,115,6,119,2,13,119,123,1,123,6,127,1,5,127,131,2,6,131,135,2,6,135,139,1,139,5,143,1,143,10,147,1,147,2,151,1,151,13,0,99,2,0,14,0".split(
		',')
	d2_in = [int(x) for x in d2_in]
	for noun in range(100):
		for verb in range(100):
			program = d2_in[:]
			program[1] = noun
			program[2] = verb
			for i in range(len(program) // 4):
				i *= 4
				if program[i] == 99:
					break
				elif program[i] == 1:
					program[program[i +
																					3]] = program[program[i + 1]] + program[program[i + 2]]
				elif program[i] == 2:
					program[program[i + 3]] = program[program[i + 1]] * program[program[i + 2]]
			if program[0] == 19690720:
				print(noun, verb)
				break
				
def day03():
	d = {'D': complex(0,-1),
		'U': complex(0,1),
		'L': complex(-1,0),
		'R': complex(1,0)
	}
	input_data='''R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83'''
#	input_data='''R8,U5,L5,D3 U7,R6,D4,L4'''
	with open(r'aoc2019/day03.txt') as f:
		input_data = f.read()
	in1, in2 = input_data.split()
	moves1, moves2 = in1.split(','), in2.split(',')
	locs1 = set()
	path1 = []
	loc1=complex(0,0)
	for move in moves1:
		direct =d[move[0]]
		dist = int(move[1:])
		for i in range(dist):
			loc1 += direct
			path1.append(loc1)
			locs1.add(loc1)

	path2 = []
	locs2 = set()
	loc2=complex(0,0)
	for move in moves2:
		direct =d[move[0]]
		dist = int(move[1:])
		for i in range(dist):
			loc2 += direct
			path2.append(loc2)
			locs2.add(loc2)
	intersections = locs1.intersection(locs2)
	intersections.discard(complex(0,0))
	shortest_path= min([path1.index(inter)+path2.index(inter) + 2 for inter in intersections])
		

	return int(min([abs(c.real)+abs(c.imag) for c in intersections])), shortest_path

	
def day05(input_data):
#	input_data='3,9,8,9,10,9,4,9,99,-1,8'
#	input_data='3,9,7,9,10,9,4,9,99,-1,8'
	program = [int(x) for x in input_data.split(',')]
	parser = (x for x in program)
	input_val = 5
	output_vals = []
	
	def switch(n, i):
		nonlocal program
		if i: 
			return n
		return program[n]
		
	while True:
		print(program)
		opcode = next(parser)
		print(opcode,end='   ')
		a,b,c,d,e = str(opcode).zfill(5)

		opcode = int(d+e)
		a,b,c=int(a),int(b),int(c)
		if opcode == 1:
			x,y = next(parser), next(parser)
			print(x,y)
			program[ next(parser)] = switch(x,c) + switch(y,b)
		elif opcode == 2:
			x,y = next(parser), next(parser)
			program[ next(parser)] = switch(x,c) * switch(y,b)
		elif opcode == 3:
			program[ next(parser)] = input_val
		elif opcode == 4:
			print('444444444')
			output_vals.append(program[ next(parser)])
		elif opcode == 5:
			x,y = next(parser), next(parser)
			if switch(x,c):
				parser = (x for x in program[switch(y,b):])
		elif opcode == 6:
			x,y = next(parser), next(parser)
			if not switch(x,c):
				parser = (x for x in program[switch(y,b):])
		elif opcode == 7:
			x,y,z = next(parser), next(parser), next(parser)
			if switch(x,c) < switch(y,b):
				program[z] = 1
			else:
				program[z] = 0
		elif opcode == 8:
			x,y,z = next(parser), next(parser), next(parser)
			if switch(x,c) == switch(y,b):
				program[z] = 1
			else:
				program[z] = 0
		elif opcode ==99:
			break
	
	print(output_vals)
	
	ans1=output_vals[-1]
	ans2=None
	return ans1,ans2
	
	
def day06(input_data):
	print(input_data)
	orbits = defaultdict(lambda: {'sattelites':[],'distance':0,'YOUdist':None,'SANdist':None})
	parents = {}
	for line in input_data.split():
		parent, child = line.split(')')
		orbits[parent]['sattelites'].append(child)
		parents[child] = parent

	distance = 0
	chain = ['COM']
	for body in chain:
		distance=orbits[body]['distance']
		for child in orbits[body]['sattelites']:
			orbits[child]['distance']= distance+1
			chain.append(child)
#	print(orbits)

	child = 'YOU'
	distance = 0
	while parent != 'COM':
		parent=parents[child]
		orbits[parent]['YOUdist'] = distance
		child=parent
		distance += 1
	parent=child='SAN'
	distance = 0
	while parent != 'COM':
		parent=parents[child]
		orbits[parent]['SANdist'] = distance
		child=parent
		distance += 1
		
	ans1= sum((body['distance'] for body in orbits.values()))
	ans2= min((o['SANdist'] + o['YOUdist'] for o in orbits.values() if o['SANdist'] and o['YOUdist']))
	return ans1,ans2
	
	
def day07(input_data:str):
	
	def switch(n, i):
		nonlocal program
		if i: 
			return n
		return program[n]
		
	if True:# input_data is None:
		input_data = '''3,8,1001,8,10,8,105,1,0,0,21,34,47,72,93,110,191,272,353,434,99999,3,9,102,3,9,9,1001,9,3,9,4,9,99,3,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,1001,9,2,9,1002,9,2,9,101,4,9,9,4,9,99,3,9,1002,9,3,9,101,5,9,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,101,3,9,9,102,4,9,9,1001,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99'''
		
	phase_seqs = permutations(range(5))

	output_vals = [0]
	maxi = 0
	
	for phase_seq in phase_seqs:
		input_vals = [0]
		for phase in phase_seq:
			program = [int(x) for x in input_data.split(',')]
			parser = (x for x in program)
			
			input_vals.append(phase)
		
			while True:
				opcode = next(parser)
				a,b,c,d,e = str(opcode).zfill(5)
		
				opcode = int(d+e)
				a,b,c=int(a),int(b),int(c)
				if opcode == 1:
					x,y = next(parser), next(parser)
					program[ next(parser)] = switch(x,c) + switch(y,b)
				elif opcode == 2:
					x,y = next(parser), next(parser)
					program[ next(parser)] = switch(x,c) * switch(y,b)
				elif opcode == 3:
					program[ next(parser)] = input_vals.pop()
				elif opcode == 4:
					input_vals.append(program[ next(parser)])
				elif opcode == 5:
					x,y = next(parser), next(parser)
					if switch(x,c):
						parser = (x for x in program[switch(y,b):])
				elif opcode == 6:
					x,y = next(parser), next(parser)
					if not switch(x,c):
						parser = (x for x in program[switch(y,b):])
				elif opcode == 7:
					x,y,z = next(parser), next(parser), next(parser)
					if switch(x,c) < switch(y,b):
						program[z] = 1
					else:
						program[z] = 0
				elif opcode == 8:
					x,y,z = next(parser), next(parser), next(parser)
					if switch(x,c) == switch(y,b):
						program[z] = 1
					else:
						program[z] = 0
				elif opcode ==99:
					break

		maxi=max(int(input_vals[-1]),maxi)
	
	print(input_vals)
	
	ans1=maxi
	
	
	phase_seqs = permutations(range(5,10))
	input_data='''3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'''

	maxi = 0


	for phase_seq in phase_seqs:
		input_vals = [0]
		programmes = []
		parsers = []
		complete = [False for _ in range(5)]
		while not all(complete):
			for i, phase in enumerate(phase_seq):
				if len(programmes)<5:
					print(i)
					input_vals.append(phase)
					programmes.append( [int(x) for x in input_data.split(',')])
					parsers.append( (x for x in program))
	#			program = programmes[i]
				parser = parsers[i]
			
				while True:
					try:
						opcode = next(parser)
					except StopIteration:
						complete[i] = True
						break
					a,b,c,d,e = str(opcode).zfill(5)
			
					opcode = int(d+e)
					a,b,c=int(a),int(b),int(c)
					if opcode == 1:
						x,y = next(parser), next(parser)
						program[ next(parser)] = switch(x,c) + switch(y,b)
					elif opcode == 2:
						x,y = next(parser), next(parser)
						program[ next(parser)] = switch(x,c) * switch(y,b)
					elif opcode == 3:
						print('3'*20)
						program[ next(parser)] = input_vals.pop()
					elif opcode == 4:
						print('4'*20)
						input_vals.append(program[ next(parser)])
						print(input_vals)
	#					break
					elif opcode == 5:
						x,y = next(parser), next(parser)
						if switch(x,c):
							parser = (x for x in program[switch(y,b):])
					elif opcode == 6:
						x,y = next(parser), next(parser)
						if not switch(x,c):
							parser = (x for x in program[switch(y,b):])
					elif opcode == 7:
						x,y,z = next(parser), next(parser), next(parser)
						if switch(x,c) < switch(y,b):
							program[z] = 1
						else:
							program[z] = 0
					elif opcode == 8:
						x,y,z = next(parser), next(parser), next(parser)
						if switch(x,c) == switch(y,b):
							program[z] = 1
						else:
							program[z] = 0
					elif opcode ==99:
						print('9'*20)
						break

		maxi=max(int(input_vals[-1]),maxi)
	
	ans2=maxi
	return ans1,ans2
	
	
def test_day07():
	tests = {
		'''3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0''':(43210,None),
		'''3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0''':(54321,None)
	}
	passed = True
	for input_data, right_answer in tests.items():
		try:
			my_ans = day07(input_data)
			assert my_ans == right_answer
			print('PASS',right_answer)
		except AssertionError:
			print('ERROR\n',input_data, my_ans, 'Right answer:',right_answer)
			passed = False
			
	if passed:
		print('all tests passed'.upper())
	
	
def day08(input_data):
	layers = []
	width = 25
	height = 6
	nb_lays = len(input_data)//(width*height)
	picture = [[2,]*width for _ in range(height)]
	min_zeroes = float('inf')
	for lay_num in range(nb_lays):
		layer = input_data[lay_num*width*height:(lay_num+1)*width*height]

		layers.append(layer)
		zeroes = layer.count('0')
		if zeroes < min_zeroes:
			min_zeroes = zeroes
			ones = layer.count('1')
			twos = layer.count('2')
		for i,row in enumerate(picture):
			for j, val in enumerate(row):
				if val == 2:
					row[j]= int(layer[(i*width)+j])

	
	ans1=ones*twos
	
	t = str().maketrans({'1':'8','0':' '})
	for row in picture:
		print(''.join(str(i) for i in row).translate(t))
	
	ans2=None
	return ans1,ans2
	
	
def day10(input_data:str):
	#. 20+18j
	def direction(comp):
		gcd = max(math.gcd(int(comp.real), int(comp.imag)),1)
		return complex(comp.real/gcd,comp.imag/gcd)
		
	def degrees_north(c:complex):
		gcd = max(math.gcd(int(c.real), int(c.imag)),1)
		angle = math.atan2(c.real/gcd,c.imag/gcd) * 360 /(2*math.pi)
		if angle < 0:
			angle += 360
		return angle
		
	def in_grid(comp: complex):
		return max(comp.real,comp.imag) <= width and min(comp.real,comp.imag)>=0
			
	if True:# not input_data:
		input_data = '''.###.#...#.#.##.#.####..
.#....#####...#.######..
#.#.###.###.#.....#.####
##.###..##..####.#.####.
###########.#######.##.#
##########.#########.##.
.#.##.########.##...###.
###.#.##.#####.#.###.###
##.#####.##..###.#.##.#.
.#.#.#####.####.#..#####
.###.#####.#..#..##.#.##
########.##.#...########
.####..##..#.###.###.#.#
....######.##.#.######.#
###.####.######.#....###
############.#.#.##.####
##...##..####.####.#..##
.###.#########.###..#.##
#.##.#.#...##...#####..#
##.#..###############.##
##.###.#####.##.######..
##.#####.#.#.##..#######
...#######.######...####
#....#.#.#.####.#.#.#.##'''
	width= max(len(input_data.split()),len(input_data.split()[0]))
	asteroids = {}
	for y, line in enumerate(input_data.split()):
		for x, l in enumerate(line):
			if l == '#':
				asteroids[complex(x,width-y)] = True
	print(asteroids)
	#PART TWO
	targets = {c - complex('20+18j') :None for c in asteroids}
	directions = defaultdict(list)
	for target in targets:
		directions[degrees_north(target)].append(target)
	print(directions)
	prev_dir = -1
	blasted = 0
	while True:
		for direct in sorted(directions):
			targets = directions[direct]
			targets.sort(key = lambda c: abs(c),reverse=True)
#			print(direct,directions[direct])
			if targets:
				target = targets.pop()
				blasted +=1
				if blasted==200:
					print(target)
					ans2 = target
		

	
	# PART ONE
	maxi = 0
	max_loc = None
#	print(asteroids)
	for loc in asteroids:
#		print(loc)
		loc_asteroids = deepcopy(asteroids)
		loc_asteroids[loc] = False
		for other_loc in loc_asteroids:
			for i in range(1,width+1):
				direct = direction(other_loc-loc)
	#			print(loc,other_loc,direct)
				shadow_loc= other_loc+i*direct
				if not in_grid(shadow_loc):
					break
				if shadow_loc in loc_asteroids:
#					print('hey',shadow_loc)
					loc_asteroids[shadow_loc] = False
		loc_maxi= sum(loc_asteroids.values())
		if loc_maxi>maxi:
			maxi = loc_maxi
			max_loc = loc
#		print(loc_asteroids)
	print(maxi, max_loc)
				
		
	ans1=maxi

	return ans1,ans2
	

def test_day10():
	tests = {'''.#..#
.....
#####
....#
...##''':8,

'''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####''':33
}
	passed = True
	for input_data, right_answer in tests.items():
		try:
			my_ans = day10(input_data)[0]
			assert my_ans == right_answer
		except AssertionError:
			print('ERROR\n',input_data, my_ans, 'Right answer:',right_answer)
			passed = False
			
	if passed:
		print('all tests passed'.upper())
			
def day14(input_data):
	ingredients = defaultdict(list)
	qty_made = {}
	for line in input_data.split('\n'):
		ins,out = line.split(' => ')
		out = out.split()
		out = (int(out[0]),out[1])
		for ingredient in ins.split(', '):
			ingredient = ingredient.split()
			ingredients[out[1]].append(ingredient[1])
			qty_made[out[1]] = int(ingredient[0])
	print(ingredients, qty_made)
	needs = {'FUEL':1}
	haves = defaultdict(int)
	ore = 0
	while 'FUEL' not in haves:
		for need, num_needed in needs.items():
			for ingre in ingredients[need]:
				ingreds_made= qty_made[ingre]
				qty = ((qty//num_needed)+1)-haves[ingre]
				haves
			pass
	ans1=None
	ans2=None
	return ans1,ans2			
			
			
def test_day14():
	tests = {
		'''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL''':(31,None)
	}
	passed = True
	for input_data, right_answer in tests.items():
		try:
			my_ans = day14(input_data)
			assert my_ans == right_answer
			print('PASS',right_answer)
		except AssertionError:
			print('ERROR\n',input_data, my_ans, 'Right answer:',right_answer)
			passed = False
			
	if passed:
		print('all tests passed'.upper())
	

if __name__ == '__main__':
	day = 7
	try:
		with open(f'aoc2019//day{day:02d}.txt') as f:
			input_data = f.read()
	except FileNotFoundError:
		input_data=None
	
	try:
		exec(f'test_day{day:02d}()')
		answer = eval(f'day{day:02d}(input_data)')
	except NameError:
		answer = (None,f'def day{day:02d}(input_data:str):\n\tans1=None\n\tans2=None\n\treturn ans1,ans2')
	print(answer)

	try:
		clipboard.set(str(answer[-1]))
	except TypeError:
		clipboard.set(str(answer))
