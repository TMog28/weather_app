import os
import json
import requests
from datetime import date, datetime
from dotenv import load_dotenv
import time





load_dotenv()

api_key =os.getenv('OWM_KEY')

''' FUNCTION TO CALL API AND CALL OWM API '''
def geo_locator(user_city):
	api_call = f'http://api.openweathermap.org/geo/1.0/direct?q={user_city},&limit=1&appid={api_key}'
	api_response = requests.get(api_call)
	data_api = api_response.json()
	#print(data_api)
	geo_data = []
	results = {
		'timestamp':datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
		'data': {
			'city':data_api[0]['name'],
			'lat':data_api[0]['lat'],
			'lon':data_api[0]['lon'],
			'country': data_api[0]['country'], 
			'state': data_api[0]['state']
		}
	}

	geo_data.append(results)
	
	
	file_name =  str(results['data']['city'])+'-'+str(results['data']['lat'])+'-'+str(results['data']['lon'])
	
	f= open(file_name.replace(" ", "_").lower()+'.txt',"w")
	f.write(json.dumps(geo_data))
	f.close()

	return print(f" City: {results['data']['city']} \n Lat: {results['data']['lat']} \n Lon: {results['data']['lon']} \n State: {results['data']['state']} \n Country: {results['data']['country']}")



try:
	city_name = input('What is the name of your city? ')

	query_files = [filename for filename in os.listdir('.') if filename.startswith(city_name.replace(" ", "_").lower())]

	if query_files:
		#print('Exists')
		for i in query_files:
			with open(i,'r') as f:
				contents = json.load(f)

		#calculate the time 
		current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		t1 = datetime.strptime(current_time,'%Y-%m-%d %H:%M:%S')
		
		content_time = contents[0]['timestamp']
		t2 = datetime.strptime(content_time, '%Y-%m-%d %H:%M:%S')
		
		last_query = t1.hour - t2.hour
		# end time calculation 

		#if equal to or less then 3 hours read txt file
		if last_query <= 3:
			#print('Use existing')
			print(f" City: {contents[0]['data']['city']} \n Lat: {contents[0]['data']['lat']} \n Lon: {contents[0]['data']['lon']} \n State: {contents[0]['data']['state']} \n Country: {contents[0]['data']['country']}")
		#else query api for new data
		else:
			#print('New query')
			geo_locator(city_name)
	else:
		#print('Does not Exist ')
		geo_locator(city_name)
		
except Exception as e:
	print(e)
	print('Sorry could not complete your request. Please ensure city name is typed in correctly')