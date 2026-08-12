
import urllib.request
import json, sys, random

oeis_data = {}
json_filename = 'oeis_data.json'


def load_data():
	global oeis_data
	with open(json_filename, 'r') as f:
		oeis_data=json.load(f)
	for num in list(oeis_data.keys()):
		if type(num) is str:
			oeis_data[int(num)] = oeis_data[num]
			del oeis_data[num]



def save_data():
	with open(json_filename, 'w') as f:
		json.dump(oeis_data, f)


def existing_entry_numbers():
	for num in oeis_data:
		yield num

def is_existing_entry_number(num):
	return num in oeis_data

def num_available_sequences():
	return len(oeis_data)

def random_available_sequence():
	index = random.randrange(0, num_available_sequences()-1)
	for i,n in enumerate(existing_entry_numbers()):
		if i==index:
			return OEISSequence(n)


def fetch_json_data(number):
	entry = f'A{number:06}'
	url = f'https://oeis.org/search?q=id:{entry}&fmt=json'
	req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "})
	try:
		resp = urllib.request.urlopen(req)

		html = resp.read().decode('utf-8')

		[data] = json.loads(html)
		return data
	except:
		return {}


_OEISSequence_instances = {}

class OEISSequence(object):

	def __new__(cls, number):
		if number in _OEISSequence_instances:
			return _OEISSequence_instances[number]
		if number not in oeis_data:
			raise ValueError('that entry is not found, please parse it.')
		instance = super().__new__(cls)
		self = instance
		entry = oeis_data[number]
		self._number = number
		self._entry_label = entry['entry']
		self._sequence = entry['sequence']
		self._url = entry['link']
		self._description = entry.get('description', None)
		self._json_data = None
		_OEISSequence_instances[number] = instance
		return instance


	@property
	def number(self):
		return self._number

	def __iter__(self):
		for a in self._sequence:
			yield a

	@property
	def url(self):
		return self._url

	@property
	def entry_label(self):
		return self._entry_label


	def _get_json_data(self):
		if self._json_data is None:
			self._json_data = fetch_json_data(self.number)
		return self._json_data

	@property
	def description(self):
		if self._description is None:
			self._description = self._get_json_data().get('name', None)
		return self._description


	def reload_sequence(self):
		self._sequence = list(map(int,self._get_json_data()['data'].split(',')))
	

	@description.setter
	def description(self, text:str):
		self._description = text

	def remove_description(self):
		self._description = None


	def commit_data(self):
		entry = oeis_data[self.number]
		entry['sequence'] = self._sequence
		if self._description is not None:
			entry['description'] = self._description

	def __len__(self):
		return len(self._sequence)

	def __str__(self):
		NL = '\n'
		return f'''
OEIS entry #{self.number}:
First {len(self)} terms: {self._sequence} { f'{NL}{self._description}' if self._description else ''}
		'''

	def __repr__(self):
		return f'{type(self).__name__}({self.number})'


	def __call__(self, n:int):
		if n<0 or n>=len(self):
			raise ValueError(f'argument must be in the range [{0},{len(self)}).')
		return self._sequence[n]



	
		



