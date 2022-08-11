"""Gets video stats from YouTube playlist into a spreadsheet."""
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
import argparse

def pl_to_csv():
    """Main function to go from playlist link to video stats."""
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("sort_by", type=str, help="Sorts data by views (v), likes (l) or likes per view (lpv). Accepts v, l, or lpv.")
        args = parser.parse_args()
        sort_by = args.sort_by
    api_key = open("api_key.txt", "r")
    youtube = build("youtube", "v3", developerKey=api_key.read())  
    api_key.close()
    #setup API
    while True:
        playlist_url = input('Playlist Link? (entire link, should contain "playlist?list=") \n> ')
        if playlist_url.__contains__("playlist?list="):
            break
        else:
            print("Invalid URL (check URL to make sure it's a playlist and not a video). Try again.")
    #get playlist link from user and check its validity
    playlist = playlist_url.replace("https://www.youtube.com/playlist?list=","")
    url_head = "https://www.youtube.com/watch?v="
    token = ""
    titles = []
    views = []
    likes = []
    urls = []
    attempt = 1
    #setup parameters for API call
    try:
        while token is not None:
            pl_request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist,
                maxResults="50",
                pageToken=token
                )
            pl_response = pl_request.execute()
            for pl_item in pl_response["items"]: 
                urls.append(pl_item["contentDetails"]["videoId"])
            #gets individual video ID"s from playlist and creates a list out of them
            video_request = youtube.videos().list(
                part=["statistics","snippet"],
                id=",".join(urls)
                )
            video_response = video_request.execute()
            for video in video_response["items"]:
                titles.append(video["snippet"]["localized"]["title"])
                views.append(video["statistics"]["viewCount"])
                likes.append(video["statistics"]["likeCount"])
            #gets data for each video ID in the previously made list and stores to list
            print(f"Fetched first {attempt*50} results, searching for more...")
            attempt += 1
            token = pl_response["nextPageToken"]
    except:
        #exception ocurrs when there is no nextPageToken, which means that there are no more videos in the playlist
        print("No more data found, preparing for export...")
    likes_per_view = [float(l)/float(v) for l, v in zip(likes, views)]
    lpv_round = [round (lpv, 4) for lpv in likes_per_view]
    #divides like and view list to get the likes/per metric
    links = [url_head + url for url in urls]
    #makes the video ID's clickable links    
    dict = {"Video Title":titles, "Views":views, "Likes":likes, "Likes/View":lpv_round, "Video Links":links}
    df = pd.DataFrame(dict)
    sort_dict = {"v":"Views", "l":"Likes", "lpv":"Likes/View"}
    df[sort_dict[sort_by]] = pd.to_numeric(df[sort_dict[sort_by]])
    df = df.sort_values(by=[sort_dict[sort_by]], ascending=False)
    df.to_csv(f"playlist_data/{playlist}.csv")

pl_to_csv()
