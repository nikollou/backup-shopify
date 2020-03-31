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
count = requests.get(url + 'custom_collections/count.json',auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD'))).json().get('count')

print("Total Products: #{count}".format(count=count))

collects = requests.get(url + 'custom_collections.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("collections.csv", "w"))
f.writerow(["Handle", "Title", "Body (HTML)"])


z = collects.json()
print(z)


while collects:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = collects.json()
		for item in x["collects"]:
			asset_id = item["id"]
			y = requests.get(url + 'collections/' + str(asset_id) + '.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
			y = y.json()

			f.writerow([y["collection"]["handle"],y["collection"]["title"],y["collection"]["body_html"]])

		collects = custom_collections.links['next']['url']
		collects = requests.get(custom_collections,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		collects = ""

	page_number += 1