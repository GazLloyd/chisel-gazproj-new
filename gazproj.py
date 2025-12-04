import os
import sys
sys.path.append('/tools/gazproj/')
from wsgirouter import Router
import orjson
from time import strftime, gmtime
from urllib.parse import parse_qs
from re import compile as recomp, IGNORECASE

# maximum size of a chunk to read when serving static files
# int
CHUNKSIZE=1024*1024
# map of mimetype to a list of tuples of (route regex, static filepath)
# these files are served as-is, no alterations
# dict[mimetype, list[tuple[route,filepath]]]
STATIC_SERVES = {
	'text/html; charset=utf-8': [
		(r'^/$', 'html/index.html'), # homepage
		(r'^/mrid$', 'html/mrid.html'), #mrdbs
		(r'^/mrod$', 'html/mrod.html'), #mrdbs
		(r'^/mrnd$', 'html/mrnd.html'), #mrdbs
		(r'^/usercontribsdiff$', 'html/usercontribsdiff.html'),
		(r'^/tally$', 'html/tally.html'),
		(r'^/gazbot$', 'html/gazbot.html'),
		(r'^/recipe$', 'html/recipe.html'),
		(r'^$', 'html/.html'),
		(r'^$', 'html/.html'),
		(r'^$', 'html/.html'),
		(r'^$', 'html/.html'),
		(r'^$', 'html/.html'),
	],
	'text/css': [
		(r'^styles.css$', 'css/styles.css'),
	],
	'text/javascript': [
		(r'^mrdbs.js$', 'js/mrdbs.js'),
	],
	'application/json': [
		(r'$/gazbot/status_rs$', '/home/gaz/gazgebot/GazGEBot/config/rs_ge.json'),
		(r'$/gazbot/status_os$', '/home/gaz/gazgebot/GazGEBot/config/os_ge.json'),
		(r'$/gazbot/rs_dump.json$', '/home/gaz/gazgebot/GazGEBot/rs_dump.json'),
		(r'$/gazbot/os_dump.json$', '/home/gaz/gazgebot/GazGEBot/os_dump.json'),
	]
}
INDSORT = orjson.OPT_APPEND_NEWLINE|orjson.OPT_INDENT_2|orjson.OPT_SORT_KEYS
def inputhtmlsafe(s):
	return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(u'\xa0', ' ')

# names of the cache files, without the rest of the filepath or .json
# list[str]
RSCACHE_FILENAMES = ['items', 'npcs', '']
# directory of the cache files
# str
RSCACHE_FILEPATH = '/home/gaz/rscache' 

# rscache data
rscache_data = {}
rscache_maxids = {}

# the router itself
# i believe the `application`` variable has to be the router
application = Router()
# shortcut, so we can do @r()
r = application.route

# open a file with utf-8 encoding
# (str, str) => filehandle
def openu(fn, ot):
	return open(fn, ot ,encoding='utf-8')

# format a time in HH:MM:SS DD MM YY
# (float) => str
def timeformat(t):
	return strftime("%H:%M:%S %d %B %Y" , gmtime(t))

# returns the formated modified-by time for a file
# (str) => str
def modtime(fn):
	return timeformat(os.stat(fn).st_mtime)

# load a json file (efficiently with orjson)
# (str)=>dict|list
def loadjson(filepath):
	with open(filepath, 'rb') as f:
		return orjson.loads(f.read())

# save a json file (efficiently using orjson)
# optional args: indent - pretty-print the json; sort - sort the keys of dicts in the json
# (str, dict|list, bool=false, bool=false) => void
def savejson(filepath, json, indent=False, sort=False):
	flags = orjson.OPT_APPEND_NEWLINE
	if indent:
		flags |= orjson.OPT_INDENT_2
	if sort:
		flags |= orjson.OPT_SORT_KEYS
	with open(filepath, 'wb') as f:
		f.write(orjson.dumps(json, option=flags))

# generate the HTML files of the diffs
# () => void
def makeDiffHtmls():
	for fn in RSCACHE_FILENAMES:
		with openu(f'{RSCACHE_FILEPATH}/{fn}_diff.txt', 'r') as fin, openu(f'{RSCACHE_FILEPATH}/{fn}_diff.html', 'w') as fout:
			fout.write(f'''<!DOCTYPE html>
			<html>
			<head><title>{fn}_diff.txt</title></head>
			<style>
			body {{
				background: #071022;
				color: #f9f9f9;
				border: #071022;
			}}
			pre {{
				white-space: pre-wrap;
			}}</style>
			<body>
			<pre>''')
			fout.write(fin.read())
			fout.write('''</pre>
			</body>
			</html>''')
	with openu('html/index_template.html','r') as ftemp, openu('html/index.html', 'w') as fout:
		fout.write(ftemp.read().format(
			items = modtime('/home/gaz/rscache/items.json'),
			alog = modtime('/home/gaz/rscache/alog.json'),
			npcs = modtime('/home/gaz/rscache/npcs.json'),
			best = modtime('/home/gaz/rscache/bestiary.json'),
			objs = modtime('/home/gaz/rscache/locations.json')
		))
	for mr, mt in [('mrid','items'), ('mrnd', 'npcs'), ('mrod', 'locations')]:
		with openu(f'html/{mr}_template.html','r') as ftemp, openu(f'html/{mr}.html', 'w') as fout:
			dictofnames = {x['id']:x.get('name','') for x in rscache_data[mt]}
			listofnames = []
			for i in range(0,max(dictofnames.keys())+1):
				if i in dictofnames:
					listofnames.append(dictofnames[i])
				else:
					listofnames.append('')
			js = orjson.dumps(listofnames).decode().replace("'",r"\'")
			fout.write(ftemp.format(namesjson=js))

# reload the RS cache jsons & remake the html
# () => void
def reloadRSCache():
	global rscache_data
	rscache_data = {}
	rscache_maxids = {}
	for fn in RSCACHE_FILENAMES:
		rscache_data[fn] = {x['id']:x for x in loadjson(f'{RSCACHE_FILEPATH}/{fn}.json')}
		rscache_maxids[fn] = max(rscache_data.keys())
	rscache_data['alog'] = {x['item_id']:x for x in loadjson(f'{RSCACHE_FILEPATH}/alog.json')}
	for i,v in loadjson(f'{RSCACHE_FILEPATH}/location_examines.json.json'):
		rscache_data['locations'].get(i, {})['examine'] = v['examine']
	for v in rscache_data['alog']:
		if type(v) == dict:
			rscache_data['items'].get(v['item_id'], {})['examine'] = v['desc']
	makeDiffHtmls()

# generator to read a file in chunks, reduce memory overhead of reading a file
# (file handle)*=>bytes
def filechunks(fd):
	while True:
		chunk = fd.read(CHUNKSIZE)
		if not chunk:
			break
		yield chunk

# serve a static file
# (start response object, string, string) => bytes
def serve_file(start_response, filepath, mime):
	try:
		with open(filepath, 'rb') as f:
			start_response('200 OK', [('Content-Type', mime)])
			return filechunks(f)
	except:
		start_response('404 NOT FOUND', [('Content-Type', mime)])
		return '404 NOT FOUND'.encode('utf-8')

# setup a static file, adding the route to the router
# (regexstr, str, str) => void
def static_file(route, filepath, mime):
	def serve(env, resp):
		yield serve_file(resp, filepath, mime)
	regex = re.compile(pat)
	application.rules.append(((regex, ['GET'], serve),(pat,)))

# set up the defined static serves
for mimetype, fileroutes in STATIC_SERVES.items():
	for route,filename in fileroutes:
		static_file(route, filename, mimetype)

# setup cache serves
for fn in RSCACHE_FILENAMES:
	static_file(f'^/cache/{fn}.json$', f'{RSCACHE_FILEPATH}/{fn}.json', 'application/json') #cache file
	static_file(f'^/cache/{fn}_diff.txt$', f'{RSCACHE_FILEPATH}/{fn}_diff.txt', 'text/plain') #cache diff as plaintext
	static_file(f'^/cache/{fn}_diff.html$', f'{RSCACHE_FILEPATH}/{fn}_diff.html', 'text/html; charset=utf-8') #cache diff as html

# reload the cache
reloadRSCache()

def get_item_name(item_cache, dflt=None):
	if item_cache is not None:
		if item_cache.get('name') is not None:
			return item_cache.get('name')
		if item_cache.get('combine_shard_name') is not None:
			return item_cache.get('combine_shard_name')
	return dflt

def get_unnoted_item(item_cache):
	notedata = item_cache.get('noteData')
	if notedata is None:
		notedata = item_cache.get('bindLink')
	if notedata is None:
		return None
	return rscache_data['items'].get(notedata)

def stripNulls(l):
	return list(filter(lambda x: not (x is None or x=='null'), l))

def formatMRDB_items(vals):
	out = []
	for cache in vals:
		ret = {
			'id': cache.get('id'),
			'name': get_item_name(cache, '@unknown@'),
			'value': cache.get('value', 1),
			'examine': cache.get('examine', ''),
			'actions_inv': stripNulls(cache.get('widget_actions', [])),
			'actions_worn': [],
			'actions_ground': stripNulls(cache.get('ground_actions', [])),
			'tradeable': not cache.get('notTradeable', False),
			'on_ge': cache.get('is_on_ge') is not None,
			'members': cache.get('Members'),
			'noted': False,
			'hasrecipe': False,
			'models': str(cache.get('baseModel', ''))
		}
		extra = cache.get('extra', {})
		if ret.get('name') == '@unknown@':
			unnoted = get_unnoted_item(cache)
			if unnoted is not None:
				ret['noted'] = True
				ret['name'] = get_item_name(unnoted.get('cache'), '@unknown@')
		
		if extra is not None:
			for i in range(1,11):
				act = extra.get('worn_option_'+str(i))
				if act is not None:
					ret['actions_worn'].append(act)
			ret['hasrecipe'] = 'create_requirement_type_1' in extra or 'craft_xp_skill_1' in extra or 'craft_item_1' in extra

		for i in ['rotation', 'modelTranslate', 'colours', 'textures', 'scale', 'maleModels', 'femaleModels', 'maleHeads', 'femaleHeads']:
			ret[i] = str(cache.get(i, ''))

		out.append(ret)
	return out

def formatMRDB_npcs(vals):
	out = []
	for cache in vals:
		ret = {
			'id': cache.get('id'),
			'name': cache.get('name','@unknown@'),
			'combat': cache.get('combat'),
			'examine': '',
			'members': '',
			'pet_item_id': cache.get('extra', {}).get('pet_item_id', ''),
			'actions': stripNulls(cache.get('actions')),
			'members_actions': stripNulls(cache.get('members_actions'))
		}

		bestiary = rscache_data['bestiary'].get(cache.get('id'))
		if type(bestiary) == dict and bestiary.get('contents', '') != 'null':
			if bestiary.get('members') is not None:
				ret['members'] = bestiary.get('members')
			if bestiary.get('description') is not None:
				ret['examine'] = bestiary.get('description')
		out.append(ret)
	return out

def formatMRDB_locations(vals):
	out = []
	for cache in vals:
		ret = {
			'id': cache.get('id'),
			'name': cache.get('name', ''),
			'members': cache.get('isMembers', ''),
			'examine': cache.get('examine', ''),
			'actions': stripNulls(cache.get('actions'), []),
			'members_actions': [],
			'morphs_1': cache.get('morphs_1'),
			'morphs_2': cache.get('morphs_2')
		}
		for i in range(1,11):
			a = cache.get('members_action_'+str(i))
			if a is not None:
				ret['members_actions'].append(a)
		out.append(ret)
	return ret


ALLOWED_MRDBS = ['items', 'npcs', 'locations']
MRDB_RXS = {
	'id': recomp(r'(\d+)'),
	'idrange': recomp(r'(\d+)([-+])(\d+)'),
	'recent': recomp(r'recent(\d+)', IGNORECASE),
	'enum': recomp(r'enum(\d+)', IGNORECASE)
}
@r('^/mrdb/get$')
def route_mrdb_get(env,resp):
	qs = parse_qs(env.get('QUERY_STRING',''))
	qs_db = qs.get('db')
	if qs_db not in ALLOWED_MRDBS:
		resp('400 ERROR', [('Content-Type', 'application/json')])
		return b'{"error":"invalid mrdb provided"}'
	queries = qs.get('q', [])
	if len(queries) < 1:
		resp('400 ERROR', [('Content-Type', 'application/json')])
		return b'{"error":"no query provided"}'
	db = rscache_data[qs_db]
	ret = []
	for q in queries:
		q = q.strip()
		m = MRDB_RXS['id'].fullmatch(q)
		if m is not None:
			val =  db.get(int(m.group(1)))
			if val is not None:
				ret.append(val)
			continue
		m = MRDB_RXS['idrange'].fullmatch(q)
		if m is not None:
			startid = int(m.group(1))
			endid = int(m.group(3))
			if m.group(2) == '+':
				endid = startid + endid
			for i in range(startid, endid+1):
				val = db.get(i)
				if val is not None:
					ret.append(val)
			continue
		m = MRDB_RXS['recent'].fullmatch(q)
		if m is not None:
			val = int(m.group(1))
			maxid = rscache_maxids[qs_db]
			for i in range(maxid-val, maxid+1):
				val = db.get(i)
				if val is not None:
					ret.append(val)
			continue
		m = MRDB_RXS['enum'].fullmatch(q)
		if m is not None:
			val = int(m.group(1))
			enm = rscache_data['enums'].get(val)
			if enm is not None:
				c08 = enm.get('code_08')
				if c08 is not None:
					for k in sorted(enm.get('code_08').keys(), key=int):
						val2 = db.get(c08.get(k))
						if val2 is not None:
							ret.append(val2)
			continue
		# must be a search
		cmp = None
		test = None
		if q[0] == '/' and q[-1] == '/':
			cmp = recomp(q[1:-1], IGNORECASE)
			test = lambda x: rx.search(x) is not None
		else:
			cmp = q.lower()
			test = lambda x: x.lower() == cmp
		for i, val in db.items():
			if test(val.get('name')):
				ret.append(val)

	out = []
	if len(ret)>0:
		if qs_db == 'items':
			out = formatMRIDrow(ret)
		if qs_db == 'locations':
			out = formatMRODrow(ret)
		if qs_db == 'npcs':
			out = formatMRNDrow(ret)
	
	resp('200 OK', [('Content-Type', 'application/json')])
	return orjson.dumps(out)


def mrdb_detail_body(body,title,i,name):
	return '''<!DOCTYPE html>
	<html>
		<head>
			<title>{title}</title>
			<link rel='stylesheet' href='/gazproj/styles.css'>
		</head>
		<body>
			<div class="header">
				<div class="prev-link"><a href="?id={id_prev}">&lt;&lt; {id_prev}</a></div>
				<div class="item-name">{id} - {item_name}</div>
				<div class="next-link link"><a href="?id={id_next}">{id_next} &gt;&gt;</a></div>
			</div>
			{body}
			<script>
			const copyConfig = (event) => {{
				const tgt = event.currentTarget.data('txtarea');
				const val = document.querySelector(`textarea.config[data-txtarea="${{tgt}}"]`).value;
				navigator.clipboard.writeText(val);
				tgt.classList.add('copied');
				tgt.textContent = 'Copied!';
				setTimeout(()=>{{tgt.classList.remove('copied'); tgt.textContent = 'Copy';}}, 2500);
			}};
			document.querySelectorAll('.copy-config').forEach(el=>el.addEventListener('click', copyConfig));
			</script>
		</body>
	</html>'''.format(title=title, body=body, id=i, item_name=name, id_prev=i-1, id_next=i+1)

@r('^/mrid/detail')
def route_mrid_detail(env, resp):
	qs = parse_qs(env.get('QUERY_STRING',''))
	i = qs.get('id')
	out = None
	title = 'MRID detail'
	if i is None:
		out = '<div class="error">Please pass in an integer ID with ?id=#</div>'
	else:
		try:
			i = int(i[0])
		except (ValueError,TypeError):
			out = '<div class="error">Please pass in an integer ID with ?id=#</div>'

	if out is None:
		cache = rscache_data['items'].get(i)
		alog = rscache_data['alog'].get(i)
		title = f'{i} - MRID detail'
		name_str = '@unknown@'
		if cache is None:
			cachestr = 'failed to load cache json'
		else:
			name_str = cache.get('name', '@unknown@')
			cachestr = inputhtmlsafe(orjson.dumps(cache, option=INDSORT).decode())
		if type(alog) == dict:
			alogstr = inputhtmlsafe(orjson.dumps(alog, option=INDSORT).decode())
		else:
			alogstr = 'failed to load alog json'
		out = '''
		<table>
			<tr>
				<th>Cache JSON<br><span class="button copy-config" data-txtarea="cache">Copy</span></td>
				<th>ALOG JSON (if available)<br><span class="button copy-config" data-txtarea="alog">Copy</span></td>
				<th>Inventory Icon (GEDB)</td>
				<th>DII (model viewer)</td>
			</tr>
			<tr>
				<td class="mrdb-detail-json"><textarea class="config" data-txtarea="cache" readonly>{cache}</textarea></td>
				<td class="mrdb-detail-json"><textarea class="config" data-txtarea="alog" readonly>{alog}</textarea></td>
				<td class="mrdb-detail-icon" style="text-align:center;"><img src="/gazproj/icons/png/{id}.png"/></td>
				<td class="mrdb-detail-dii" style="text-align:center;"><a href="https://r2.weirdgloop.org/rs-render/dii/{id}.png" target="_blank" rel="noopener noreferrer"><img src="https://r2.weirdgloop.org/rs-render/dii/{id}.png" /></a></td>
			</tr>
		</table>'''.format(
			id=t,
			cache=cache_str,
			alog=alog_str
		)
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return mrdb_detail_body(out,title,t,name_str)

@r('^/mrnd/detail')
def route_mrnd_detail(env, resp):
	qs = parse_qs(env.get('QUERY_STRING',''))
	i = qs.get('id')
	out = None
	title = 'MRND detail'
	if i is None:
		out = '<div class="error">Please pass in an integer ID with ?id=#</div>'
	else:
		try:
			i = int(i[0])
		except (ValueError,TypeError):
			out = '<div class="error">Please pass in an integer ID with ?id=#</div>'

	if out is None:
		cache = rscache_data['npcs'].get(i)
		bestiary = rscache_data['bestiary'].get(i)
		title = f'{i} - MRND detail'
		name_str = '@unknown@'
		if cache is None:
			cachestr = 'failed to load cache json'
		else:
			name_str = cache.get('name', '@unknown@')
			cachestr = inputhtmlsafe(orjson.dumps(cache, option=INDSORT).decode())
		if type(bestiary) == dict:
			bestiarystr = inputhtmlsafe(orjson.dumps(bestiary, option=INDSORT).decode())
		else:
			bestiarystr = 'failed to load bestiary json'
		out = '''
		<table>
			<tr>
				<th>Cache JSON<br><span class="button copy-config" data-txtarea="cache">Copy</span></td>
				<th>Bestiary JSON (if available)<br><span class="button copy-config" data-txtarea="bestiary">Copy</span></td>
				<th>Image (model viewer)</td>
			</tr>
			<tr>
				<td class="mrdb-detail-json"><textarea class="config" data-txtarea="cache" readonly>{cache}</textarea></td>
				<td class="mrdb-detail-json"><textarea class="config" data-txtarea="bestiary" readonly>{bestiary}</textarea></td>
				<td class="mrdb-detail-dii" style="text-align:center;"><a href="https://r2.weirdgloop.org/rs-render/npc/{id}.png" target="_blank" rel="noopener noreferrer"><img src="https://r2.weirdgloop.org/rs-render/npc/{id}.png" /></a></td>
			</tr>
		</table>'''.format(
			id=t,
			cache=cache_str,
			bestiary=bestiary_str
		)
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return mrdb_detail_body(out,title,t,name_str)

@r('^/mrod/detail')
def route_mrod_detail(env, resp):
	qs = parse_qs(env.get('QUERY_STRING',''))
	i = qs.get('id')
	out = None
	title = 'MROD detail'
	if i is None:
		out = '<div class="error">Please pass in an integer ID with ?id=#</div>'
	else:
		try:
			i = int(i[0])
		except (ValueError,TypeError):
			out = '<div class="error">Please pass in an integer ID with ?id=#</div>'

	if out is None:
		cache = rscache_data['locations'].get(i)
		title = f'{i} - MRND detail'
		name_str = '@unknown@'
		if cache is None:
			cachestr = 'failed to load cache json'
		else:
			name_str = cache.get('name', '@unknown@')
			cachestr = inputhtmlsafe(orjson.dumps(cache, option=INDSORT).decode())
		out = '''
		<table>
			<tr>
				<th>Cache JSON<br><span class="button copy-config" data-txtarea="cache">Copy</span></td>
				<th>Image (model viewer)</td>
			</tr>
			<tr>
				<td class="mrdb-detail-json"><textarea class="config" data-txtarea="cache" readonly>{cache}</textarea></td>
				<td class="mrdb-detail-dii" style="text-align:center;"><a href="https://r2.weirdgloop.org/rs-render/loc/{id}.png" target="_blank" rel="noopener noreferrer"><img src="https://r2.weirdgloop.org/rs-render/loc/{id}.png" /></a></td>
			</tr>
		</table>'''.format(
			id=t,
			cache=cache_str
		)
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return mrdb_detail_body(out,title,t,name_str)

@r(r'^/icons/png/\d{1,5}\.png$')
def route_icons_png(env, resp):
	path = '/home/gaz/iteminfobox/inventory/'+ environ.get('PATH_INFO')[1:]
	return serve_file(resp,path,'image/png')

@r(r'^/recipe$')
def page(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return '<html><head><title>infobox recipe generator</title></head><body>Hi! This is where you can generate some infobox recipes - if things don\'t seem to work, let me know. Append the item ID of the item to the end of the url, e.g. <a href="recipe/361">/recipe/361</a>. You can find the item ID in the infobox item on the page.\n\nThis isn\'t perfect so you will need to put in some manual effort to make sure infoboxes are correct.</body></html>'