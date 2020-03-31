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

print("Total custom_collections: #{count}".format(count=count))

custom_collections = requests.get(url + 'custom_collections.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("collections_custom.csv", "w"))
f.writerow(["Handle", "Title", "Body (HTML)"])

while custom_collections:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = custom_collections.json()
		for item in x["custom_collections"]:
			print(item["title"])
			f.writerow([item["handle"],item["title"],item["body_html"]])

		custom_collections = custom_collections.links['next']['url']
		custom_collections = requests.get(custom_collections,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		custom_collections = ""

	page_number += 1