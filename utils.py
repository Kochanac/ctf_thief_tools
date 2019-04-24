from termcolor import colored as clr

category_to_color = {
	'cry': 'green',
	'pwn': 'magenta',
	'rev': 'yellow',
	'for': 'cyan',
	'joy': 'red',
	'web': 'grey'
}

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
		return clr('[ SOLVED ]'
		           , 'green'
		           , attrs = ['bold'])
	else:
		return ''

def process_category(data):
	return clr( data["Category"]
	           , category_to_color.get(data["Category"][:3], 'white') )

def process_title(data, ls=False):
	if ls:
		return data["Title"]
	else:
		return clr(data["Title"]
		           , value_to_color(data['Value'])
		           , attrs=['bold'])

def process_desc(text):
	return text
