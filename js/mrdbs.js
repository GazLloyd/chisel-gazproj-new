const rowDef = window.rowDef;
const dbtype = window.dbtype;
const gbid = x=>document.getElementById(x);
const geturl = (base, params) => {
	const url = new URL(base);
	const search = new URLSearchParams(params);
	url.search = search.toString();
	return url.toString();
};
const e = (t, params) => {
	const el = document.createElement(t);
	if (!(params === undefined)) {
		if (params.text) {
			el.textContent = params.text;
		} else if (params.html) {
			el.innerHTML = params.html;
		}
		if (params.class) {
			el.className = params.class;
		}
		if (params.id) {
			el.id = params.id;
		}
		if (params.attr) {
			for (let [k, v] of Object.entries(params.attr)) {
				el.setAttribute(k, v);
			}
		}
		if (params.append) {
			el.append(...params.append);
		}
	}
	return el;
};

const q = gbid('mrdb-search'),
	goButton = gbid('mrdb-go'),
	currentList = gbid('mrdb-currentlist'),
	statusEl = gbid('mrdb-status'),
	tbody = gbid('mrdb-body');
const rxRecent = /^recent(\d+)$/i, rxEnum = /^enum(\d+)$/i;
const addRow = (data)=>{
	const row = e('tr', {class:'mrdb-row', attr:{'data-id':data.id}});

	for (const def of rowDef) {
		let td, deftxt = data[def];
		if (Array.isArray(deftxt)) deftxt = deftxt.join(', ');
		td = e('td', {class:'mrdb-cell-'+def, text:deftxt});
		if (typeof(def)==='object') {
			if (typeof(def.format)==='function') {
				td.innerHTML='';
				let contents = def.format(data);
				if (Array.isArray(contents)) td.append(...contents);
				else td.append(contents);
			}
			if (def.class !== undefined) td.classList.add(def.class);
		}
	}
	if (data.noted) {
		row.classList.add('noted');
	}

	tbody.append(row);
};
const doQuery = async (query)=>{
	q.disabled=true;
	goButton.disabled=true;
	if (!Array.isArray(query)) {
		query = query.split('¦');
	}
	if (query.length===0) {
		q.disabled=false;
		goButton.disabled=false;
		return;
	}
	const endstrs = [];
	const sp = URLSearchParams([['db', dbtype]]);
	for (const qu of query) {
		let endstr = qu;
		qu = qu.trim();
		let val = rxRecent.exec(qu);
		if (val !== null) {
			endstr = 'the most recent '+val[1];
		} else {
			val = rxEnum.exec(qu);
			if (val !== null) {
				endstr = 'enum '+val[1];
			}
		}
		sp.append('q', id);
		endstrs.push(endstr);
	}
	const resp = await fetch('mrdb/get&'+sp.toString(), {method: 'GET'});
	if (resp.status !== 200) {
		statusEl.textContent = 'failed to fetch from server';
		statusEl.classList.add('mrdb-error');
	} else {
		statusEl.textContent = '';
		statusEl.classList.remove('mrdb-error');
		const data = await resp.json();
		const addedRows = data.map(makeRow);
		if (currentList.textContent === '') currentList.textContent = endstrs.join(', ');
		else currentList.textContent += ', ' + endstrs.join(', ');
	}
	q.disabled=false;
	goButton.disabled=false;
	return sp;
};
const submit = async ()=>{
	const newq = await doQuery(q.value);
	const queries = new URLSearchParams(window.location.search);
	newq.getAll('q').forEach(i=>queries.append('q', i));
	window.history.replaceState(null, '', '?'+queries.toString());
	q.value='';
};
const init = async ()=>{
	// setup events
	// keyup for enter -> submit
	q.addEventListener('keyup', e=>{
		if (e.key === 'Enter') submit();
	});
	// go button
	goButton.addEventListener('click', submit);

	// noted checkbox
	let checkbox = gbid('mrdb-noted');
	if (checkbox !== null) {
		checkbox.addEventListener('input', e=>{
			tbody.classList.toggle('hidenoted');
			window.localStorage.setItem('hideNoted', tbody.parentElement.classList.contains('hidenoted'))
		});
	if (window.localStorage.getItem('hideNoted') === 'false') tbody.classList.remove('hidenoted');

	}
	// models checkbox
	checkbox = gbid('mrdb-models');
	if (checkbox !== null) {
		checkbox.addEventListener('input', e=>{
			tbody.parentElement.classList.toggle('showmodel');
			window.localStorage.setItem('showmodel', tbody.parentElement.classList.contains('showmodel'))
		});
		if (window.localStorage.getItem('showmodel') === 'false') tbody.parentElement.classList.add('showmodel');
	}
	// clear buton
	gbid('mrdb-clear').addEventListener('input', e=>{
		tbody.innerHTML='';
		currentList.innerHTML='';
		statusEl.innerHTML='';
		statusEl.classList.remove('mrdb-error');
	});

	// initial query
	const params = new URLSearchParams(window.location.search);
	const qs = params.getAll('q');
	if (qs.length>0) {
		await doQuery();
	} else {
		await doQuery(['recent50']);
	}
	for (const hl of params.getAll('h')) {
		document.querySelectorAll(`.mrdb-row[data-id="${hl}"]`).forEach(el=>el.classList.add('hilite'));
	}
};