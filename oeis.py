
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


