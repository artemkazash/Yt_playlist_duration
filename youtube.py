from googleapiclient.discovery import build
import re
import pyautogui


def playlist_id_from_link(link):
    id_pattern=re.compile(r"(?:(?:\?|&)list=)((?!videoseries)[a-zA-Z0-9_-]*)")
    return id_pattern.findall(link)[0]


# Converts specific youtube duration format to total amount of seconds in a video
def duration_to_seconds(d):
    hours_pattern, minutes_pattern, seconds_pattern = re.compile(r'(\d+)H'), re.compile(r'(\d+)M'), re.compile(r'(\d+)S')
    h, m, s = int(hours_pattern.findall(d)[0])*3600 if hours_pattern.findall(d) else 0, int(minutes_pattern.findall(d)[0])*60 if minutes_pattern.findall(d) else 0,\
             int(seconds_pattern.findall(d)[0]) if seconds_pattern.findall(d) else 0
    return h+m+s


# Covert seconds to hours:minutes:seconds
def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "the total duration is %d:%02d:%02d" % (hour, min, sec)


y_playlist=input('Enter your playlist link: ')
api_key=pyautogui.password(text='Enter your dev_api key', title='', default='', mask='*')
youtube=build('youtube', 'v3', developerKey=api_key)
token=None
id_list=[]
# Extracting all id's of playlist videos
while True:
    playlist = youtube.playlistItems().list(
                part='contentDetails',
                maxResults=50,
                pageToken= token,
                playlistId=playlist_id_from_link(y_playlist)).execute()
    id_list.extend([video['contentDetails']['videoId'] for video in playlist['items']])
    token=playlist.get('nextPageToken')
    if not token: break

# Extracting all durations of playlist videos
duration_list=[youtube.videos().list(part='contentDetails',id=id).execute()['items'][0]['contentDetails']['duration']
               for id in id_list if youtube.videos().list(part='contentDetails',id=id).execute()['pageInfo']['totalResults']]

total_seconds=sum([duration_to_seconds(i) for i in duration_list])
print(convert(total_seconds))

