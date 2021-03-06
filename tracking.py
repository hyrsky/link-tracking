#!/usr/bin/env python

import os
import logging
import hug
import falcon

from zappa.async import task
from datetime import datetime
from marshmallow import fields

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('tracking')

# Get sheets id from environment variables
GOOGLE_SHEETS_ID = os.environ.get('GOOGLE_SHEETS_ID')

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by key and open the first sheet
sheet = client.open_by_key(GOOGLE_SHEETS_ID).sheet1

@hug.get('/')
def track(id: fields.Integer(required=True), 
				 	val: fields.Integer(required=True), 
				 	url: fields.Url(required=True)):
	"""
	Save request parameters and redirect to url
	"""
	logger.info(f'{id}: value: {val} -> {url}')

	# Save results is processed asynchronously
	save_results(id, val)

	raise falcon.HTTPFound(url)

@task
def save_results(id, value):
	try:
		created = datetime.utcnow()
		sheet.append_row([created.isoformat(), id, value])
	except Exception:
		logger.exception('Saving results failed')
		logger.error(f'{id}: value: {value} -> {url}')
