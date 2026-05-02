import markdown
from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension
import xml.etree.ElementTree as etree
from lxml.html import html5parser as lxmlhtml
import re
import json
import sys


# $img(pkmn/box9_1.png) => <div class="box9-img"><img src="/gazproj/pkmn/box9_1.png"></div>
# $img(pkmn/box9_1.png, hello) => <div class="box9-img"><img src="/gazproj/pkmn/box9_1.png"><div class="box9-img-caption">hello</div></div>
class GalleryProcessor(BlockProcessor):
	IMG_GAL = re.compile(r'^ *\$gallery *\r?\n')
	IMG_GAL_END = re.compile(r'\r?\n *\$endgallery\s*$')
	def test(self, parent, block):
		return self.IMG_GAL.search(block) is not None

	def run(self, parent, blocks):
		print('running $gallery parser')
		if self.IMG_GAL.search(blocks[0]):
			print('$gallery found')
			for block_num, block in enumerate(blocks):
				print(block_num, block)
				if self.IMG_GAL_END.search(block):
					print('$gallery-end found')
					blocks[0] = self.IMG_GAL.sub('', blocks[0]).strip()
					blocks[block_num] = self.IMG_GAL_END.sub('', blocks[block_num]).strip()
					print('\n'.join(blocks[0:block_num+1]))
					div = etree.SubElement(parent, 'div')
					div.set('class', 'md-gallery')
					div.text = '\n'.join(blocks[0:block_num+1])
					#self.parser.parseBlocks(div, blocks[0:block_num+1])
					print(etree.tostring(div))
					print(list(range(0,block_num+1)))
					print(type(blocks))
					blocks[0:block_num+1] = []
					#for i in range(0, block_num+1):
					#	print(f'removing {blocks.pop()}')
					return True
		return False

class ImageProcessor(BlockProcessor):
	IMG_RE = re.compile(r'^\$img\((.*)\)$')
	def test(self, parent, block):
		return self.IMG_RE.search(block) is not None

	def run(self, parent, blocks):
		print('running $img block parser')
		if self.IMG_RE.search(block):
			mtch = self.IMG_RE.search(blk)
			if mtch is not None and mtch.group(1) is not None:
				print(f'$img: found {mtch.group(1)}')
				grp = mtch.group(1).split(',', maxsplit=1)
				url = grp[0].strip()
				div = etree.SubElement(parent, 'div')
				div.set('class', 'md-img')
				img = etree.SubElement(div, 'img')
				img.set('loading', 'lazy')
				img.set('src', f'/gazproj/{url}')
				if len(grp) > 1:
					caption = grp[1].strip()
					if caption is not None and len(caption) > 0:
						div2 = etree.SubElement(div, 'div')
						div2.set('class', 'md-img-caption')
						div2.text = caption
				blocks.pop(0)
				return True
		return False

class InlineImageProcessor(InlineProcessor):
	IMG_RE = r'\$img\(([^\r\n]*)\)'
	def __init__(self, md=None):
		super().__init__(self.IMG_RE, md)

	def handleMatch(self, m, data):
		if m is not None and m.group(1) is not None:
			m_txt = m.group(0)
			gr = m.group(1).split(',', maxsplit=1)
			url = gr[0].strip()
			e = etree.Element('div')
			e.set('class', 'md-img')
			a = etree.SubElement(e, 'a')
			a.set('href', f'/gazproj/{url}')
			a.set('target', '_new')
			img = etree.SubElement(a, 'img')
			img.set('loading', 'lazy')
			img.set('src', f'/gazproj/{url}')
			if re.search(f'\\S *{m_txt} *', data) or re.search(f' *{m_txt} *\\S', data):
				e.set('class', 'md-img md-img-inline')
			else:
				if len(gr) > 1:
					caption = gr[1].strip()
					if caption is not None and len(caption)>0:
						div2 = etree.SubElement(e, 'div')
						div2.set('class', 'md-img-caption')
						div2.text = caption
			return (e, m.start(0), m.end(0))
		return (None,None,None)

class BRPreProcessor(Preprocessor):
	BR_RE = re.compile(r'<br */?>')
	def run(self, lines):
		newlines = []
		for line in lines:
			newlines.append(self.BR_RE.sub('¬', line))
		return newlines

class BRPostProcessor(Preprocessor):
	BR_RE = r'¬'
	def run(self, text):
		return text.replace(self.BR_RE, '<br>')


class TOCParser(Postprocessor):
	def run(self, text):
		with open('md_test.html', 'w', encoding='utf-8') as f:
			f.write(text)
		root = lxmlhtml.fromstring(f'<div class="wrapper"><div class="content">{text}</div></div>')
		toc = lxmlhtml.Element('div')
		root.getchildren()[0].addprevious(toc)
		toc_head = lxmlhtml.Element('div')
		toc.append(toc_head)
		toc_head.text = 'Table of Contents'
		toc.classes.add('toc')
		numbers = [0,0,0]
		for header in root.xpath('//h1 | //h2 | //h3'):
			level = int(header.tag[1]) - 1
			numbers[level] += 1
			for i in range(level+1, len(numbers)):
				numbers[i] = 0
			num_str = []
			layer = 0
			for i in range(len(numbers)):
				if numbers[i] > 0:
					num_str.append(str(numbers[i]))
					layer += 1
				else:
					break
			num_str = '.'.join(num_str)
			txt = header.text_content()
			anchor = txt.replace(' ', '_')
			header.set('id', anchor)
			toc_el = lxmlhtml.Element('a')
			toc.append(toc_el)
			toc_el.set('href', f'#{anchor}')
			toc_el.classes.add(f'toc-layer-{layer}')
			toc_el.text = f'{num_str} {txt}'
		
		#root.cssselect('div.box9-gallery > p').drop_tag()

		return lxmlhtml.tostring(root, encoding='unicode')

class SpoilerProcessor(InlineProcessor):
	IMG_RE = r'\|\|(.+?)\|\|'
	def __init__(self, md=None):
		super().__init__(self.IMG_RE, md)

	def handleMatch(self, m, data):
		if m is not None and m.group(1) is not None:
			m_txt = m.group(1)
			e = etree.Element('span')
			e.set('class', 'spoiler spoiler-hidden')
			e.text = m_txt
			return (e, m.start(0), m.end(0))
		return (None,None,None)


class GazExtension(Extension):
	def extendMarkdown(self, md):
		md.parser.blockprocessors.register(GalleryProcessor(md.parser), 'gaz-gallery', 175000)
		md.inlinePatterns.register(InlineImageProcessor(), 'gaz-img-inline', 175)
		md.inlinePatterns.register(SpoilerProcessor(), 'gaz-spoiler', 175)
		#md.preprocessors.register(BRPreProcessor(), 'gaz-br-pre', 10000)
		#md.postprocessors.register(BRPostProcessor(), 'gaz-br-post', 10000)
		#md.postprocessors.register(TOCParser(md), 'gaz-toc', 175)

def go():
	if len(sys.argv)>1:
		if sys.argv[1] == 'box9':
			with open('box9guide.md', 'r', encoding='utf-8') as f_in, open('../html/box9guide.html', 'w', encoding='utf-8') as f_out:
				f_out.write('<!DOCTYPE html><html><head><title>BOX 9 ACE guide</title><link rel="stylesheet" type="text/css" href="/gazproj/pkmn.css"></head><body class="box9guide">\n')
				f_out.write(markdown.markdown(f_in.read(), extensions=['tables', 'md_in_html', 'toc', 'smarty', GazExtension()]))
				f_out.write('\n</body></html>')
			return
		if sys.argv[1] == 'plza':
			with open('plzashiny.md', 'r', encoding='utf-8') as f_in, open('../html/plzashiny.html', 'w', encoding='utf-8') as f_out:
				f_out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>Shiny Hunting in Pokémon Legends: Z-A</title>
		<link rel="stylesheet" type="text/css" href="/gazproj/pkmn.css">
	</head>
	<body class="plzaguide">\n''')
				f_out.write(markdown.markdown(f_in.read(), extensions=['tables', 'md_in_html', 'toc', 'smarty', GazExtension()]))
				f_out.write('''
		<script>
		document.querySelectorAll('.spoiler.spoiler-hidden').forEach(e=>{
			e.addEventListener('click', ev=>{ev.target.classList.remove('spoiler-hidden')});
		});
		document.getElementById('unspoiler-all').addEventListener('click', ()=>{
			document.querySelectorAll('.spoiler.spoiler-hidden').forEach(e=>{
				e.className = '';
			});
			document.getElementById('unspoiler-all').textContent = 'unspoilered everything :)';
		});
		</script>
	</body>
</html>''')
			return
	print(f'python3 {sys.argv[0]} [box9|plza]')

if __name__ == '__main__':
	go()