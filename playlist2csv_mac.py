import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors
import os, sys
from googleapiclient.discovery import build
#import required libraries

api_key = open("api_key.txt", "r")
youtube = build("youtube", "v3", developerKey=api_key.read())  
api_key.close()
#setup API key to fetch YT data
def pl_to_csv():
    playlist_url = input('Playlist Link? (whole thing, should contain "playlist?list=") \n>')

    while True:
        if playlist_url.__contains__("playlist?list="):
            break
        else:
            print("Invalid URL (check URL to make sure it's a playlist and not a video). Try again.")
            playlist_url = input('Playlist Link? (whole thing, should contain "playlist?list=") \n>')
    
    playlist = playlist_url.replace('https://www.youtube.com/playlist?list=','')
    urlHead = 'https://www.youtube.com/watch?v='
    token = ''
    csvTitles = []
    csvViews = []
    csvLikes = []
    urlList = []
    print('Countdown:')
    try:
        while token is not None:
            print('t')
            vid_ids=[]
            titles = []
            views = []
            likes = []
            
            pl_request = youtube.playlistItems().list(
                part = 'contentDetails',
                playlistId = playlist,
                maxResults = '10',
                pageToken = token
                )
            pl_response = pl_request.execute()  #gets contentDetails of playlist
            
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

            csvTitles.extend(titles)
            csvViews.extend(views)
            urlList.extend(vid_ids)     #aggregate the desired lists with extend function
            csvLikes.extend(likes)

            token = pl_response['nextPageToken']
    except:
        pass
   
    likesPerView = [float(l)/float(v) for l,v in zip(csvLikes, csvViews)]
    csvLikesPerView = [round (i, 4) for i in likesPerView]      #divides the like list and the view list

    csvLinks = [urlHead + j for j in urlList]   #makes the video ID's clickable links
        
    dict = {'Video Title': csvTitles, 'Views': csvViews, 'Likes/View': csvLikesPerView, 'Video Links':csvLinks}
    df = pd.DataFrame(dict)
    df.to_csv('PlaylistData.csv')            #formats and saves lists to a .csv

pl_to_csv()