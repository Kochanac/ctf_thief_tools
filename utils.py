from termcolor import colored as clr

category_to_color = {
	'cry': 'green',
	'pwn': 'magenta',
	'rev': 'yellow',
	'for': 'cyan',
	'joy': 'red',
	'web': 'blue'
}

def red(text):
	return clr(text, "red")

def value_to_color(val):
	val = int(val)
	if val < 100:
		return "white"
	if val < 250:
		return "green"
	if val < 350:
		return "yellow"
	if val < 450:
		return "cyan"
	if val < 600:
		return "yellow"
	if val < 800:
		return "magenta"
	if val >= 800:
		return "red"

def process_value(val):
	if int(val) >= 1000:
		return clr(f' {val} ', value_to_color(val), 'on_white', attrs=['bold'])
	elif int(val) >= 400:
		return clr(val, value_to_color(val), attrs=['bold'])
	else:
		return clr(val, value_to_color(val))


# TODO: clean these things

def process_solved(data):
	if 'Solved' in data and data['Solved']:
		return clr('[ SOLVED ] '
		           , 'green'
		           , attrs = ['bold'])
	else:
		return ''

def process_category(data):
	if data["Category"][:3].lower() in category_to_color:
		return clr( data["Category"]
	           , category_to_color[data["Category"][:3].lower()])
	else:
		return data["Category"]

def process_title(data, ls=False):
	if ls:
		return data["Title"]
	else:
		return clr(data["Title"]
		           , value_to_color(data['Value'])
		           , attrs=['bold'])


def process_desc(text):
	return text

def parse_request(http):
	# Now we need to parse request
	txt = open('/tmp/request', 'r').readlines()

	# http = (True if 'HTTPS/' not in txt[0] else False)

	headers = dict()
	for i in txt[1::]:
		hdr = i.replace('\n', '').split(': ')
		if len(hdr) > 2:
			print(i, i.split(': '))
			raise TypeError('invalid request headers')

		headers[hdr[0]] = hdr[1]

	headers['Accept-Encoding'] = 'json'
	headers['If-Modified-Since'] = '0'
	url = ('https://' if not http else 'http://') + headers['Host'] + txt[0].split(' ')[1]

	return url, headers
