import json
import logging
import threading
from logging.handlers import RotatingFileHandler

# Constants for file names
POSTS_FILE = 'posts.json'
LOG_FILE = 'posts.log'
file_lock = threading.Lock()  # Lock for thread-safe file access

logger = None

def initLogger(appLogger):
    global logger
    logger = appLogger

# Function to read posts from the JSON file
def readPosts():
    with file_lock:
        try:
            with open(POSTS_FILE, 'r') as f:
                return json.load(f)  # Load and return JSON data
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Return an empty list if the file doesn't exist or is empty

# Function to write posts to the JSON file
def writePosts(posts):
    with file_lock:
        with open(POSTS_FILE, 'w') as f:
            json.dump(posts, f, indent=4, ensure_ascii=False)  # Write JSON data with indentation

# Function to append a log entry to the log file
def appendLog(entry):
    with file_lock:
        with open(LOG_FILE, 'a') as logFile:
            logFile.write(json.dumps(entry, ensure_ascii=False) + '\n')  # Append JSON data to log file

# Generic function to log and append an entry
def logAndAppend(entry_type, content):
    entry = {"type": entry_type, "content": content}
    posts = readPosts()
    posts.append(entry)
    writePosts(posts)
    appendLog(entry)
    if logger:
        logger.info(json.dumps(entry, ensure_ascii=False))
