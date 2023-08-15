from flask import Flask, render_template, request
from video_scraper import *  # Import your video scraping script

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('base.html')  # Default to video search tab

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
    return render_template('channelsearch.html')

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