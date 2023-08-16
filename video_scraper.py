from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import TranscriptsDisabled
from pytube import YouTube
from pytube import Channel
import scrapetube
import urllib.parse as urlparse
import sys
import pandas as pd
from pprint import pprint

# TODO: Figure out how to search an entire channel for keywords
# TODO: generate Command line interface
# TODO: generate a simple GUI using Django
# TODO: refactor code and put the timestamp generator into its own function (for example)

# Get the video id from the url
# from the following source: https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python
def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse.urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urlparse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None





# Search a single video for a keyword
def search_video(video_tag, search_keyword):
    print("This is the video id tag: " + video_tag)
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_tag)

        print("This is the transcript list size: " + str(sys.getsizeof(transcript_list)))

        # iterate over all available transcripts
        for transcript in transcript_list:
            print("This is the transcript type: " + str(type(transcript)))
            #pprint(vars(transcript))
            

            # the Transcript object provides metadata properties
            """print(
                transcript.video_id,
                transcript.language,
                transcript.language_code,
                # whether it has been manually created or generated by YouTube
                transcript.is_generated,
                # whether this transcript can be translated or not
                transcript.is_translatable,
                # a list of languages the transcript can be translated to
                transcript.translation_languages,
            )
            """
            # fetch the actual transcript data
            #print(transcript.fetch())

            # Figuring out how to search for keyword in the transcript data
            print("Text bruh " + str(transcript.fetch()[-1]))
            #print(next(x for x in transcript.fetch() if x['text'] == "haven't already and I'll see you guys"))
            #print(next((item for item in transcript.fetch() if item['text'] == "guys"), None))
            #print(next((item for item in transcript.fetch() if item['text'].find("guys") != -1), None))

            result = [video_slice for video_slice in transcript.fetch() if video_slice['text'].find(search_keyword) != -1]
            count = 0

            if (len(result) == 0):
                print("\nNo matches found for keyword: " + search_keyword)
                df_html = ""
                return df_html, count

            else:
                print()
                print(result)
                link = 'https://youtu.be/'

                # Define column names
                columns = ["Occurence Time (seconds)", "Timestamp URL", "Transcript Text"]

                # Create a list that will store the intermediate data frame rows
                data = []
                
                #Generate the timestamp links where the keyword was found in the video
                print("\nTimestamps matching keyword: " + search_keyword)

                for item in result:
                    timestamp_url = link + video_tag + '?t=' + str(item['start']-1) + 's'

                    data.append([str(item['start']), timestamp_url, item['text']])
                    print("Transcript text: " + item['text']) 
                    print("Start time: " + str(item['start']))
                    print( "timestamp url: " + timestamp_url + "\n")
                
                # Create a DataFrame
                search_results = pd.DataFrame(data, columns=columns)
                search_results.columns.name = 'Instance'
                search_results.index.name = None
                search_results.index += 1   # Starts the count at 1 instead of the default of zero
                count = len(search_results.index)
                # Convert URLs to HTML anchor tags
                #search_results['Timestamp URL'] = search_results['Timestamp URL'].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')

                print("This is the dataframe: \n", search_results)

                # Convert DataFrame to HTML table
                df_html = search_results.to_html(index= True, escape= False, render_links=True, classes='table table-bordered w3-table-all w3-card-4 table-striped', justify='center')
                print("this is the count returned back: ", count)
                return df_html, count

    except TranscriptsDisabled:
        print("Subtitles are disabled for this video. Unable to search for keyword")
    

    # translating the transcript will return another transcript object
    #print(transcript.translate('en').fetch())


# Search a single video for a keyword
def search_channel(channel_url, search_keyword):
    #c = Channel('https://www.youtube.com/channel/UCjXCAh2R1gwE1WlmNRUNpIg')
        c = Channel(channel_url)

        print("This is the channel name: " + str(c.channel_name))
        print("This is the channel id: " + str(c.channel_id))   

        videos = scrapetube.get_channel(c.channel_id)
        df_list = list()
        video_titles = list()
        count_list = list()

        for video in videos:
            video_tag = video['videoId']
            search_results, keyword_count = search_video(video_tag, search_keyword)
            link = 'https://youtu.be/'
            video_url= link + video_tag
            yt = YouTube(video_url)

            if search_results != "" and search_results != None:
                df_list.append(search_results)
                video_titles.append(yt.title)
                count_list.append(keyword_count)
                print("This is the video URL: ", video_url)
                print("This is the title: ", yt.title)
                print("This is the keyword count: ", keyword_count)

        print("This is the dataframe returned to the front end: \n", df_list)

        return df_list, video_titles, count_list



# Download the video. Specify video URL and optional download path
def download_video(video_url, download_path):
    yt = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
    print(yt.author)
    print(yt.channel_url)

    # Testing out the download video functionality
    yt.streams.filter(file_extension='mp4')
    stream = yt.streams.get_by_itag(22)
    stream.download(output_path=download_path)

# you can also directly filter for the language you are looking for, using the transcript list
#transcript = transcript_list.find_transcript(['de', 'en'])  

# or just filter for manually created transcripts  
#transcript = transcript_list.find_manually_created_transcript(['de', 'en'])  

# or automatically generated ones  
#transcript = transcript_list.find_generated_transcript(['de', 'en'])

#next((transcript for transcript in transcript_list if transcript["text"] == "haven't already and I'll see you guys"), None)
#print(next(x for x in transcript_list if x.text() == "haven't already and I'll see you guys"))