
import rlp
from generic_mutator_bytes import *
import random
import copy
import dosstuff

MAX_ADD_COUNT = 5 # Add a maximum of five copies of a list thing..


def init(seed):
	pass

def deinit():
	pass



def mutate_list(some_bullshit):

	# Select random element to mutate.


	if len(some_bullshit) == 0:
		return b"AAAAA" # Safeguard.

	strat = random.randrange(3)
	if strat == 0:
		# Pop random element.
		orig_len = len(some_bullshit)
		some_bullshit.pop(random.randrange(len(some_bullshit))) # Pop an element
		new_len = len(some_bullshit)
		assert new_len == orig_len - 1 #  We should remove one element from the list...
		return some_bullshit
	elif strat == 1:
		# Multiply element in the list...
		rand_element = copy.deepcopy(random.choice(some_bullshit)) # Copy that shit...
		# Now try to add it a couple of times.
		for _ in range(MAX_ADD_COUNT):
			some_bullshit.insert(random.randrange(len(some_bullshit)), copy.deepcopy(rand_element))
		return some_bullshit
	elif strat == 2: # Mutate element.
		rand_index = random.randrange(len(some_bullshit))
		if isinstance(some_bullshit[rand_index], list):
			mutate_list(some_bullshit[rand_index]) # Recursively.
			return some_bullshit
		elif isinstance(some_bullshit[rand_index], bytes) or isinstance(some_bullshit[rand_index], bytearray):
			# Now just use generic mutator.
			some_bullshit[rand_index] = mutate_generic(some_bullshit[rand_index])
			return some_bullshit
		else:
			print("poopoof"*1000)
			assert False
	elif strat == 3:
		# Just copy a random element a bunch of times...
		rand_element = random.choice(some_bullshit)
		rand_element = copy.deepcopy(rand_element)

		for _ in range(random.randrange(1,100000)):
			some_bullshit.insert(random.randrange(len(some_bullshit)), rand_element)
		return some_bullshit

	print("Fuck!!!"*10000)
	assert False

def fuzz(buf, add_buf, max_size):
	buf = bytes(buf)

	#if random.randrange(10) == 1:
	#	return bytearray(dosstuff.mutate(bytes(buf))[:max_size])[:max_size]
	#print("mutatinggggg")

	#fh = open("paska.bin", "wb")
	#fh.write(buf)
	#fh.close()
	
	try:
		#print("fffffffffffffffffffffffffffff!!!!")
		thing = rlp.decode(buf)

		#fh = open("shitfuck.bin", "wb")
		#fh.write(b"somebullshitheremaybefefefefefefefefefefefefefefefefe")
		#fh.close()
	
		#print("decded!!!!")
		#assert False
		#print(str(type(thing))*10000)
		if isinstance(thing, bytes): # Just one value.
			#print("fuukccc"*1000)
			resthing = bytearray(rlp.encode(mutate_generic(thing)))[:max_size]
			#print("resthing == "+str(resthing))
			#print("Returning input with length: "+str(len(resthing)))
			return resthing
		elif isinstance(thing, list):
			# 
			#print("poooopooooooo")
			resthing = bytearray(rlp.encode(mutate_list(thing)))[:max_size]
			#print("resthing == "+str(resthing))
			#print("Returning input with length: "+str(len(resthing)))
			return resthing
		else:
			#print("Invalid type!!!")
			assert False
	except Exception as e: # Invalid data. Just return original buffer.
		#print("Encountered exception: "+str(e))
		return bytearray(buf)

	#return mutated_out

def fuzz_count(buffer):
	try:
		res = rlp.decode(bytes(buffer))

		return 10_000
	except:
		return 1 # Invalid so just do this


if __name__=="__main__":

	fh = open("input.bin", "rb")
	data = fh.read()

	fh.close()

	res = fuzz(bytearray(data), bytearray(b"AAAA"), 10000)
	assert isinstance(res, bytearray)
	print(res)

	exit(0)


