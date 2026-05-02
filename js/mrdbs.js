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

const rxRecent = /^recent(\d+)$/i, rxEnum = /^enum(\d+)$/i;
const addRow = (tbody,data)=>{
	const row = e('tr', {class:'mrdb-row', attr:{'data-id':data.id}});

	for (const def of rowDef) {
		let td, deftxt = data[def];
		if (Array.isArray(deftxt)) deftxt = deftxt.join(', ');
		let classname = def;
		if (typeof(def)==='object') classname = def.name;
		td = e('td', {class:'mrdb-cell-'+classname, text:deftxt});
		if (typeof(def)==='object') {
			if (typeof(def.format)==='function') {
				td.innerHTML='';
				let contents = def.format(data);
				if (Array.isArray(contents)) td.append(...contents);
				else td.append(contents);
			}
			if (def.class !== undefined) td.classList.add(def.class);
		}
		row.append(td);
	}
	if (data.noted) {
		row.classList.add('noted');
	}

	tbody.append(row);
	return row;
};
const toggleDisableForm = (isDisabled)=>{
	const goButton = gbid('mrdb-go'), q = gbid('mrdb-search');
	if (isDisabled) {
		q.setAttribute('disabled', '');
		goButton.setAttribute('disabled', '');
	} else {
		q.removeAttribute('disabled');
		goButton.removeAttribute('disabled');
	}
};
const doQuery = async (query)=>{
	const currentList = gbid('mrdb-currentlist'), statusEl = gbid('mrdb-status');
	toggleDisableForm(true);
	if (!Array.isArray(query)) {
		query = query.split('¦');
	}
	if (query.length===0) {
		toggleDisableForm(false);
		return;
	}
	const endstrs = [];
	const sp = new URLSearchParams([['db', dbtype]]);
	for (let qu of query) {
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
		sp.append('q', qu);
		endstrs.push(endstr);
	}
	const resp = await fetch('mrdb/get?'+sp.toString(), {method: 'GET'});
	if (resp.status !== 200) {
		statusEl.textContent = 'failed to fetch from server';
		statusEl.classList.add('mrdb-error');
	} else {
		const tbody = gbid('mrdb-body');
		statusEl.textContent = '';
		statusEl.classList.remove('mrdb-error');
		const data = await resp.json();
		const addedRows = data.map(x=>addRow(tbody,x));
		if (currentList.textContent === '') currentList.textContent = endstrs.join(', ');
		else currentList.textContent += ', ' + endstrs.join(', ');
	}
	toggleDisableForm(false);
	return sp;
};
const submit = async ()=>{
	const q = gbid('mrdb-search');
	const newq = await doQuery(q.value);
	const queries = new URLSearchParams(window.location.search);
	newq.getAll('q').forEach(i=>queries.append('q', i));
	window.history.replaceState(null, '', '?'+queries.toString());
	q.value='';
};
const init = async ()=>{
	const q = gbid('mrdb-search'),
		goButton = gbid('mrdb-go'),
		currentList = gbid('mrdb-currentlist'),
		statusEl = gbid('mrdb-status'),
		tbody = gbid('mrdb-body')
	// setup events
	// keyup for enter -> submit
	q.addEventListener('keyup', e=>{
		if (e.key === 'Enter') submit();
	});
	// go button
	goButton.addEventListener('click', submit);

	// noted checkbox
	let notecheckbox = gbid('mrdb-noted');
	if (notecheckbox !== null) {
		notecheckbox.addEventListener('input', e=>{
			tbody.classList.toggle('hidenoted', notecheckbox.checked);
			window.localStorage.setItem('hideNoted', tbody.parentElement.classList.contains('hidenoted'))
		});
	if (window.localStorage.getItem('hideNoted') === 'false') tbody.classList.remove('hidenoted');

	}
	// models checkbox
	let modelcheckbox = gbid('mrdb-models');
	if (modelcheckbox !== null) {
		modelcheckbox.addEventListener('input', e=>{
			tbody.parentElement.classList.toggle('showmodel', modelcheckbox.checked);
			window.localStorage.setItem('showmodel', tbody.parentElement.classList.contains('showmodel'))
		});
		if (window.localStorage.getItem('showmodel') === 'true') tbody.parentElement.classList.add('showmodel');
	}
	// clear buton
	gbid('mrdb-clear').addEventListener('click', e=>{
		tbody.innerHTML='';
		currentList.innerHTML='';
		statusEl.innerHTML='';
		statusEl.classList.remove('mrdb-error');
		window.history.replaceState(null, '', '?');
	});

	// initial query
	const params = new URLSearchParams(window.location.search);
	const qs = params.getAll('q');
	if (qs.length>0) {
		await doQuery(qs);
	} else {
		await doQuery(['recent50']);
	}
	for (const hl of params.getAll('h')) {
		document.querySelectorAll(`.mrdb-row[data-id="${hl}"]`).forEach(el=>el.classList.add('hilite'));
	}
};
window.setTimeout(init, 10);