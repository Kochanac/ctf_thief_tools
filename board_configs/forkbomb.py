import json

def getInfo():
	return {
		"task_id_in_url": -1,
		"url_to_files": "",
		"http?": False,
		"custom_ids": True
	}

def get_ids(url):
	import requests as req
	from lxml import etree

	url = '/'.join(url.split('/')[:-1])
	
	urls = etree.HTML(req.get(url).text).xpath('//a[@class="tile"]/@href')
	
	return map(lambda x: x.split('/')[-1], urls)



def parse_task(data, **kwargs):
	from lxml import etree
	
	tasktag = etree.HTML(data).xpath('//table[@id="flagtable"]')[0]

	author = tasktag.xpath('.//span[@class="author"]/text()')[0]
	
	task = {
		"Title": tasktag.xpath('.//span[@class="desc"]/text()')[0],
		"Category": tasktag.xpath('.//span[@class="cat"]/text()')[0],
		"Description": etree.tostring(tasktag.xpath('.//div[@class="fullDesc"]')[0]).decode() + f"\n\n(from forkbomb, { author })",
		"Files": list(),
		"Color": tasktag.xpath('//div[contains(@class,"fullTile")]/@style')[0].split(" ")[-1],
		"Solved": len(tasktag.xpath('//div[@class="fullTile solved"]')) == 1,
		"Value": int(tasktag.xpath('.//span[@class="cost"]/text()')[0])
	}

	return task

def get_meta(base, HEADERS):
	return {}