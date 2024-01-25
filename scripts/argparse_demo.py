def blah(x, y):
	print(x, y)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('x')
	parser.add_argument('y')

	args = parser.parse_args()
	blah(args.x, args.y)


# # Bit in __name__ block not run
# import test

# # Bit in __name__ block run
# python test.py

