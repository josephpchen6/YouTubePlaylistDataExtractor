import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors
import os, sys
from googleapiclient.discovery import build     #import required libraries

api_key = open("api_key.txt", "r")
youtube = build('youtube', 'v3', developerKey=api_key.read())  #setup API key to fetch YT data
api_key.close()

plCount = []

print('Playlist Link? (whole thing)')
playlistUrl = input()
playlist = playlistUrl.replace('https://www.youtube.com/playlist?list=','')

pl_lengthRequest = youtube.playlists().list(
    id = playlist,
    part = 'contentDetails',
    )
pl_lengthResponse = pl_lengthRequest.execute()
length = pl_lengthResponse['items'][0]['contentDetails']['itemCount']

num = int((length-1)/5)    #turns list into string and divides by 5 for later use

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

    for b in pl_response['items']: 
        vid_ids.append(b['contentDetails']['videoId'])  #gets list of video IDs off the playlist's videos

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

    for c in title_response['items']:
        titles.append(c['snippet']['localized']['title'])   #gets the title of a video from the video ID list copy
                      
    for d in stat_response['items']:
        views.append(d['statistics']['viewCount'])      #gets the view count of a video from the video ID list copy
        likes.append(d['statistics']['likeCount'])      #also gets the like count of the video

    for e in pageKey_response['nextPageToken']:
        token = token + e
    #print(token)       #remove for debug
    
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
    
for f in remainderId_response['items']:
    extraIds.append(f['contentDetails']['videoId'])
    
remainderTitle_request = youtube.videos().list(
    part = 'snippet',
    id = ','.join(extraIds)
    )
remainderTitle_response = remainderTitle_request.execute()

extraIdCopy = extraIds

for g in remainderTitle_response['items']:
    extraTitles.append(g['snippet']['localized']['title'])

remainderStat_request = youtube.videos().list(
    part = 'statistics',
    id = ','.join(extraIdCopy)
    )
remainderStat_response = remainderStat_request.execute()

for h in remainderStat_response['items']:
    extraViews.append(h['statistics']['viewCount'])
    extraLikes.append(h['statistics']['likeCount'])

csvTitles.extend(extraTitles)
csvViews.extend(extraViews)
urlList.extend(extraIds)
csvLikes.extend(extraLikes)
#finalDebug()
#extraDebug()

likesPerView = [float(l)/float(v) for l,v in zip(csvLikes, csvViews)]
csvLikesPerView = [round (i, 4) for i in likesPerView]      #divides the like list and the view list

fileMake = open('PlaylistData.csv', 'w+')

filePath = os.path.abspath(fileMake.name)

fileMake.close()

csvLinks = [urlHead + j for j in urlList]   #makes the video ID's clickable links
    
dict = {'Video Title': csvTitles, 'Views': csvViews, 'Likes/View': csvLikesPerView, 'Video Links':csvLinks}
df = pd.DataFrame(dict)
df.to_csv('PlaylistData.csv')            #formats and saves lists to a .csv
