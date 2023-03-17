'''
Functions to rate the NBA game
'''
import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "path/to/client_secret_file"

def get_authenticated_service():
	"""
	Get credentials and create an API client. Will need to authorize first time and credential will be saved for future use.
	"""
	credential_pickle_file = "path/to/credential_pickle_file/"
	flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
	if os.path.exists(credential_pickle_file):
		with open(credential_pickle_file, 'rb') as f:
			credentials = pickle.load(f)
	else:
		credentials = flow.run_console()
		with open(credential_pickle_file, 'wb') as f:
			pickle.dump(credentials, f)
	return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

youtube = get_authenticated_service()

def get_channel(channel_username = "") -> str:
	"""
	Return channel id
	"""
	request = youtube.channels().list(
		part="snippet,contentDetails,statistics",
		forUsername=channel_username
	)
	response = request.execute()
	return response['items'][0]['id']

def get_playlist(channel_id:str, playlist_title:str) -> str:
	"""
	Search for a specific playlist within a channel and return that playlist
	"""
	request = youtube.playlists().list(
	part="snippet,contentDetails",
	channelId=channel_id,
	maxResults=25
	)
	response = request.execute()

	# Finds desired playlist
	playlist_id = ""
	for playlist in response['items']:
		if playlist['snippet']['title'] == playlist_title:
			playlist_id = playlist['id']

	return playlist_id

def get_playlist_items(playlist_id:str) -> list:
	"""
	Return items in a given playlist
	"""
	request = youtube.playlistItems().list(
		part="snippet,contentDetails",
		maxResults=10,
		playlistId=playlist_id
	)

	response = request.execute()
	return response['items']

def get_videos_from_playlist(channel_username: str, playlist_title: str) -> list:
	"""
	Return videos from a playlist of a channel
	"""
	channel_id = get_channel(channel_username)
	playlist_id = get_playlist(channel_id, playlist_title)
	playlist_items = get_playlist_items(playlist_id)
	return playlist_items

