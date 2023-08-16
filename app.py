from flask import Flask, render_template, request
from video_scraper import *  # Import my video scraping script
from pytube import Channel
from pytube import YouTube
import scrapetube

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('videosearch.html', df_html= [])  # Default to video search tab

@app.route('/videosearch', methods=['GET', 'POST'])
def videosearch():
    if request.method == 'POST':
        video_url = request.form['video_url']
        search_keyword = request.form['search_word']

        video_tag = video_id(video_url)
        
        # Call the video search function from video_scraper.py
        search_results = search_video(video_tag, search_keyword)

        print("This is the dataframe returned to the front end: \n", search_results)
        return render_template('videosearch.html', df_html= search_results)
    
    return render_template('videosearch.html', df_html= [])

@app.route('/channelsearch', methods=['GET', 'POST'])
def channelsearch():
    if request.method == 'POST':
        channel_url = request.form['channel_url']
        search_keyword = request.form['search_word']
        #c = Channel('https://www.youtube.com/channel/UCjXCAh2R1gwE1WlmNRUNpIg')
        c = Channel(channel_url)

        print("This is the channel name: " + str(c.channel_name))
        print("This is the channel id: " + str(c.channel_id))   

        videos = scrapetube.get_channel(c.channel_id)
        df_list = list()
        video_titles = list()
        count = 0

        for video in videos:
            count += 1
            video_tag = video['videoId']
            search_results = search_video(video_tag, search_keyword)
            link = 'https://youtu.be/'
            video_url= link + video_tag
            yt = YouTube(video_url)

            if search_results != "" and search_results != None:
                df_list.append(search_results)
                video_titles.append(yt.title)
                print("This is the video URL: ", video_url)
                print("This is the title: ", yt.title)
        print(count)

        print("This is the dataframe returned to the front end: \n", df_list)
        return render_template('channelsearch.html', df_html= df_list, titles_list = video_titles, zip=zip)
    return render_template('channelsearch.html', df_html= [], titles_list = [], zip=zip)

@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html')  # Default to video search tab

"""def index():
    if request.method == 'POST':
        action = request.form['action']
        video_url = request.form['video_url']
        search_keyword = request.form['search_word']

        video_tag = video_id(video_url)
        

        if action == 'search channel':
            # Call the channel search function from video_scraper.py
            print("Placeholder code")

        if action == 'search video':
            # Call the video search function from video_scraper.py
            search_results = search_video(video_tag, search_keyword)

            print("This is the dataframe returned to the front end: \n", search_results)
            return render_template('index.html', df_html= search_results)
        
    return render_template('index.html', df_html=None)
"""

"""@app.route('/videosearch')
def about():
    return render_template('videosearch.html')

@app.route('/channelsearch')
def contact():
    return render_template('channelsearch.html')"""

if __name__ == '__main__':
    app.run(debug=True)