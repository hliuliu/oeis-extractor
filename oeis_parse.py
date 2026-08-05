
import urllib.request
import json, sys, random

from html.parser import HTMLParser


oeis_data = {}


def new_random_number():
	num = random.randrange(1, 400000-1)
	while num in oeis_data:
		num = random.randrange(1, 400000-1)
	return num


def get_oeis_info(number):
	entry = f'A{number:06}'
	url = f'https://oeis.org/{entry}'
	listurl = f'{url}/list'

	req = urllib.request.Request(listurl, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "})
	resp = urllib.request.urlopen(req)

	html = resp.read().decode('utf-8')

	parser = OEISParser()

	parser.feed(html)

	if not parser.seqdata_tag_found or not parser.seqdata:
		return {}

	return dict(
		entry=entry,
		link=url,
		sequence = parser.seqdata
	)

# print(html)


def toint(s):
	s = ''.join((c for c in s if '0'<=c<='9'))
	return int(s)


class OEISParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.seqdata = []
		self.seqdata_tag_found = False

	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)
		if self.seqdata_tag_found:
			return
		if attrs.get('class', None)=='seqdata':
			self.seqdata_tag_found = True

	def handle_data(self, data):
		if self.seqdata_tag_found:
			if self.seqdata:
				return
			data = data.strip()
			if not data:
				return
			assert(data[0]=='[' and data[-1]==']')
			try:
				data = list(map(toint, data[1:-1].split(',')))
			except:
				data = []
			self.seqdata = data


	

def main():
	global oeis_data
	json_filename = 'oeis_data.json'
	with open(json_filename, 'r') as f:
		oeis_data=json.load(f)
	for num in list(oeis_data.keys()):
		if type(num) is str:
			oeis_data[int(num)] = oeis_data[num]
			del oeis_data[num]
	nums = map(int, sys.argv[1:])
	if len(sys.argv)<2:
		L = random.randrange(100, 1000)
		nums = (new_random_number() for _ in range(L))
	for num in nums:
		if num not in oeis_data:
			try:
				info = get_oeis_info(num)
			except Exception as e:
				print(num,e)
				continue
			if not info:
				continue
			oeis_data[num] = info
	with open(json_filename, 'w') as f:
		json.dump(oeis_data, f)
	




if __name__=='__main__':
	main()
	# print(oeis_data)
	print(list(oeis_data.keys())[-10:])
	print(f'{len(oeis_data)} entries saved.')
