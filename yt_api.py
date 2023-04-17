import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from config import CLIENT_SECRET_FILE

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"

def test_credientials(client) -> bool:
	"""
	Given Youbube API client, test to see if it can make connection can be made
	"""
	try:
		request = client.channels().list(
			part="snippet,contentDetails,statistics",
			forUsername="NBA"
		)
		response = request.execute()
		return True
	except Exception as _:
		print("Cilent could not be accessed. Need to reauthorize API.")
		return False
	
def get_authenticated_service():
	"""
	Get credentials and create an API client. Will need to authorize first time and credential will be saved for future use.
	"""
	credential_pickle_file = "./yt_credentials/CREDENTIALS_PICKLE_FILE"
	flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes)

	# Use old credential token if it is exists and still valid. Delete if not valid so we can create new one
	if os.path.exists(credential_pickle_file):
		with open(credential_pickle_file, 'rb') as f:
			credentials = pickle.load(f)
		yt = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
		if test_credientials(yt):
			return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
		os.remove(credential_pickle_file)

	# Creates new credential token if none exist or if previous token is expired
	credentials = flow.run_console()
	with open(credential_pickle_file, 'wb') as f:
		pickle.dump(credentials, f)
	return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

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

youtube = get_authenticated_service()
