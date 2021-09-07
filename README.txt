IMPORTANT:
Avoid installing multiple times- future installations will have spaces in
the directory path, resulting in the .csv file being unable to open. Delete
old files before reinstalling, or rename file to something without a space.
Similarly, avoid putting the file into a directory with a space (i.e.
enclosing folder has space) for full effect.

Description:
Paste YouTube playlist link into shell (A playlist link looks like this:
https://www.youtube.com/playlist?list=;
click "VIEW FULL PLAYLIST" if using YouTube search). A .csv file
will be opened, containing a spreadsheet with the video titles,
views, likes, likes per view, and clickable links.

Required directories:
-pandas (pip install pandas)
-googleapiclient.discovery (pip install google-api-python-client)

**Make sure to install correct version based on OS (Windows/Mac)**

Currently working on:
Directly export .csv into a youtube playlist (need more quotas)
Linux Version
