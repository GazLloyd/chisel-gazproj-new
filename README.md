# Gazproj on Chisel

This is the code that runs https://chisel.weirdgloop.org/gazproj and all routes within.

The main script is gazproj.py

# Design decisions

There reason for this project existing:

* It is part of ongoing efforts to get chisel tools into version control
* Gazproj was very old, messy, and inefficient
* Gazproj ran on python2 which made it made it insecure and limited
  * This ultimately forced the change, as we upgraded ubuntu version to 24.04, which does not run python2 at all.

There are various other decisions made through the process of writing the script, documented here - if something is still confusing, feel free to contact me and I'll add a line.

* Using orjson: much faster and more efficient than standard library json, especially given we are regularly dealing with large JSON files from the game cache.
* Keeping cache in memory: A little harsh on RAM but way faster for individual queries, and generally we only update caches weekly so we don't need to keep reloading them. I am also endeavouring for this to be the only place the caches are loaded in full - altering other chisel tools to be integrated with gazproj, or to query gazproj for info.
* Building various HTML files ahead of time: another attempt to move load times from on-request to on-load; prior behaviour was to build the [gazproj/cache](https://chisel.weirdgloop.org/gazproj/cache) page and diffs whenever they were requested. This is unnecessary, since the cache files only change weekly.
* Chunking files: reducing memory overhead for serving files, especially large ones.
* Static serves: reduce code repetition by just defining mimetypes, routes, and the file to serve. Not quite a one-size-fits-all approach but works really well for simple files. There is room for a regex-to-regex approach to serve simple routes in future (eg the `^/icons/png/\d{1,5}.png$` route)
* tabulate.py as a separate file: It was always a separate file, which ran under python3 via a subprocess; it is now integrated to take advantage of the cached-cache. I didn't think it necessarily needed to be completely merged in.
* navbox/sidebar tracking: Data sent by [gadget-navbox-tracking](https://runescape.wiki/w/MediaWiki:Gadget-navbox-tracking.js) and [gadget-sidebar-tracking](https://runescape.wiki/w/MediaWiki:Gadget-sidebar-tracking.js) on RSW and OSRSW. Turns out a handful of other wikis have copied the scripts without understanding them! So now it specifically filters out other wikis. I decided to allow MCW, though.
* alt1 tools: Only small projects are stored in this repo. Larger projects are elsewhere and symlinked ([Construction contracts](https://github.com/GazLloyd/ConstructionContractsAlt1) and [RSWTranscriber](https://github.com/GazLloyd/RSWikiTranscriber))

# Routes overview
Taking the base URL as `https://chisel.weirdgloop.org/gazproj`
* [`/`](https://chisel.weirdgloop.org/gazproj) root, html created on load
* [`/styles.css`](https://chisel.weirdgloop.org/gazproj/styles.css) - generalised styles used all over gazproj
* [`/mrid`](https://chisel.weirdgloop.org/gazproj/mrid), [`/mrnd`](https://chisel.weirdgloop.org/gazproj/mrnd), [`/mrod`](https://chisel.weirdgloop.org/gazproj/mrod) - minimal runescape databases of items, npcs, and objects/scenery. These files contain config used by the general script.
  * [`/mrid/detail`](https://chisel.weirdgloop.org/gazproj/mrid/detail?id=4151), [`/mrnd/detail`](https://chisel.weirdgloop.org/gazproj/mrnd/detail?id=1615), [`/mrod/detail`](https://chisel.weirdgloop.org/gazproj/mrod/detail?id=118999) - detail about an entry from the databases
* [`/mrdbs.js`](https://chisel.weirdgloop.org/gazproj/mrdbs.js) - javascript for mrid/mrnd/mrod, using config from the individual files.
* [`/icons/png/[id].png`](https://chisel.weirdgloop.org/gazproj/icons/png/4151.png) - item icons grabbed from the [GEDB](https://secure.runescape.com/m=itemdb_rs/) (with some basic editing)
* [`/cache`](https://chisel.weirdgloop.org/gazproj/cache) - overview of cache files
  * [`/cache/items_diff.html`](https://chisel.weirdgloop.org/gazproj/cache/items_diff.html) etc - HTML view of diff files, created at load
  * [`/cache/items_diff.txt`](https://chisel.weirdgloop.org/gazproj/cache/items_diff.txt) etc - download of diff txt file
  * [`/cache/items.json`](https://chisel.weirdgloop.org/gazproj/cache/items.json) etc - download of full cache json file
  * [`/cache/tabulate`](https://chisel.weirdgloop.org/gazproj/cache/tabulate) - tabulate information from cache files
    * `/cache/tabulate/get` - perform a tabulation & return the resulting JSON
    * `/cache/tabulate/download` - download a TSV of a tabulation
      * TODO: make the javascript on the tabulate.html page do this instead
* [`/[filename].png`](https://chisel.weirdgloop.org/gazproj/weirdglorp.png) - a handful of files used on gazproj pages or by gazbot-discord.
* [`/gazbot`](https://chisel.weirdgloop.org/gazproj/gazbot) - status information about the runs of Gaz GEBot
  * [`/gazbot/status_rs`](https://chisel.weirdgloop.org/gazproj/gazbot/status_rs), [`/gazbot/status_os`](https://chisel.weirdgloop.org/gazproj/gazbot/status_os) - status JSON of the runs
  * [`/gazbot/rs_dump.json`](https://chisel.weirdgloop.org/gazproj/gazbot/rs_dump.json), [`/gazbot/os_dump.json`](https://chisel.weirdgloop.org/gazproj/gazbot/os_dump.json) - full dump of all the information Gaz GEBot gathers (see also [RuneScape:Grand Exchange Market Watch/Usage and APIs](https://runescape.wiki/w/RuneScape:Grand_Exchange_Market_Watch/Usage_and_APIs))
  * `/gazbot/rcep.log` - RecentChanges Emoji Patrol log (logged by gazbot-discord)
  * `/gazbot/rcep_whitelist.txt` - RecentChanges Emoji Patrol whitelist
* `/track/navbox`, `/track/sidebar` - endpoint that tracks clicks from [gadget-navbox-tracking](https://runescape.wiki/w/MediaWiki:Gadget-navbox-tracking.js) and [gadget-sidebar-tracking](https://runescape.wiki/w/MediaWiki:Gadget-sidebar-tracking.js) on RSW and OSRSW
* `/alt1` - all alt1 tools go under here
  * [`/alt1/timers`](https://chisel.weirdgloop.org/gazproj/alt1/timers) - simple timer tool (WIP)
  * [`/alt1/rocks`](https://chisel.weirdgloop.org/gazproj/alt1/rocks) - strange and golden rock tracker
    * `/alt1/rocksconfig.json` - appconfig to install the app
  * [`/alt1/contracts`](https://chisel.weirdgloop.org/gazproj/alt1/contracts) - Construction contracts tool ([github](https://github.com/GazLloyd/ConstructionContractsAlt1))
    * `/alt1/contractsconfig.json` - appconfig to install the app
    * `/alt1/contracts/contracts.bundle.js` - compiled javascript for the app
    * `/alt1/imgs/[filename].png` - images for the app
    * `/alt1/contracts/data` - tracks info from construction contracts app. I don't remember why I wanted this.
  * [`/alt1/transcribe`](https://github.com/GazLloyd/RSWikiTranscriber) - transcriber tool ([github](https://github.com/GazLloyd/RSWikiTranscriber))
    * `/alt1/transcribe/appconfig.json` - appconfig to install the app
    * `/alt1/transcribe/main.js` - compiled javascript for the app
    * `/alt1/transcribe/RSWikiIcon.png` - image for the app
  * `/alt1/nischeckbox.png`, `/alt1/nischeckbox-checked.png`- checkbox image for apps
* `/pkmn` - various Pokémon things I wrote go here
  * [`/pkmn/box9`](https://chisel.weirdgloop.org/gazproj/pkmn/box9) - guide to an ACE in Pokémon Gold/Silver, focused on shiny collecting. Compiled from markdown.
    * [`/pkmn/gs`](https://chisel.weirdgloop.org/gazproj/pkmn/gs) - a calculator for the ACE
  * [`/pkmn/plza`](https://chisel.weirdgloop.org/gazproj/pkmn/plza) - guide to shiny hunting in Hyperspace Lumiose in the DLC for Pokémon Legends: Z-A. Compiled from markdown.
  * [`/pkmn/[filename].png`](https://chisel.weirdgloop.org/gazproj/pkmn/plza_shinies_shalphas.png) - images for the Pokémon pages
* [`/test`](https://chisel.weirdgloop.org/gazproj/test) - Returns the contents of the environment passed to a route (headers & other info), plus a parsed quesy string and request body. Be careful about sharing contents/screenshots of this as it contains IPs and cookies etc.

# Running it yourself
Good luck.

You'll need:

* An ubuntu server. I couldn't tell you everything that's installed on here, its a lot. Chisel is a digitalocean droplet, current ubuntu version 24.04 LTS. It uses a decent amount of CPU when booting & RAM always, so you can't be too stingy.
* [UWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) with python3 support. I compiled this myself on chisel for python 3.9.7, though other versions are probably fine. This is installed an running as `uwsgi-py3`, as originally chisel also ran with a stock `uwsgi` which ran python2.7.
* UWSGI runs in emperor mode on chisel, pulling config from an ini file (not included in this repo). You don't necessarily need that, though, as you can run in single process mode with command line args if you prefer. An example ini is below; alter as needed.
* wsgirouter, which is installed on chisel (I don't remember how). The source code is provided in the repo as wsgirouter_example.py.
* [orjson](https://github.com/ijl/orjson) installed in a way that UWSGI can see. [Standard library json](https://docs.python.org/3/library/json.html) can also work, if you prefer.

Example ini
```ini
[uwsgi]
strict = true
wsgi-file = gazproj.py

chmod-socket = 666
socket = /tmp/gazproj.sock
vacuum = true
logger = file:.uwsgi-py3.log 
```