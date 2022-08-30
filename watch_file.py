import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        for fileName in os.listdir(folder_to_track):
            src = folder_to_track+'/'+fileName
folder_to_track=''