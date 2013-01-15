import html5lib
import urllib2
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from BeautifulSoup import BeautifulSoup
import re

def memoize(f):
    cache= {}
    def memf(*x):
        if x not in cache:
            cache[x] = f(*x)
        return cache[x]
    return memf

@memoize
def prev_and_next_ep(url, str_or_lst):
	"""Next episode, followed by previous episode, returned in the form of a list."""
	parser = html5lib.HTMLParser()
	tag_soup = urllib2.urlopen(url).read()
	root = fromstring(tag_soup)
	string = tostring(root, pretty_print=True)
	soup = BeautifulSoup(string)
	div = soup.findAll("div", "grid_7_5 box margin_top_bottom")
	lst = []
	prev_and_next = []
	next = ''
	prev = ''
	for item in div:
		x = item.find("span", "content_title")
		if x:
			if x.find(text=True) == 'Episode Info':
				lst.append(item)
	y = lst[0].findAll("h2")
	for item in y:
		prev_and_next.append((item.findAll(text=True)))	
	if str_or_lst == 'lst':
		return prev_and_next
	elif str_or_lst == 'str':
		for item in prev_and_next[0][1:]:
			next += str(item)
		for item in prev_and_next[1][1:]:
			prev += str(item)
		return (next, prev)
	

	"""	prev_and_next = []
	for item in div:
		x = item.find("span", "content_title")
		if x:
			if x.find(text=True) == 'Episode Info':
				lst.append(item)
	y = lst[0].findAll("h2")
	for item in y:
		prev_and_next.append((item.findAll(text=True)))
	return prev_and_next
	"""
@memoize
def picture(url):
	parser = html5lib.HTMLParser()
	tag_soup = urllib2.urlopen(url).read()
	root = fromstring(tag_soup)
	string = tostring(root, pretty_print=True)
	soup = BeautifulSoup(string)
	x = soup.find("div", "image_box")
	y = x.find("img")
	return str(y["src"])
	
@memoize
def synopsis(url='http://www.tvrage.com/The_Office'):
	"""Returns the synopsis."""
	parser = html5lib.HTMLParser()
	tag_soup = urllib2.urlopen(url).read()
	root = fromstring(tag_soup)
	string = tostring(root, pretty_print=True)
	soup = BeautifulSoup(string)
	div = soup.find("div", "show_synopsis")
	return div.findAll(text=True)
	