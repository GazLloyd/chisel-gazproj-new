import orjson
import requests
import mwparserfromhell
PARAMETER_CONFIGS = {}

# image from name, replaces invalid characters
# @param {str} name the file name
# @returns {str} the formatted file name
def filename(name):
	fname = name.replace('/', '-').replace(':', '-')
	return f'[[File:{fname}.png]]'

# gets the wikitext of a page
# @param {str} page pagename to get
# @returns {str} the text of the page. will return an empty string if the page does not exist
def get_text(page):
    text = wikiutils.get_text(page)
    if text is None:
        text = ''
    return text

# fetch old infobox from the wiki
# @param {str} pagename name of the page
# @param {str} templatename name of the template
# @returns {Tuple[dict[str,str], str]} returns a dict of parameters:values, and the unmodified template as a string
def get_from_wiki(pagename, templatename):
	text = get_text(pagename)
	wikitext = mwparserfromhell.parse(text)
	params = {}
	oldtemp = None
	for temp in wikitext.filter_templates(match=lambda x: str(x.name).strip().lower() == templatename):
		oldtemp = str(temp)
		for param in temp.params:
			params[str(param.name).strip()] = str(param.value).strip()
	return params, oldtemp


# make an infobox - entrypoint from base.py
# @param {str} infoboxtype the type of infobox to make
# @param {dict[int,dict]} fullcache the complete cache, passed in from the main process
# @param {list[{"id":int, "ver":str|None}]} config configuration of the infobox. a list of dicts, where each dict includes an id for that version, and an optional version name
#           if omitted, version name will be the id
#           singleton infoboxes ignore version names
# @param {str|None} merge=None name of the page to fetch the infobox from and attempt to merge with; if None, does not attempt a merge
def make(infoboxtype, fullcache, config, merge=None):
	datas = []
	for conf in config:
		i = config['id']
		if len(config) == 1:
			v = None
		else:
			v = config.get('ver', str(i))
		cache = fullcache.get(i)
		d = None
		if cache is not None:
			func = None
			if infoboxtype == 'ITEM':
				func = item_params
			elif infoboxtype == 'BONUS':
				func = bonus_params
			elif infoboxtype == 'RECIPE':
				func = recipe_params
			elif infoboxtype == 'MONSTER':
				func = monster_params
			if func is not None:
				d = func(cache, v, merge)
		datas.append(d)

# load infobox parameter configs from json
def load_configs():
	global PARAMETER_CONFIGS
	with open("infobox_parameters.json", 'rb') as f:
		PARAMETER_CONFIGS = orjson.loads(f.read())
load_configs()

# finds the most common value in the list and returns it
# returns None if:
#	No most common value (everything has 1 occurence)
#	Most common value is None
#	Multiple things have the same number of occurences
# @param {list[any]} vals list of things to check
# @returns {any|None} the most common value, or None if no most common value
#                   most common value could be None, where None is returned; this is desirable in this case
#                   as we want the case of no most common 
def most_common(vals):
	if len(vals) == 1:
		return None #guaranteed to be None so lets skip everything else
	max_val = None #the value
	max_val_count = 0 #the count of the value
	max_val_count_count = 0 #the number of values that have the same max_count; if this is >1 then there isn't one most common value
	for v in set(vals):
		c = vals.count(v)
		if c > max_val_count:
			max_val = v
			max_val_count = c
			max_val_count_count = 1
		elif c == max_val_count:
			max_val_count_count += 1
	if max_val_count == 1:
		return None
	if max_val_count_count > 1:
		return None
	return max_val


# format an infobox
# @param {list[dict[str,str]]} params parameters of the infobox - a list of dicts of arg:value
# @param {str} infobox_name name of the infobox
# @param {list[str]} param_order order of parameters
# @param {list[str]} required_params list of parameters that are required by the infobox
# @returns {str} the formatted infobox
def format_infobox(params, infobox_name, param_order, required_params):
	all_params = set()
	for box in params:
		all_params.update(box.keys())
	if not all_params.issubset(param_order):
		raise Exception(f'Invalid parameter(s): {all_params.difference(param_order)}')
	is_singleton = len(params) == 1
	out = ['{{'+infobox_name]
	for param in param_order:
		is_required = param in required_params
		one_is_defined = False
		vals = []
		for i in range(len(params)):
			v = params[i].get(param)
			if v is not None:
				v = str(v).strip()
				one_is_defined = True
			vals.append(v)
		common = most_common(vals)
		if common is not None:
			out.append(f'|{param} = {common}')
		for i,v in enumerate(vals):
			if is_singleton:
				iver = ''
			else:
				iver = i+1
			if common is not None and v == common:
				# intentional pass to be clear
				# if common is available and v is equal to it, skip
				pass
			else:
				if v is None or v == '':
					if is_required or one_is_defined:
						out.append(f'|{param}{iver} = ')
				else:
					out.append(f'|{param}{iver} = {v}')
	out.append('}}')
	return '\n'.join(out)



# construct a dict of the paramters of the infobox from the cache
# @param {dict} cache the cache entry for the item
# @param {str|None} version=None name of the version, or none for singletons
# @param {str|None} merge=None name of the page to fetch the infobox from and attempt to merge with; if None, does not attempt a merge
# @returns {dict}
def item_params(cache, version=None, merge=None):
	params = {}
	name = cache.get('name')
	extra = cache.get('extra', {})

	if version is not None:
		params['version'] = version
	
	params['name'] = name
	
	return params




def test():
	print('test 1: singleton\nexpected:4 values a,b,c,d')
	print(format_infobox([{'a':'hello','b':'bello','c':'cello','d':'bob'}], [], 'test', ['a','b','c','d'], ['a','c']))

	print('\ntest 2: simple versions with everything different\nexpected: 10 values version1,version2,a1,a2,b1,b2,c1,c2,d1,d2')
	print(format_infobox([{'a':'hello','b':'bello','c':'cello','d':'bob'},{'a':'yello','b':'gello','c':'jello','d':'dod'}], ['a','b'], 'test', ['a','b','c','d'], ['a','c']))


	print('\ntest 3: versions with some overlap\nexpected: version1,version2,version3, a,a2, b,b1, c1,c2,c3, d,d3')
	print(format_infobox([{'a':'hello','b':'bello','c':'cello','d':'bob'},{'a':'yello','b':'gello','c':'jello','d':'bob'},{'a':'hello','b':'gello','c':'aello','d':'bob2'}], ['gee', 'dee', 'pee'], 'test', ['a','b','c','d'], ['a','c']))


	print('\ntest 4: versions with missing info\nexpected: version1,version2,version3,version4, a,a2=, b,b4=, c1=,c2=,c3=,c4=, (no d)')
	print(format_infobox([{'a':'hello','b':'bello'},{'b':'bello'},{'a':'hello','b':'bello'},{'a':'hello',}], ['man','i','love','fishing'], 'test', ['a','b','c','d'], ['a','c']))

if __name__ == '__main__':
	test()