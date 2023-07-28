from googleapiclient.discovery import build
import pandas as pd
from IPython.display import JSON
from dateutil import parser
import isodate
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# # NLP
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
# from wordcloud import WordCloud

from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("youtube_api_key")


channel_ids = ['UCIUt1auGAZGqo3jmeP-LB1g']


api_service_name = "youtube"
api_version = "v3"
# Get credentials and create an API client
youtube = build(api_service_name, api_version, developerKey=api_key)


def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids))
    response = request.execute() 
    
    for i in range(len(response['items'])):
        data = dict(channelName = response['items'][i]['snippet']['title'],
                    subscribers = response['items'][i]['statistics']['subscriberCount'],
                    views = response['items'][i]['statistics']['viewCount'],
                    totalVideos = response['items'][i]['statistics']['videoCount'],
                    playlistId = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    
    return pd.DataFrame(all_data)


channel_stats = get_channel_stats(youtube, channel_ids)

channel_stats.to_csv("vtl_youtube_data.csv")


