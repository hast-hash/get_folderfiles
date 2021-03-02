# get_folderfiles
This codes get a specific folder ID and a list of file in the folder in Google Drive by specifying an absolute path.
Google Drive adopts a flat file system but you can spcify the absolute folder path such as '\\user\\me\\my folder'. 
This codes return a file list, folder id, and Google Drive API object, respectively.<BR>
<BR>
Usage:<BR>
&nbsp;&nbsp;&nbsp;&nbsp;python get_folderfiles.py '\\user\\me\\my folder'<BR>
OR<BR>
&nbsp;&nbsp;&nbsp;&nbsp;filelist, folderid, service = get_folderfiles('\\user\\me\\my folder')<BR>
<BR>
Before starting, create a credential file, 'credentials.json', by downloading it from Google Cloud Platform.
See APIs & Services -> Credentials -> OAuth 2.0 Client IDs.<BR>
