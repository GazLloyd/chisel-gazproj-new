import orjson
import sys
import time

skills_map = "attack defence strength constitution ranged prayer magic cooking woodcutting fletching fishing firemaking crafting smithing mining herblore agility thieving slayer farming runecrafting hunter construction summoning dungeoneering divination invention archaeology necromancy".split()

def getField(entry, field):
	field_split = field.split('.')
	working = entry
	while len(field_split) > 0:
		# if is list, use list fetching
		if isinstance(working, list):
			fs = int(field_split.pop(0))
			try:
				working = working[fs]
			except:
				working = None
		# if is object, use get
		elif isinstance(working, object):
			working = working.get(field_split.pop(0))
		# is an endpoint
		else:
			working = None
		if working is None:
			return None
	
	return working


def main(cache, search, view):
	output = []
	for entry in cache.values():
		# check if this needs to be added
		add_this = False
		out = {}
		for s in search:
			field = getField(entry, s)
			add_this = add_this or (field is not None)
			if field is None:
				out[s] = ''
			else:
				out[s] = field
		if add_this:
			for v in view:
				field = getField(entry, v)
				if field is None:
					out[v] = ''
				else:
					out[v] = field
			output.append(out)

	order_of_args = ['id', 'name']
	for a in search:
		if a not in order_of_args:
			order_of_args.append(a)
	for a in view:
		if a not in order_of_args:
			order_of_args.append(a)
	
	# make file
	outname = f'tabulate_{time.time()}'
	#print(output)
	with open(f'/tools/gazproj/tabulatefiles/{outname}.tsv', 'w', encoding='utf-8') as f:
		f.write('\t'.join(order_of_args))
		for o in output:
			line = []
			for a in order_of_args:
				line.append(str(o.get(a)))
			f.write('\n')
			f.write('\t'.join(line))
	with open(f'/tools/gazproj/tabulatefiles/{outname}.json', 'wb') as f:
		f.write(orjson.dumps({"output":output, "order":order_of_args, 'filename': outname}, f))
	return outname

def run(args=sys.argv[1:]):
	search_args = []
	view_args = ['id', 'name']
	for _a in args[1].split(';'):
		a = _a.strip()
		if a == '':
			continue
		search_args.append(a)
	if len(args) > 2:
		for _a in args[2].split(';'):
			a = _a.strip()
			if a == '':
				continue
			view_args.append(a)

	return main(args[0], search_args, view_args)


if __name__ == '__main__':
	print(run())