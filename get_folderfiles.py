# -*- coding: utf-8 -*-
#get_folderfiles:
#This codes get a specific folder ID in Google Drive and a list of file 
#in the folder. Google Drive adopts a flat file system but you can spcify
#the absolute folder path such as '\\user\\me\\my folder'. 
#This codes return a file list, folder id, and Google Drive API object.
#python get_folderfiles.py '\\user\\me\\my folder'
#
#Before starting, create creds_file, 'credentials.json', by downloading it from Google Cloud Platform.
#See APIs & Services -> Credentials -> OAuth 2.0 Client IDs.
#
from __future__ import print_function
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pprint
import sys
import os
import logging
from apiclient import errors as api_errors, http as api_http
from _stat import filemode

#log file
log_file = 'debug.log.txt'

logger = logging.getLogger(__name__)

#files for authorizing
creds_file = 'credentials.json'
token_file = 'token.pickle'
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
#Default folder. Specify absolute folder path. 
#You can also use a command line argument.
folder = 'root'
service = {}
parentid = None
filelist = []

##logging
MYFORMAT = '[%(asctime)s]%(filename)s(%(lineno)d): %(message)s'
logging.basicConfig(
    filename = log_file,
    filemode = 'w', # Default is 'a'
    format = MYFORMAT, 
    datefmt = '%Y-%m-%d %H:%M:%S', 
    level = logging.DEBUG)
##
##
def auth_googledrive(creds_file=creds_file, token_file=token_file):
#This is Python quickstart codes shown in Google Drive API v3.
#Create creds_file, 'credentials.json', by downloading it from Google Cloud Platform.
#See APIs & Services -> Credentials -> OAuth 2.0 Client IDs.
    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return creds
##

##search files in a folder shown by a parentid
def get_filelist_sub(service=service, parentid=parentid):
    q = f"'{parentid}' in parents and trashed!=true".format(parentid)
    k=()
    try:
        k = service.files().list(q=q,fields="nextPageToken, files(id, name)").execute()
    except api_errors.HttpError as error:
        logger.error('HTTP error in get_filelist_sub: %s', error)
    except:
        logger.error('An error occurred in get_filelist_sub: [%s] %s ', sys.exc_info()[0], sys.exc_info()[1])
    return k

##get file names in a specific folder    
def get_filelist(service=service, folder=folder):
# folder = path to the specific folder
# returns: filelist: file names in the specific folders
#          parentid: id in the parent folder     

    if '\\' in folder:
        setPath=folder.split('\\')
    else:
        setPath = folder.split('/')
    filelist=None
    parentid = 'root'
    
    #first attempt to check the files in a root folder
    try:
        filelist = get_filelist_sub(service, 'root')
    except:
        logger.error('An error occurred in get_filelist: [%s] %s ', sys.exc_info()[0], sys.exc_info()[1])
    if len(setPath)>1:
        #the attempts after searching a root folder
        for i in setPath:
            parentid = [x['id'] for x in filelist['files'] if x['name'] == i]
            parentid = parentid[0] if len(parentid) else ''
            if parentid:
                try:
                    filelist = get_filelist_sub(service, parentid)
                except:
                    logger.error('An error occurred in get_filelist: [%s] %s ', sys.exc_info()[0], sys.exc_info()[1])
    return filelist, parentid
                    
def get_folderfiles(folder=folder):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
#Google Drive autorization
    creds = auth_googledrive(creds_file, token_file)
#open API service
    service = build('drive', 'v3', credentials=creds)
#get filelist with parentid in a specific folder (path)
    filelist, parentid = get_filelist(service, folder)
    return filelist, parentid, service

if __name__ == '__main__':
    value = sys.argv
    if len(value) > 1:
        folder=value[1]
    get_folderfiles(folder)