# -*- coding: utf-8 -*-
import random, re, string
import dateutil.tz, dateutil.relativedelta, dateutil.parser
import datetime

dateutilparser = dateutil.parser() #Because i have no idea why i can't call dateutil.parser.parse() directly... 

TITLE = 'Crunchyroll'
ART = 'art-default.png'
ICON = 'icon-default.png'
ICON_QUEUE = 'icon-queue.png'
ICON_LIST = 'icon-list.png'
ICON_PREFS = 'icon-prefs.png'
ICON_SEARCH = 'icon-search.png'
ICON_NEXT = 'icon_next.png'

API_URL = "https://api.crunchyroll.com"
API_HEADERS = {'User-Agent':"Mozilla/5.0 (PLAYSTATION 3; 4.31)", 'Host':"api.crunchyroll.com", 'Accept-Encoding':"gzip, deflate", 'Accept':"*/*", 'Content-Type':"application/x-www-form-urlencoded"}
API_VERSION = "1.0.1"
API_LOCALE = "enUS" 
API_ACCESS_TOKEN = "S7zg3vKx6tRZ0Sf"
API_DEVICE_TYPE = "com.crunchyroll.ps3"

####################################################################################################
def Start():

	Plugin.AddViewGroup('InfoList', viewMode = 'InfoList', mediaType = 'items')
	Plugin.AddViewGroup('List', viewMode = 'List', mediaType = 'items')

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	ObjectContainer.view_group = 'List'

	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)

	VideoClipObject.thumb = R(ICON)
	VideoClipObject.art = R(ART)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0'
	
####################################################################################################
def login():

	current_datetime = datetime.datetime.now(dateutil.tz.tzutc())
	username = Prefs['username']
	password = Prefs['password']
	
	#Create unique device_id or retreive the existing device_id
	if not Data.Exists("device_id"):
		char_set = string.ascii_letters + string.digits
		device_id = ''.join(random.sample(char_set,32))
		Data.SaveObject("device_id", device_id)
		Log("Crunchyroll.bundle ----> New device_id created. New device_id is: "+ str(device_id))
	else:
		device_id = Data.LoadObject("device_id")
	
	#Check to see if a session_id doesn't exist or if the current auth token is invalid and if so start a new session and log it in. 	
	if ('session_id' not in Dict or 'auth_expires' not in Dict or current_datetime > Dict['auth_expires']): 
		
		#Start new session
		Log("Crunchyroll.bundle ----> Starting new session.")
		options = {'device_id':device_id, 'device_type':API_DEVICE_TYPE, 'access_token':API_ACCESS_TOKEN, 'version':API_VERSION, 'locale': API_LOCALE}
		request = JSON.ObjectFromURL(API_URL+"/start_session.0.json", values=options, cacheTime=0, headers=API_HEADERS)
		if request['error'] is False:
			Dict['session_id'] = request['data']['session_id'] 
			Dict['session_expires'] = (current_datetime + dateutil.relativedelta.relativedelta( hours = +4 ))
			Log("Crunchyroll.bundle ----> New session created! Session ID is: "+ str(Dict['session_id']))
		elif request['error'] is True:
			Log("Crunchyroll.bundle ----> Error starting new session. Error message is: "+ str(request['message']))
			return False
			
		#Login the session we just started.
		if not username or not password:
			Log("Crunchyroll.bundle ----> No Username or Password set")
			return False
		else: 
			Log("Crunchyroll.bundle ----> Logging in the new session we just created.")
			options = {'session_id':Dict['session_id'], 'password':password, 'account':username, 'version':API_VERSION, 'locale': API_LOCALE}
			request = JSON.ObjectFromURL(API_URL+"/login.0.json", values=options, cacheTime=0, headers=API_HEADERS)
			if request['error'] is False:
				Dict['auth_token'] = request['data']['auth'] 
				Dict['auth_expires'] = dateutilparser.parse(request['data']['expires'])
				Dict['premium_type'] = request['data']['user']['premium']
				Log("Crunchyroll.bundle ----> Login successful.")
			elif request['error'] is True:
				Log("Crunchyroll.bundle ----> Error logging in new session. Error message was: "+ str(request['message']))
				return False				
		
		Dict.Save()
		return True
		
	#Check to see if a valid session and auth token exist and if so reinitialize a new session using the auth token. 	
	elif ('session_id' in Dict and 'auth_token' in Dict and current_datetime < Dict['auth_expires'] and current_datetime > Dict['session_expires']):
		
		#Re-start new session
		Log("Crunchyroll.bundle ----> Valid auth token was detected. Restarting session.")
		options = {'device_id':device_id, 'device_type':API_DEVICE_TYPE, 'access_token':API_ACCESS_TOKEN, 'version':API_VERSION, 'locale': API_LOCALE, 'auth':Dict['auth_token']}
		request = JSON.ObjectFromURL(API_URL+"/start_session.0.json", values=options, cacheTime=0, headers=API_HEADERS)
		if request['error'] is False:
			Dict['session_id'] = request['data']['session_id'] 
			Dict['auth_expires'] = dateutilparser.parse(request['data']['expires']) 
			Dict['premium_type'] = request['data']['user']['premium'] 
			Dict['auth_token'] = request['data']['auth'] 
			Dict['session_expires'] = (current_datetime + dateutil.relativedelta.relativedelta( hours = +4 )) #4 hours is a guess. Might be +/- 4. 
			Log("Crunchyroll.bundle ----> Session restart successful. New session_id is: "+ str(Dict['session_id']))
					
			Dict.Save()	
			return True
		elif request['error'] is True:
			#Remove Dict variables so we start a new session next time around. 
			del Dict['session_id']
			del Dict['auth_expires']
			del Dict['premium_type']
			del Dict['auth_token']
			del Dict['session_expires']
			Log("Crunchyroll.bundle ----> Error restarting session. Error message was: "+ str(request['message']))
			
			Dict.Save()
			return False

	#If we got to this point that means a session exists and it's still valid, we don't need to do anything. 
	elif ('session_id' in Dict and current_datetime < Dict['session_expires']):
		Log("Crunchyroll.bundle ----> A valid session was detected. Using existing session_id of: "+ str(Dict['session_id']))
		return True
	
	#This is here as a catch all in case something gets messed up along the way. Remove Dict variables so we start a new session next time around. 
	else:
		del Dict['session_id']
		del Dict['auth_expires']
		del Dict['premium_type']
		del Dict['auth_token']
		del Dict['session_expires']
		Log("Crunchyroll.bundle ----> Something in the login process went wrong.")
		
		Dict.Save()	
		return False 
		

####################################################################################################
def ValidatePrefs():
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))

####################################################################################################
@handler('/video/crunchyroll', TITLE, thumb=ICON, art=ART)
def MainMenu():
	loginResult = login()
	Log("Crunchyroll.bundle ----> Login result: " + str(loginResult))
	
	oc = ObjectContainer(no_cache = True)
	
	if loginResult is True:
		oc.add(DirectoryObject(key=Callback(Queue, title = "My Queue"), title = "My Queue", thumb = R(ICON_QUEUE)))
		oc.add(DirectoryObject(key=Callback(History, title = "History", offset = 0), title = "History", thumb = R(ICON_QUEUE)))
		oc.add(DirectoryObject(key=Callback(Channels, title = "Anime", type = "anime"), title = "Anime", thumb = R(ICON_LIST)))	
		oc.add(DirectoryObject(key=Callback(Channels, title = "Drama", type = "drama"), title = "Drama", thumb = R(ICON_LIST)))	
		oc.add(DirectoryObject(key=Callback(Channels, title = "Pop", type = "pop"), title = "Pop", thumb = R(ICON_LIST)))	
		oc.add(InputDirectoryObject(key=Callback(Search), title = "Search", prompt = "Anime series, drama, etc", thumb = R(ICON_SEARCH)))	

	oc.add(PrefsObject(title = 'Preferences', thumb = R(ICON_PREFS)))
	return oc

####################################################################################################	
@route('/video/crunchyroll/queue')
def Queue(title):
	oc = ObjectContainer(title2 = title)
	if Prefs['queue_type'] == 'Episodes':
		fields = "media.episode_number,media.name,media.description,media.media_type,media.series_name,media.available,media.available_time,media.free_available,media.free_available_time,media.duration,media.url,media.screenshot_image,image.fwide_url,image.fwidestar_url"
		options = {'media_types':"anime|drama", 'fields':fields}
		request = makeAPIRequest('queue', options)
		if request['error'] is False:	
			return list_media_items(request['data'], 'Queue', '1', 'queue')				
		elif request['error'] is True:
			return ObjectContainer(header = 'Error', message = request['message'])

	elif Prefs['queue_type'] == 'Series':
		fields = "series.name,series.description,series.series_id,series.rating,series.media_count,series.url,series.publisher_name,series.year,series.portrait_image,image.large_url"
		options = {'media_types':"anime|drama", 'fields':fields}
		request = makeAPIRequest('queue', options)
		if request['error'] is False:
			for series in request['data']:
				series = series['series']
				thumb = '' if (series['portrait_image'] is None or series['portrait_image']['large_url'] is None or 'portrait_image' not in series or 'large_url' not in series['portrait_image']) else series['portrait_image']['large_url'] #Becuase not all series have a thumbnail. 
				rating = '0' if (series['rating'] == '' or 'rating' not in series) else series['rating'] #Because Crunchyroll seems to like passing series without ratings
				if ('media_count' in series and 'series_id' in series and 'name' in series and series['media_count'] > 0): #Because Crunchyroll seems to like passing series without these things
					oc.add(TVShowObject(
						key = Callback(list_collections, series_id = series['series_id'], series_name = series['name'], thumb = thumb, count = series['media_count']), 
						rating_key = series['url'],
						title = series['name'],
						summary = series['description'],
						studio = series['publisher_name'],
						thumb = thumb,
						episode_count = int(series['media_count']), 
						viewed_episode_count = 0,
						rating = (float(rating) / 10)))
			
			#Check to see if anything was returned
			if len(oc) == 0:
				return ObjectContainer(header='No Results', message='No results were found')
			
		elif request['error'] is True:
			return ObjectContainer(header = 'Error', message = request['message'])

	return oc

####################################################################################################	
@route('/video/crunchyroll/history')
def History(title, offset):
	oc = ObjectContainer(title2 = title)
	fields = "media.episode_number,media.name,media.description,media.media_type,media.series_name,media.available,media.available_time,media.free_available,media.free_available_time,media.duration,media.url,media.screenshot_image,image.fwide_url,image.fwidestar_url"
	options = {'media_types':"anime|drama", 'fields':fields, 'limit':'64'}
	request = makeAPIRequest('recently_watched', options)
	if request['error'] is False:	
		return list_media_items(request['data'], 'Recently Watched', '1', 'history')	
	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

	return oc
	
####################################################################################################
@route('/video/crunchyroll/channels')
def Channels(title, type):
	oc = ObjectContainer(title2 = title)
	oc.add(DirectoryObject(key=Callback(list_series, title = "Popular", media_type = type, filter = "popular", offset = 0), title = "Popular", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key=Callback(list_series, title = "Simulcasts", media_type = type, filter = "simulcast", offset = 0), title = "Simulcasts", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key=Callback(list_series, title = "Updated", media_type = type, filter = "updated", offset = 0), title = "Updated", thumb = R(ICON_LIST)))	
	oc.add(DirectoryObject(key=Callback(list_series, title = "Alphabetical", media_type = type, filter = "alpha", offset = 0), title = "Alphabetical", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key=Callback(list_categories, title = "Genres", media_type = type, filter = "genre"), title = "Genres", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key=Callback(list_categories, title = "Seasons", media_type = type, filter = "season"), title = "Seasons", thumb = R(ICON_LIST)))
	return oc

####################################################################################################	
@route('/video/crunchyroll/search')
def Search(query): 
	oc = ObjectContainer(title2 = 'Search')
	fields = "series.name,series.description,series.series_id,series.rating,series.media_count,series.url,series.publisher_name,series.year,series.portrait_image,image.large_url"
	options = {'media_types':'anime|drama|pop', 'classes':'series', 'fields':fields, 'limit':'64', 'q':query}
	request = makeAPIRequest('search', options)
	if request['error'] is False:
		for series in request['data']:
			thumb = '' if (series['portrait_image'] is None or series['portrait_image']['large_url'] is None or 'portrait_image' not in series or 'large_url' not in series['portrait_image']) else series['portrait_image']['large_url'] #Becuase not all series have a thumbnail. 
			rating = '0' if (series['rating'] == '' or 'rating' not in series) else series['rating'] #Because Crunchyroll seems to like passing series without ratings
			if ('media_count' in series and 'series_id' in series and 'name' in series and series['media_count'] > 0): #Because Crunchyroll seems to like passing series without these things
				oc.add(TVShowObject(
					key = Callback(list_collections, series_id = series['series_id'], series_name = series['name'], thumb = thumb, count = series['media_count']), 
					rating_key = series['url'],
					title = series['name'],
					summary = series['description'],
					studio = series['publisher_name'],
					thumb = thumb,
					episode_count = int(series['media_count']), 
					viewed_episode_count = 0,
					rating = (float(rating) / 10)))
		
	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])
	
	#Check to see if anything was returned
	if len(oc) == 0:
		return ObjectContainer(header='No Results', message='No results were found')
	
	return oc
	
####################################################################################################	
@route('/video/crunchyroll/series')
def list_series(title, media_type, filter, offset): 
	oc = ObjectContainer(title2 = title)
	fields = "series.name,series.description,series.series_id,series.rating,series.media_count,series.url,series.publisher_name,series.year,series.portrait_image,image.large_url"
	options = {'media_type':media_type, 'filter':filter, 'fields':fields, 'limit':'64', 'offset':offset}
	request = makeAPIRequest('list_series', options)
	if request['error'] is False:
		counter = 0
		for series in request['data']:
			thumb = '' if (series['portrait_image'] is None or series['portrait_image']['large_url'] is None or 'portrait_image' not in series or 'large_url' not in series['portrait_image']) else series['portrait_image']['large_url'] #Becuase not all series have a thumbnail. 
			rating = '0' if (series['rating'] == '' or 'rating' not in series) else series['rating'] #Because Crunchyroll seems to like passing series without ratings
			if ('media_count' in series and 'series_id' in series and 'name' in series and series['media_count'] > 0): #Because Crunchyroll seems to like passing series without these things
				oc.add(TVShowObject(
					key = Callback(list_collections, series_id = series['series_id'], series_name = series['name'], thumb = thumb, count = series['media_count']), 
					rating_key = series['url'],
					title = series['name'],
					summary = series['description'],
					studio = series['publisher_name'],
					thumb = thumb,
					episode_count = int(series['media_count']), 
					viewed_episode_count = 0,
					rating = (float(rating) / 10)))
			counter = counter + 1
		if counter >= 64:
			offset = (int(offset) + counter)
			oc.add(DirectoryObject(key = Callback(list_series, title = title, media_type = media_type, filter = filter, offset = offset), title = "Next...", thumb = R(ICON_NEXT)))
		
		#Check to see if anything was returned
		if len(oc) == 0:
			return ObjectContainer(header='No Results', message='No results were found')
		
	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

	return oc

####################################################################################################	
@route('/video/crunchyroll/categories')
def list_categories(title, media_type, filter): 
	oc = ObjectContainer(title2 = title)
	options = {'media_type':media_type}
	request = makeAPIRequest('categories', options)
	if request['error'] is False:
		if filter == 'genre':
			if 'genre' in request['data']:
				for genre in request['data']['genre']:
					oc.add(DirectoryObject(key=Callback(list_series, title = genre['label'], media_type = media_type, filter = 'tag:'+genre['tag'], offset = 0), title = genre['label'], thumb = R(ICON_LIST)))

		if filter == 'season':
			if 'season' in request['data']:
				for season in request['data']['season']:
					oc.add(DirectoryObject(key=Callback(list_series, title = season['label'], media_type = media_type, filter = 'tag:'+season['tag'], offset = 0), title = season['label'], thumb = R(ICON_LIST)))
				
		#Check to see if anything was returned
		if len(oc) == 0:
			return ObjectContainer(header='No Results', message='No results were found')
	
	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

	return oc

####################################################################################################	
@route('/video/crunchyroll/collections')
def list_collections(series_id, series_name, thumb, count):
	oc = ObjectContainer(title2 = series_name)
	fields = "collections.collections_id,collections.season,collections.name,collections.portrait_image,collections.large_url"
	options = {'series_id':series_id, 'fields':fields, 'sort':'desc', 'limit':count}
	request = makeAPIRequest('list_collections', options)
	if request['error'] is False:		
		for collection in request['data']:
			if collection['season'] == "0":
				return list_media(collection['collection_id'], series_name, count, collection['complete'], '1')
			else:
				oc.add(SeasonObject(
					key = Callback(list_media, collection_id = collection['collection_id'], series_name = series_name, count = count, complete = collection['complete'], season = collection['season']), 
					rating_key = collection['collection_id'],
					index = int(collection['season']), 
					title = collection['name'],
					summary = collection['description'],
					show = str(series_name),
					thumb = thumb))
				
				#Check to see if anything was returned
				if len(oc) == 0:
					return ObjectContainer(header='No Results', message='No results were found')
			
	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])

	return oc
####################################################################################################
@route('/video/crunchyroll/media')
def list_media(collection_id, series_name, count, complete, season):
	oc = ObjectContainer(title2 = series_name)
	sort = 'asc' if complete is True else 'desc'	
	fields = "media.episode_number,media.name,media.description,media.media_type,media.series_name,media.available,media.available_time,media.free_available,media.free_available_time,media.duration,media.url,media.screenshot_image,image.fwide_url,image.fwidestar_url"
	options = {'collection_id':collection_id, 'fields':fields, 'sort':sort, 'limit':count}
	request = makeAPIRequest('list_media', options)
	if request['error'] is False:	
		return list_media_items(request['data'], series_name, season, 'normal')
	elif request['error'] is True:
		return ObjectContainer(header = 'Error', message = request['message'])
	return oc

####################################################################################################
def list_media_items(request, series_name, season, mode):
	oc = ObjectContainer(title2 = series_name)
	for media in request:
		
		#The following are items to help display Recently Watched and Queue items correctly
		season = media['collection']['season'] if mode == "history" else season 
		series_name = media['series']['name'] if (mode == "history" or mode == "queue") else series_name
		media = media['media'] if mode == "history" else media  #History media is one level deeper in the json string than normal media items. 
		if mode == "queue" and 'most_likely_media' not in media: #Some queue items don't have most_likely_media so we have to skip them.
			continue 
		media = media['most_likely_media'] if mode == "queue" else media  #Queue media is one level deeper in the json string than normal media items.
		
		#Dates, times, and such
		current_datetime = datetime.datetime.now(dateutil.tz.tzutc()) 
		available_datetime = dateutilparser.parse(media['available_time']).astimezone(dateutil.tz.tzlocal()) 
		available_date = available_datetime.date() 
		available_at = available_datetime.strftime('%A, %Y-%m-%d at %I:%M %p') 		
		free_available_datetime = dateutilparser.parse(media['free_available_time']).astimezone(dateutil.tz.tzlocal()) if media['free_available_time'].startswith('2') else dateutilparser.parse(media['free_available_time']) #Becuase dateutil doesn't like some of the dates that CR uses for shows that are never available to free users. 
		free_available_at = free_available_datetime.strftime('%A, %Y-%m-%d at %I:%M %p')
		
		#Fix Crunchyroll inconsistencies
		media['episode_number'] = '0' if media['episode_number'] == '' else media['episode_number'] #PV episodes have no episode number so we set it to 0. 
		media['episode_number'] = re.sub('\D', '', media['episode_number'])	#Because CR puts letters into some rare episode numbers.
		name = "Episode "+str(media['episode_number']) if media['name'] == '' else media['name'] #CR doesn't seem to include episode names for all media so we have to make one up. 	
		season = '1' if season == '0' else season #There is a bug which prevents Season 0 from displaying correctly in PMC. This is to help fix that. Will break if a series has both season 0 and 1. 
		thumb = "http://static.ak.crunchyroll.com/i/no_image_beta_full.jpg" if media['screenshot_image'] is None else media['screenshot_image']['fwide_url'] #because not all shows have thumbnails.
		
		if media['available'] is False:
			description = "This episode will be available on "+str(available_at)
			
			oc.add(DirectoryObject(
				key = Callback(media_unavailable, reason=description),
				title = str(media['episode_number'])+". "+"Coming Soon",
				summary = description,
				thumb = "http://static.ak.crunchyroll.com/i/coming_soon_beta_fwide.jpg"))
			
		elif media['available'] is True:
			if (media['free_available'] is False and media['media_type'] in Dict['premium_type']) or (media['free_available'] is False and media['media_type'] == 'pop' and Dict['premium_type'] in 'anime|drama') or media['free_available'] is True:					

				oc.add(EpisodeObject(
					url = media['url'],
					title = name,
					summary = media['description'],
					originally_available_at = available_date,
					index = int(media['episode_number']),
					show = media['series_name'],
					season = int(season),
					thumb = thumb,
					duration = int((float(media['duration']) * 1000))))
					
			else:
				if (current_datetime < free_available_datetime and free_available_datetime < (current_datetime + dateutil.relativedelta.relativedelta( days = +365 ))): #The second condition is to keep from showing outrageously far off available dates for media that wont ever be available to free users. 
					description = "Only available for premium users. It will be available for free users on "+str(free_available_at)+". \r\n \r\n"+str(media['description'])
				else:
					description = "Only available for "+media['media_type']+" premium users. \r\n \r\n"+str(media['description'])
				
				reason = "Only available for "+media['media_type']+" premium users."
				thumb = "http://static.ak.crunchyroll.com/i/no_image_beta_full.jpg" if media['screenshot_image'] is None else media['screenshot_image']['fwidestar_url'] #because not all shows have thumbnails.
				
				oc.add(DirectoryObject(
					key = Callback(media_unavailable, reason=reason),
					title = str(media['episode_number'])+". "+str(name),
					summary = description.decode('utf-8'),
					thumb = thumb,
					duration = int((float(media['duration']) * 1000))))
					
	#Check to see if anything was returned
	if len(oc) == 0:
		return ObjectContainer(header='No Results', message='No results were found')
	
	return oc
	
####################################################################################################
@route('/video/crunchyroll/media_unavailable')
def media_unavailable(reason):
	return ObjectContainer(header = 'Unavailable', message = reason)

####################################################################################################
@route('/video/crunchyroll/freetrial')
def FreeTrial():
  url = "http://www.crunchyroll.com/freetrial/"
  webbrowser.open(url, new=1, autoraise=True)
  return ObjectContainer(header="Free Trial Signup", message="A browser has been opened so that you may sign up for a free trial. If you do not have a mouse and keyboard handy, visit http://www.crunchyroll.com and sign up for free today!")
	
####################################################################################################
def makeAPIRequest(method, options):
	values = {'session_id':Dict['session_id'], 'version':API_VERSION, 'locale':API_LOCALE} 
	values.update(options)
	request = JSON.ObjectFromURL(API_URL+"/"+method+".0.json", values=values, cacheTime=0, headers=API_HEADERS, timeout=120)	
	return request