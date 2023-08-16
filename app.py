from flask import Flask, render_template, request
from video_scraper import *  # Import my video scraping script
from pytube import YouTube

app = Flask(__name__)

#TODO: Add in some error handling for inputs
#TODO: Have search results displayed as a separate page
#TODO: Fix the table so that it works with the new flatly theme
#TODO: Clean up the code and document the project

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

        #Get the title of the video
        yt = YouTube(video_url)

        print("This is the dataframe returned to the front end: \n", search_results)
        return render_template('videosearch.html', df_html= search_results, title = yt.title)
    
    return render_template('videosearch.html', df_html= [], title = "")

@app.route('/channelsearch', methods=['GET', 'POST'])
def channelsearch():
    if request.method == 'POST':
        channel_url = request.form['channel_url']
        search_keyword = request.form['search_word']

        # Call the channel search function from video_scraper.py
        df_list, video_titles = search_channel(channel_url, search_keyword)
        
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