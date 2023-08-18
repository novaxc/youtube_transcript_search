from flask import Flask, render_template, request
from video_scraper import *  # Import my video scraping script
from pytube import YouTube

app = Flask(__name__)

#TODO: Add in some error handling for inputs (try/catch blocks)
#TODO: Clean up the code and document the project
#TODO: Make the channel Regex better (especially for handling the new channel handles that youtube has)
#TODO: Look into form input pattern checking for channel urls and video urls (either at form input level or backend level)


@app.route('/', methods=['GET', 'POST'])
def home():
    # Displays the home page and defaults to the video search page

    return render_template('videosearch.html', df_html= [])  # Default to video search tab


@app.route('/videosearch', methods=['GET', 'POST'])
def videosearch():
    # Displays a form to gather user input for the video search functionality

    if request.method == 'POST':
        video_url = request.form['video_url']
        search_keyword = request.form['search_word']

        video_tag = video_id(video_url)
        
        # Call the video search function from video_scraper.py
        search_results, keyword_count = search_video(video_tag, search_keyword)

        #Get the title of the video
        yt = YouTube(video_url)

        print("This is the dataframe returned to the front end: \n", search_results)
        return render_template('videoresults.html', df_html= search_results, title = yt.title, keyword_count=keyword_count, search_keyword=search_keyword)
    
    return render_template('videosearch.html', df_html= [], title = "", keyword_count=0)


@app.route('/channelsearch', methods=['GET', 'POST'])
def channelsearch():
    # Displays a form to gather user input for the channel search functionality

    if request.method == 'POST':
        channel_url = request.form['channel_url']
        search_keyword = request.form['search_word']

        # Call the channel search function from video_scraper.py
        df_list, video_titles, count_list, channel_name = search_channel(channel_url, search_keyword)
        
        return render_template('channelresults.html', df_html= df_list, titles_list = video_titles, count_list = count_list, search_keyword=search_keyword, channel_name=channel_name, zip=zip)
    return render_template('channelsearch.html', df_html= [], titles_list = [], count_list = [], zip=zip)


@app.route('/videoresults', methods=['GET', 'POST'])
def videoresults():
    # Displays the HTML table results representing all the instances where the keyword was found in the video

    return render_template('videoresults.html')  


@app.route('/channelresults', methods=['GET', 'POST'])
def channelresults():
    # Displays the HTML table results representing all the instances where the keyword was found for each video
    # in the channel

    return render_template('channelresults.html')  

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