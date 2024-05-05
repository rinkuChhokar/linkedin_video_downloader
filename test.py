import requests
from bs4 import BeautifulSoup
import urllib
import json
import uuid


def download_linkedin_video(url):
    # Send a GET request to the LinkedIn post URL
    response = requests.get(url)
    
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <video> tag containing the video URL
    video_tag = soup.find('video')
    
    if video_tag:
        # Extract the data-source attribute 
        data_source_attr = video_tag.get('data-sources')
        if data_source_attr:
            # Parse the json data in the data-source attribute
            data_sources = json.loads(data_source_attr)
            print(data_sources)
            video_url = data_sources[1]['src']

            # Download the video from extracted url
            response_video = requests.get(video_url)
            output_path = f'{uuid.uuid4()}.mp4'
            with open(output_path, 'wb') as f:
                f.write(response_video.content)

            print("Video Successfully Downloaded!!!")

        else:
            print("Video sources not found in the LinkedIn Post")

    else:
        print("Video not found in LinkedIn Post")




linked_post_url = "https://www.linkedin.com/posts/ai-echo_technology-innovation-future-activity-7190303742821314560-_VPx?utm_source=share&utm_medium=member_desktop"
download_linkedin_video(linked_post_url)
