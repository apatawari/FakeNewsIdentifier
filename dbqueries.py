import mysql.connector as con
import configparser as cp
import logwriter as lw
import configreader as reader
import datetime
import numpy as np

logger = lw.log_writer()
mconfig = reader.config_reader('message.properties')
today  = datetime.datetime.now()
#TODO add method comments
#TODO read the error messages from properties file


def connection():
	try:
		config = cp.RawConfigParser()
		config.read('config.properties')
		dbname = config.get('DatabaseSection', 'database.dbname');
		dbuser = config.get('DatabaseSection', 'database.user');
		dbpass = config.get('DatabaseSection', 'database.password');
		host   = config.get('DatabaseSection', 'database.host'); 
		auth_plugin = config.get('DatabaseSection','database.auth_plugin');
		conn = con.connect(user = dbuser,password = dbpass,host = host,database = dbname,auth_plugin=auth_plugin)
        
	except Exception as error:
		raise Exception("Error configuring the database {}" .format(error))
		logger.error('Error configuring the database ', error)

	return conn
	
def save_uzhavan_request_for_pest(ai_response, request_json):

	try:
		conn = connection()
		cursor = conn.cursor()
		query = "INSERT INTO tbl_request (uzhavan_request_id, image_id, district_id, block_id, crop_id, remarks, predicted_issue_id_pest, predicted_crop_id, crop_detection_model, pd_detection_model, response_time, contact_number, request_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(query, (request_json['uzhavan_request_id'], request_json['image_id'], request_json['district_id'], request_json['block_id'], request_json['crop_id'], request_json['remarks'], ai_response['response']['crop']['pd']['id'], ai_response['response']['crop']['id'], ai_response['response']['crop']['classification_model'], ai_response['response']['crop']['pd']['classification_model'], ai_response['response']['response_time'], request_json['contact_number'], today))
		conn.commit()
		logger.info("Uzhavan request record added successfully")
	except Exception as error:
		raise Exception("Failed to insert request data from Uzhavan " .format(error))
		logger.error('Failed to insert request from Uzhavan',error)
		conn.rollback()
	finally:
		if (conn.is_connected()):
			cursor.close()
			conn.close()
			logger.info("Database connection is closed")
]