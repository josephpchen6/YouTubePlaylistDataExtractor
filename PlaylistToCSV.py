import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors
import csv
import os, sys
import time
from googleapiclient.discovery import build     #import required libraries

api_key='AIzaSyBfdmU778gN0cTc9C-IMBtlUOTl2Rt3x6s'
youtube = build('youtube', 'v3', developerKey=api_key)  #setup API key to fetch YT data

print('Playlist Link? (whole thing)')
playlistUrl = input()
playlist = playlistUrl.replace('https://www.youtube.com/playlist?list=','')

print('Playlist Length?')
playlistLength = input()
num = (int(playlistLength)-1) // 5

def mainDebug():    
    print(token)
    print(titles)
    print(views)
    print(vid_ids)

def extraDebug():
    print(extraTitles)
    print(extraViews)
    print(extraIds)
    
def finalDebug():
    print(csvTitles)
    print(csvViews)
    print(csvList)

urlHead = 'https://www.youtube.com/watch?v='
token = ''
csvTitles = []
csvViews = []
csvLikes = []
urlList = []
print('Countdown:')

for count in range(int(num)):
    print(num)
    num = int(num)-1
    vid_ids=[]
    titles = []
    views = []
    likes = []
    
    pl_request = youtube.playlistItems().list(
        part = 'contentDetails',
        playlistId = playlist,
        maxResults = '5',
        pageToken = token
        )
    pl_response = pl_request.execute()  #gets contentDetails of playlist

    pageKey_request = youtube.playlistItems().list(
        part = 'id',
        playlistId = playlist,
        pageToken = token
        )
    pageKey_response = pageKey_request.execute()

    for a in pl_response['items']: 
        vid_ids.append(a['contentDetails']['videoId'])  #gets list of video IDs off the playlist's videos

    idCopy = vid_ids       #creates a copies of the video ID list for processing
    token = ''
    
    stat_request = youtube.videos().list(
        part="statistics",
        id=','.join(vid_ids)     #joins the video ID's with commas
         
        )
    stat_response = stat_request.execute()    #gets statistics off a video

    title_request = youtube.videos().list(
        part='snippet',
        id=','.join(idCopy)    #joins the video titles with commas
        )
    title_response = title_request.execute()    #gets snippet off a video

    for b in title_response['items']:
        titles.append(b['snippet']['localized']['title'])   #gets the title of a video from the video ID list copy
                      
    for c in stat_response['items']:
        views.append(c['statistics']['viewCount'])      #gets the view count of a video from the video ID list copy
        likes.append(c['statistics']['likeCount'])      #also gets the like count of the video

    for d in pageKey_response['nextPageToken']:
        token = token + d
#    print(token)       #remove for debug
    
    csvTitles.extend(titles)
    csvViews.extend(views)
    urlList.extend(vid_ids)     #aggregate the desired lists with extend function
    csvLikes.extend(likes)
    #mainDebug()

extraIds = []
extraTitles = []
extraViews = []
extraLikes = []

remainderId_request = youtube.playlistItems().list(
    part = 'contentDetails',
    playlistId = playlist,
    pageToken = token
    )
remainderId_response = remainderId_request.execute()        #manual function for the last page with no "nextPageToken'
    
for e in remainderId_response['items']:
    extraIds.append(e['contentDetails']['videoId'])
    
remainderTitle_request = youtube.videos().list(
    part = 'snippet',
    id = ','.join(extraIds)
    )
remainderTitle_response = remainderTitle_request.execute()

extraIdCopy = extraIds

for f in remainderTitle_response['items']:
    extraTitles.append(f['snippet']['localized']['title'])

remainderStat_request = youtube.videos().list(
    part = 'statistics',
    id = ','.join(extraIdCopy)
    )
remainderStat_response = remainderStat_request.execute()

for g in remainderStat_response['items']:
    extraViews.append(g['statistics']['viewCount'])
    extraLikes.append(g['statistics']['likeCount'])

csvTitles.extend(extraTitles)
csvViews.extend(extraViews)
urlList.extend(extraIds)
csvLikes.extend(extraLikes)
#finalDebug()
#extraDebug()

likesPerView = [float(l)/float(v) for l,v in zip(csvLikes, csvViews)]
csvLikesPerView = [round (h, 4) for h in likesPerView]      #divides the like list and the view list

fileMake = open('list.csv', 'w+')

filePath = os.path.abspath(fileMake.name)

fileMake.close()

print('Manual Sample or Playlist? (m/p)')
linkPrompt = input()
if linkPrompt == 'm':
    csvLinks = [urlHead + i for i in urlList]   #makes the video ID's clickable links
    
elif linkPrompt == 'p':
    csvLinks = urlList      #keeps the videoID's intact for playlist creation
    print('Reminder: sort smallest to largest for playlist creation')
    os.system('open /Users/josephchen/Library/Python/IDbeta.py')

else:
    print('exit')
    exit()

dict = {'Video Title': csvTitles, 'Views': csvViews, 'Likes/View': csvLikesPerView, 'Video Links':csvLinks}
df = pd.DataFrame(dict)
df.to_csv('list.csv')            #formats and saves lists to a .csv
os.system('open ' + filePath)
