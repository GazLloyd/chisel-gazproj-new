# stdlib imports
import os
import sys
import orjson
from time import strftime, gmtime, time
from urllib.parse import parse_qs, urlsplit
from re import compile as recomp, IGNORECASE
import sqlite3

# custom imports
sys.path.append('/tools/gazproj/') # make sure this is on PATH
os.chdir('/tools/gazproj')
print('current working directory', os.getcwd())
from wsgirouter import Router, RouteNotFound
import tabulate
#import infobox
# maximum size of a chunk to read when serving static files
# int
CHUNKSIZE=1024*1024
# map of mimetype to a list of tuples of (route regex, static filepath)
# these files are served as-is, no alterations
# dict[mimetype, list[tuple[route,filepath]]]
STATIC_SERVES = {
	'text/html; charset=utf-8': [
		('/', 'html/index.html'), # homepage
		('/mrid', 'html/mrid.html'), #mrdbs
		('/mrod', 'html/mrod.html'), #mrdbs
		('/mrnd', 'html/mrnd.html'), #mrdbs
		('/usercontribsdiff', 'html/usercontribsdiff.html'),
		('/datasrc', 'html/datasrcrender.html'),
		('/tally', 'html/tally.html'),
		('/gazbot', 'html/gazbot.html'),
		('/recipe', 'html/recipe.html'),
		('/cache', 'html/cache.html'),
		('/cache/tabulate', 'html/tabulate.html'),
		('/alt1/timers', 'alt1/timer/timer.html'),
		('/alt1/contracts', 'alt1/constructioncontracts/contracts.html'),
		('/alt1/rocks', 'alt1/rocks/rocks.html'),
		('/alt1/transcribe', 'alt1/transcriber/index.html'),
		('/pkmn/gs', 'html/pkmn.html'),
		('/pkmn/box9', 'html/box9guide.html'),
		('/pkmn/plza', 'html/plzashiny.html')
	],
	'text/css': [
		('/styles.css', 'styles/styles.css'),
		('/mrid.css', 'styles/styles.css'),
		('/pkmn.css', 'styles/pkmn.css'),
	],
	'text/javascript': [
		('/mrdbs.js', 'js/mrdbs.js'),
		('/alt1/contracts/contracts.bundle.js', 'alt1/constructioncontracts/index.bundle.js'),
		('/alt1/transcribe/main.js', 'alt1/transcriber/main.js'),
	],
	'application/json': [
		('/gazbot/status_rs', '/home/gaz/gazgebot/GazGEBot/config/rs_ge.json'),
		('/gazbot/status_os', '/home/gaz/gazgebot/GazGEBot/config/os_ge.json'),
		('/gazbot/rs_dump.json', '/home/gaz/gazgebot/GazGEBot/rs_dump.json'),
		('/gazbot/os_dump.json', '/home/gaz/gazgebot/GazGEBot/os_dump.json'),
		('/alt1/timerconfig.json', 'alt1/timer/timerconfig.json'),
		('/alt1/contractsconfig.json', 'alt1/constructioncontracts/contractsconfig.json'),
		('/alt1/transcribe/appconfig.json', 'alt1/transcriber/appconfig.json'),
		('/alt1/rocksconfig.json', 'alt1/rocks/rocksconfig.json'),
	],
	'image/png': [
		('/alt1/transcribe/RSWikiIcon.png', 'alt1/transcriber/RSWikiIcon.png'),
		('/alt1/nischeckbox.png', 'alt1/nischeckbox.png'),
		('/alt1/nischeckbox-checked.png', 'alt1/nischeckbox-checked.png'),
		('/rsw.png', 'img/rsw.png'),
		('/osrsw.png', 'img/osrsw.png'),
		('/wowee.png', 'img/wowee.png'),
		('/meta.png', 'img/meta.png'),
		('/rsc.png', 'img/rsc.png'),
		('/rsptbr.png', 'img/rsptbr.png'),
		('/glorp.png', 'img/glorp.png'),
		('/weirdglorp.png', 'img/weirdglorp.png')
	]
}

# list of routes that return a 301 redirect to another page
REDIRECT_301s = [
	(r'^/mrid/$', '/gazproj/mrid'),
	(r'^/mrnd/$', '/gazproj/mrnd'),
	(r'^/mrod/$', '/gazproj/mrod'),
	(r'^/usercontribsdiff/$', '/gazproj/usercontribsdiff'),
	(r'^/datasrc/$', '/gazproj/datasrc'),
	(r'^/tally/$', '/gazproj/tally'),
	(r'^/gazbot/$', '/gazproj/gazbot'),
	(r'^/recipe/$', '/gazproj/recipe'),
	(r'^/cache/$', '/gazproj/cache'),
	(r'^/cache/tabulate/$', '/gazproj/cache/tabulate'),
	(r'^/alt1/timers\.html$', '/gazproj/alt1/timers'),
	(r'^/alt1/contracts\.html$', '/gazproj/alt1/contracts'),
	(r'^/alt1/rocks\.html$', '/gazproj/alt1/rocks'),
	(r'^/alt1/transcribe(\.html|/transcriber2\.html|/index\.html)$', '/gazproj/alt1/transcribe'),
	(r'^/gazbot/status_rs\.json$', '/gazproj/gazbot/status_rs'),
	(r'^/gazbot/status_os\.json$', '/gazproj/gazbot/status_os'),
	(r'^/pkmn/box9(guide|\.html|guide\.html)$', '/gazproj/box9'),
	(r'^/pkmn/plza(shiny|\.html|shiny\.html)$', '/gazproj/pkmn/plza')
]

# override routenotfound behavoir - normally prints the entire attempt tree
def return_empty(self):
	return ''
RouteNotFound.__str__ = return_empty

INDSORT = orjson.OPT_APPEND_NEWLINE|orjson.OPT_INDENT_2|orjson.OPT_SORT_KEYS
def inputhtmlsafe(s):
	return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(u'\xa0', ' ')

# names of the cache files, without the rest of the filepath or .json
# list[str]
RSCACHE_FILENAMES = ['items', 'npcs', 'locations', 'structs', 'dbrows', 'enums', 'achievements', 'quests', 'versions', 'bestiary', 'alog']
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

# sqlite connections
navbox_con = sqlite3.connect('/tools/gazproj/navbox_tracking.sqlite')
sidebar_con = sqlite3.connect('/tools/gazproj/sidebar_tracking.sqlite')

# open a file with utf-8 encoding
# (str filename, str open type) => filehandle
def openu(fn, ot):
	return open(fn, ot ,encoding='utf-8')

# format a time in HH:MM:SS DD MM YY
# (float timestamp) => str
def timeformat(t):
	return strftime("%H:%M:%S %d %B %Y" , gmtime(t))

# returns the formated modified-by time for a file
# (str filename) => str
def modtime(fn):
	return timeformat(os.stat(fn).st_mtime)

# formats a file's size with 1 decimal place
# (str filename) => str
def filesize(fn):
	num = os.stat(fn).st_size
	suffix = 'B'
	for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
		if abs(num) < 1024.0:
			return '%3.1f %s%s' % (num, unit, suffix)
		num /= 1024.0
	return '%.1f %s%s' % (num, 'Yi', suffix)

# load a json file (efficiently with orjson)
# (str filename)=>dict|list
def loadjson(filepath):
	with open(filepath, 'rb') as f:
		return orjson.loads(f.read())

# save a json file (efficiently using orjson)
# optional args: indent - pretty-print the json; sort - sort the keys of dicts in the json
# (str filename, dict|list json, bool indent=false, bool sortkeys=false) => void
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
	rows = []
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
		rows.append('<tr class="{fn}"><td></td><td>{fn}</td><td>{fn_size}</td><td>{fn_mod}</td><td><a href="https://chisel.weirdgloop.org/gazproj/cache/{fn}.json" download>download</a></td><td>{fdiff_size}</td><td><a href="https://chisel.weirdgloop.org/gazproj/cache/{fn}_diff.html">view</a> &bull; <a href="https://chisel.weirdgloop.org/gazproj/cache/{fn}_diff.txt" download>download</a></td></tr>'.format(
			fn=fn,
			fn_size=filesize(f'{RSCACHE_FILEPATH}/{fn}.json'),
			fn_mod=modtime(f'{RSCACHE_FILEPATH}/{fn}.json'),
			fdiff_size=filesize(f'{RSCACHE_FILEPATH}/{fn}_diff.txt')
		))
	with openu('html/index_template.html','r') as ftemp, openu('html/index.html', 'w') as fout:
		fout.write(ftemp.read().format(
			items = modtime(RSCACHE_FILEPATH+'/items.json'),
			alog = modtime(RSCACHE_FILEPATH+'/alog.json'),
			npcs = modtime(RSCACHE_FILEPATH+'/npcs.json'),
			best = modtime(RSCACHE_FILEPATH+'/bestiary.json'),
			objs = modtime(RSCACHE_FILEPATH+'/locations.json')
		))
	with openu('html/cache_template.html', 'r') as ftemp, openu('html/cache.html', 'w') as fout:
		gerows = []
		for f_name in ['rs', 'os']:#, 'rsfsw', 'osfsw']:
			f_file = f'/home/gaz/gazgebot/GazGEBot/{f_name}_dump.json'
			r = '<tr class="{fn}-ge"><td></td><td>{fn}</td><td><a href="https://chisel.weirdgloop.org/gazproj/gazbot/{fn}_dump.json" download>download</a></td><td><a href="https://chisel.weirdgloop.org/gazproj/gazbot/status_{fn}">status_{fn}</a></td></tr>'.format(fn=f_name)
			gerows.append(r)
		fout.write(ftemp.read().format(rows='\n'.join(rows),gerows='\n'.join(gerows)))

# reload the RS cache jsons & remake the html
# () => void
def reloadRSCache():
	global rscache_data, rscache_maxids
	rscache_data = {}
	rscache_maxids = {}
	for fn in RSCACHE_FILENAMES:
		if fn == 'versions':
			rscache_data[fn] = loadjson(f'{RSCACHE_FILEPATH}/{fn}.json')
			rscache_maxids[fn] = -1
		else:
			k = 'id'
			is_alog = False
			if fn == 'alog':
				is_alog = True
				k = 'item_id'
			try:
				rscache_data[fn] = {}
				for x in loadjson(f'{RSCACHE_FILEPATH}/{fn}.json'):
					if not is_alog or (is_alog and type(x) == dict):
						rscache_data[fn][x[k]] = x
			except Exception as e:
				print(f'error loading {fn}.json')
				raise e
			rscache_maxids[fn] = max(rscache_data[fn].keys())
	for x in loadjson(f'{RSCACHE_FILEPATH}/location_examines.json'):
		i = x['id']
		rscache_data['locations'].get(i, {})['examine'] = x['examine']
	for v in rscache_data['alog'].values():
		if type(v) == dict:
			rscache_data['items'].get(v['item_id'], {})['examine'] = v['desc']
	makeDiffHtmls()
	#infobox.load_configs()

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
	ctype = [('Content-Type', mime)]
	if filepath.startswith('alt1/'):
		ctype.append(('Access-Control-Allow-Origin', '*'))
	try:
		with open(filepath, 'rb') as f:
			start_response('200 OK', ctype)
			for ch in filechunks(f):
				yield ch
	except:
		start_response('404 NOT FOUND', ctype)
		yield '404 NOT FOUND'.encode('utf-8')

# setup a static file, adding the route to the router
# (regexstr, str, str) => void
def static_file(route, filepath, mime):
	def serve(env, resp):
		for ch in serve_file(resp, filepath, mime):
			yield ch
	regex = recomp('^'+route+'$')
	application.rules.append(((regex, ['GET'], serve),(route,)))

# setup a http 301, adding the route to the router
# (regexstr, str) => void
def http_301(route, redir_loc):
	def send_301(env, resp):
		resp('301 MOVED PERMANENTLY', [('Location', redir_loc)])
		return b''
	regex = recomp(route)
	application.rules.append(((regex, ['GET'], send_301),(route,)))

# set up the defined static serves
for mimetype, fileroutes in STATIC_SERVES.items():
	for route,filename in fileroutes:
		static_file(route, filename, mimetype)

# set up the redirects
for route,filename in REDIRECT_301s:
	http_301(route, filename)

# setup cache serves
for fn in RSCACHE_FILENAMES:
	static_file(f'/cache/{fn}.json', f'{RSCACHE_FILEPATH}/{fn}.json', 'application/json') #cache file
	static_file(f'/cache/{fn}_diff.txt', f'{RSCACHE_FILEPATH}/{fn}_diff.txt', 'text/plain') #cache diff as plaintext
	static_file(f'/cache/{fn}_diff.html', f'{RSCACHE_FILEPATH}/{fn}_diff.html', 'text/html; charset=utf-8') #cache diff as html

# reload the cache
reloadRSCache()

# MRDB helpers
# get the item's name
# (dict item, any default)=>str|any
def get_item_name(item_cache, dflt=None):
	if item_cache is not None:
		if item_cache.get('name') is not None:
			return item_cache.get('name')
		if item_cache.get('combine_shard_name') is not None:
			return item_cache.get('combine_shard_name')
	return dflt

# get the unnoted item if possible
# (dict item)=>dict
def get_unnoted_item(item_cache):
	notedata = item_cache.get('noteData')
	if notedata is None:
		notedata = item_cache.get('bindLink')
	if notedata is None:
		return None
	return rscache_data['items'].get(notedata)

# remove nulls from a list
# (list)=>list
def stripNulls(l):
	return list(filter(lambda x: not (x is None or x=='null'), l))

# format the MRDB responses
# (list<cache entries> values) => list<dict>
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
	print('formatMRDB_items', len(vals), vals[0:5], len(out), out[0:5])
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
			'actions': stripNulls(cache.get('actions', [])),
			'members_actions': stripNulls(cache.get('members_actions', []))
		}

		bestiary = rscache_data['bestiary'].get(cache.get('id'))
		if type(bestiary) == dict and bestiary.get('contents', '') != 'null':
			if bestiary.get('members') is not None:
				ret['members'] = bestiary.get('members')
			if bestiary.get('description') is not None:
				ret['examine'] = bestiary.get('description')
		out.append(ret)
	print('formatMRDB_npcs', len(vals), vals[0:5], len(out), out[0:5])
	return out

def formatMRDB_locations(vals):
	out = []
	for cache in vals:
		ret = {
			'id': cache.get('id'),
			'name': cache.get('name', ''),
			'members': cache.get('isMembers', ''),
			'examine': cache.get('examine', ''),
			'actions': stripNulls(cache.get('actions', [])),
			'members_actions': [],
			'morphs_1': cache.get('morphs_1'),
			'morphs_2': cache.get('morphs_2')
		}
		for i in range(1,11):
			a = cache.get('members_action_'+str(i))
			if a is not None:
				ret['members_actions'].append(a)
		out.append(ret)
	print('formatMRDB_locations', len(vals), vals[0:5], len(out), out[0:5])
	return out


def get_cmp_func(cmp_val):
	cmp_v = cmp_val.lower()
	def cmp(x):
		return x.lower() == cmp_v
	return cmp
def get_regex_func(re_val):
	print('making regex cmp func', re_val)
	rx = recomp(re_val, IGNORECASE)
	def cmp(x):
		return rx.search(x) is not None
	return cmp

MRDB_FUNCS = {
	'items': formatMRDB_items,
	'npcs': formatMRDB_npcs,
	'locations': formatMRDB_locations
}
MRDB_RXS = {
	'id': recomp(r'(\d+)'),
	'idrange': recomp(r'(\d+)([-+])(\d+)'),
	'recent': recomp(r'recent(\d+)', IGNORECASE),
	'enum': recomp(r'enum(\d+)', IGNORECASE)
}
@r(r'^/mrdb/get$')
def route_mrdb_get(env,resp):
	global rscache_data, rscache_maxids
	qs = parse_qs(env.get('QUERY_STRING',''))
	qs_db = qs.get('db')
	if (not type(qs_db) == list) or len(qs_db) == 0:
		resp('400 ERROR', [('Content-Type', 'application/json')])
		return b'{"error":"invalid mrdb provided"}'
	qs_db = qs_db[0]
	if qs_db not in MRDB_FUNCS:
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
			test = get_regex_func(q[1:-1])
		else:
			test = get_cmp_func(q)
		for i, val in db.items():
			if test(val.get('name', '')):
				ret.append(val)

	out = []
	if len(ret)>0:
		out = MRDB_FUNCS[qs_db](ret)
	
	resp('200 OK', [('Content-Type', 'application/json')])
	return orjson.dumps(out)

# mr[ion]d/detail body - this part is standard
# (str body, str title, int id, str name) => str
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
	</html>'''.format(title=title, body=body, id=i, item_name=name, id_prev=i-1, id_next=i+1).encode('utf-8')

@r(r'^/mrid/detail')
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
			id=i,
			cache=cachestr,
			alog=alogstr
		)
	resp('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return mrdb_detail_body(out,title,i,name_str)

@r(r'^/mrnd/detail')
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
			id=i,
			cache=cachestr,
			bestiary=bestiarystr
		)
	resp('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return mrdb_detail_body(out,title,i,name_str)

@r(r'^/mrod/detail')
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
			id=i,
			cache=cachestr
		)
	resp('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return mrdb_detail_body(out,title,i,name_str)

@r(r'^/icons/png/\d{1,5}\.png$')
def route_icons_png(env, resp):
	path = '/home/gaz/iteminfobox/inventory/'+ env.get('PATH_INFO')[1:]
	for ch in serve_file(resp, path, 'image/png'):
		yield ch

@r(r'^/recipe/\d+$')
def route_recipe(env, resp):
	resp('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return b'Sorry! This route currently not supported - coming soon!'
	itemid = env.get('PATH_INFO')[8:]
	infobox = make_recipe() #TODO
	resp('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return '''<!DOCTYPE html>
	<html>
		<head>
			<title>Infobox Recipe for {itemid}</title>
			<link rel='stylesheet' href='/gazproj/styles.css'>
		</head>
		<body>
			<pre>{infobox}</pre>
		</body>
	</html>'''.format(itemid=itemid, infobox=infobox).encode('utf-8')

@r(r'^/gazbot/rcep\.log$')
def route_gazbot_rceplog(env, resp):
	with open('/home/gaz/gazgebot/GazGEBot/rcmonitor_patrol.log', 'r') as f:
		txt = f.read()
		html = '''
		<!DOCTYPE html>
		<html>
		<head><title>rcep.log</title><link rel='stylesheet' href='/gazproj/styles.css'></head>
		<body>
		<pre>{}</pre>
		</body>
		</html>'''.format(txt)
		resp('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
		return html.encode('utf-8')

@r(r'^/gazbot/rcep_whitelist\.txt$')
def route_gazbot_rcepwhitelist(env, resp):
	with open('/home/gaz/gazgebot/GazGEBot/config/rcmonitor_whitelist.txt', 'r') as f:
		txt = f.read()
		html = '''
		<!DOCTYPE html>
		<html>
		<head><title>rcep_whitelist.txt</title><link rel='stylesheet' href='/gazproj/styles.css'></head>
		<body>
		<pre>{}</pre>
		</body>
		</html>'''.format(txt)
		resp('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
		return html.encode('utf-8')

@r(r'^/img/.*?\.png$')
def route_imgs_folder(env, resp):
	for ch in serve_file(resp, env.get('PATH_INFO')[1:], 'image/png'):
		yield ch

@r(r'^/cache/tabulate/get$')
def route_cache_tabulate_get(env, resp):
	query = env.get('QUERY_STRING')
	query = parse_qs(query)
	t = query.get('type', ['items'])[0]
	t = t.lower().strip()
	if t not in ['items', 'npcs', 'structs', 'locations', 'enums', 'quests', 'achievements', 'dbrows', 'bestiary']:
		resp('400 ERROR',[('Content-Type', 'application/json')])
		return b'{"error": true, "message": "Invalid cache type"}'
	cache = rscache_data[t]
	s = query.get('search', [])
	if len(s) == 0:
		resp('400 ERROR',[('Content-Type', 'application/json')])
		return b'{"error": true, "message": "No search provided"}'
	s = s[0].split(';')
	v = ['id', 'name']
	try:
		v.extend(query.get('view', [''])[0].split(';'))
	except:
		pass
	v = list(filter(lambda x: len(x)>0, map(lambda x: x.strip(), v)))
	s = list(filter(lambda x: len(x)>0, map(lambda x: x.strip(), s)))
	print('tablating:',t,s,v)
	outname = tabulate.main(cache, s, v)
	fname = outname.strip()
	for ch in serve_file(resp, f'/tools/gazproj/tabulatefiles/{fname}.json', 'application/json'):
		yield ch

@application.route('/cache/tabulate/download')
def route_cache_tabulate_download(env, resp):
	query = env.get('QUERY_STRING')
	query = parse_qs(query)
	fname = query.get('file', [])
	if len(fname) == 0:
		resp('404 NOT FOUND', [('Content-Type', 'text/plain')])
		return ''
	fname = fname[0]
	for ch in serve_file(resp, f'/tools/gazproj/tabulatefiles/{fname}.tsv', 'text/plain'):
		yield ch


def track_postdata_helper(obj, key, index=0):
	x = obj.get(key)
	if x is None or type(x) != list:
		return None
	if len(x) < index+1:
		return None
	return x[index]

allowed_track_wikis = (
	'en_rswiki',
	'en_osrswiki',
	'en_rscwiki',
	'en_rsdwwiki',
	'pt_rswiki',
	'en_rsmetawiki',

	'en_mcwiki',
	'cs_mcwiki',
	'de_mcwiki',
	'el_mcwiki',
	'es_mcwiki',
	'fr_mcwiki',
	'hu_mcwiki',
	'id_mcwiki',
	'it_mcwiki',
	'ja_mcwiki',
	'ko_mcwiki',
	'lzh_mcwiki',
	'nl_mcwiki',
	'pl_mcwiki',
	'pt_mcwiki',
	'pt-br_mcwiki',
	'ru_mcwiki',
	'th_mcwiki',
	'tr_mcwiki',
	'uk_mcwiki',
	'zh_mcwiki'
)
allowed_referer = (
	'runescape.wiki',
	'oldschool.runescape.wiki',
	'classic.runescape.wiki',
	'dragonwilds.runescape.wiki',
	'pt.runescape.wiki',
	'meta.runescape.wiki',

	'minecraft.wiki',
	'cs.minecraft.wiki',
	'de.minecraft.wiki',
	'el.minecraft.wiki',
	'es.minecraft.wiki',
	'fr.minecraft.wiki',
	'hu.minecraft.wiki',
	'id.minecraft.wiki',
	'it.minecraft.wiki',
	'ja.minecraft.wiki',
	'ko.minecraft.wiki',
	'lzh.minecraft.wiki',
	'nl.minecraft.wiki',
	'pl.minecraft.wiki',
	'pt.minecraft.wiki',
	'pt-br.minecraft.wiki',
	'ru.minecraft.wiki',
	'th.minecraft.wiki',
	'tr.minecraft.wiki',
	'uk.minecraft.wiki',
	'zh.minecraft.wiki'
)
def is_rsw(environ):
	try:
		ref = environ.get('HTTP_REFERER')
		if ref is not None:
			refurl = urlsplit(ref)
			return refurl.netloc in allowed_referer
	except:
		pass
	return True #just to be safe

@r(r'^/track/navbox$', methods=['POST'])
def route_track_navbox(env, resp):
	if not is_rsw(env):
		print(f'rejecting NAVBOX from referer {env.get("HTTP_REFERER")}')
		resp('403 FORBIDDEN', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
		return b'{"success":false, "reason": "wiki not allowed"}'
	raw_data = env.get('wsgi.input').read()
	try:
		post_data = parse_qs(raw_data.decode())
		pagename = track_postdata_helper(post_data, 'page', 0)
		navbox = track_postdata_helper(post_data, 'navbox', 0)
		href = track_postdata_helper(post_data, 'link', 0)
		wiki = track_postdata_helper(post_data, 'wiki', 0)
		link_type = track_postdata_helper(post_data, 'type', 0)
		click_type = track_postdata_helper(post_data, 'click', 0)
		t = time()
		if wiki not in allowed_track_wikis:
			print(f'rejecting NAVBOX from db {wiki}')
			resp('403 FORBIDDEN', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
			return b'{"success":false, "reason": "wiki not allowed - w"}'
		if pagename is None or navbox is None or href is None or link_type is None or click_type is None:
			print('failed NAVBOX', raw_data, post_data, pagename, navbox, href, wiki, link_type, click_type)
			resp('500 ERROR', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
			return orjson.dumps({'success':False, 'raw_data':str(raw_data), 'parsed_data': post_data, 'reason': 'required field is none'})
		navbox_con.execute('INSERT INTO clicks (timestamp, page_name, navbox_name, link_href, link_type, click_type, wiki) VALUES (?, ?, ?, ?, ?, ?, ?)', (t, pagename, navbox, href, link_type, click_type, wiki))
		navbox_con.commit()
		resp('200 OK', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
		return b'{"success":true}'

	except Exception as e:
		resp('500 ERROR', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
		return orjson.dumps({'success':False, 'raw_data':str(raw_data), 'reason': str(e)})
	
@r(r'^/track/sidebar$', methods=['POST'])
def route_track_sidebar(env, resp):
	if not is_rsw(env):
		print(f'rejecting SIDEBAR from referer {env.get("HTTP_REFERER")}')
		resp('403 FORBIDDEN', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
		return b'{"success":false, "reason": "wiki not allowed"}'
	raw_data = env.get('wsgi.input').read()
	try:
		post_data = parse_qs(raw_data.decode())
		pagename = track_postdata_helper(post_data, 'page', 0)
		wiki = track_postdata_helper(post_data, 'wiki', 0)
		href = track_postdata_helper(post_data, 'link', 0)
		click_type = track_postdata_helper(post_data, 'click', 0)
		t = time()
		if wiki not in allowed_track_wikis:
			print(f'rejecting SIDEBAR from db {wiki}')
			resp('403 FORBIDDEN', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
			return b'{"success":false, "reason": "wiki not allowed"}'
		if pagename is None or wiki is None or href is None or click_type is None:
			print('failed SIDEBAR', raw_data, post_data, pagename, wiki, href, click_type)
			resp('500 ERROR', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
			return orjson.dumps({'success':False, 'raw_data':str(raw_data), 'parsed_data': post_data, 'reason': 'required field is none'})
		sidebar_con.execute('INSERT INTO clicks (timestamp, page_name, link_href, click_type, wiki) VALUES (?, ?, ?, ?, ?)', (t, pagename, href, click_type, wiki))
		sidebar_con.commit()
		resp('200 OK', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
		return b'{"success":true}'

	except Exception as e:
		resp('500 ERROR', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
		return orjson.dumps({'success':False, 'raw_data':str(raw_data), 'reason': str(e)})


@r(r'^/alt1/imgs/[A-Za-z ]+\.png$')
def route_alt1_imgs(env, resp):
	filename = env.get('PATH_INFO')[11:]
	for ch in serve_file(resp, f'alt1/constructioncontracts/{filename}', 'image/png'):
		yield ch

@r(r'^/alt1/contracts/data$', methods=['POST'])
def route_alt1_submit(env, resp):
	try:
		body = json.loads(env.get('wsgi.input').read())
		with open('/home/gaz/alt1stuff/constructioncontractsinfo.txt', 'a') as f:
			f.write('\n{}\t{}\t{}'.format(time(), body.get('location', '@missing@'), ','.join(body.get('furniture', ['@missing@'])) ))
			resp('200 OK', [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')])
			return b'{"success":true}'
	except:
		pass
	resp('400', [('Content-Type', 'application/json')])
	return  b'{"success":false}'

@r(r'^/pkmn/[A-Za-z0-9_\-]+\.(png|jpg)$')
def route_pkmn_images(env, resp):
	imgpath = f'img/{env.get("PATH_INFO")}'
	mime = 'image/png'
	if imgpath[:-3] == 'jpg':
		mime = 'image/jpeg'
	#print('pkmn images', imgpath, mime)
	for ch in serve_file(resp, imgpath, mime):
		yield ch	

@r(r"^/test$", methods=['GET','POST'])
def route_test(env, resp):
	body = [ '%s: %s' %(k,v) for k,v in sorted(env.items()) ]
	body.append('parsed_query_string: %s' % parse_qs(env.get('QUERY_STRING')))
	if 'wsgi.input' in env:
		try:
			data = env.get('wsgi.input').read().decode()
			body.append('\nData:')
			body.append(data)
			body.append(str(parse_qs(data)))
		except:
			body.append('failed to read any data')
	body = '\n'.join(body)
	body = f'<pre>{body}</pre>'
	resp('200 OK', [('Content-Type', 'text/html'), ('Access-Control-Allow-Origin', '*')])
	return body.encode('utf-8')

@r(r'^/gazbot/(os|rs)_dump\.json\d{1,6}\.json$')
def route_bad_dump(env,resp):
	resp('400 BAD REQUEST', [])
	return b''