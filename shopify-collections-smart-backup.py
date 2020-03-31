#! /usr/bin/env python3

import csv
import json
import requests
import os

# Environment variables
if os.path.exists('config.env'):
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")

url = 'https://' + os.getenv('SHOPIFY_URL') + '.myshopify.com/admin/api/2020-01/'

params = {'limit': 250}
page_number = 1
count = requests.get(url + 'smart_collections/count.json',auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD'))).json().get('count')

print("Total smart_collections: #{count}".format(count=count))

smart_collections = requests.get(url + 'smart_collections.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("collections_smart.csv", "w"))
f.writerow(["Handle", "Title", "Body (HTML)", "Rules"])

while smart_collections:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = smart_collections.json()
		for item in x["smart_collections"]:
			print(item["title"])
			f.writerow([item["handle"],item["title"],item["body_html"],item["rules"]])

		smart_collections = smart_collections.links['next']['url']
		smart_collections = requests.get(smart_collections,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		smart_collections = ""

	page_number += 1