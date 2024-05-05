from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from bs4 import BeautifulSoup
import json
import uuid


app = Flask(__name__)
app.secret_key = "key123"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video', methods=['POST'])
def video():
    linkedin_post_url = request.form["link-input"]  
    print(linkedin_post_url)
    try:
        poster_url, video_url = get_linkedin_video_thumbnail(linkedin_post_url)
        flash("Video Downloaded Successfully!!", "success")
        return render_template('download_page.html', data = {'video_thumbnail':poster_url, 'video_url': video_url})
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('index'))



def get_linkedin_video_thumbnail(url):
    # Send a GET request to the LinkedIn post URL
    response = requests.get(url)
    
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <video> tag containing the video URL
    video_tag = soup.find('video')
    
    if video_tag:
        # Extract the data-source attribute 
        data_poster_url = video_tag.get('data-poster-url', '')
        if data_poster_url:
            return data_poster_url, url

def download_linkedin_video(url, video_resolution):
    # Send a GET request to the LinkedIn post URL
    response = requests.get(url)
    
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <video> tag containing the video URL
    video_tag = soup.find('video')
    
    if video_tag:
        # Extract the data-sources attribute
        data_sources_attr = video_tag.get('data-sources')
        if data_sources_attr:
            # Parse the JSON data in data-sources attribute
            data_sources = json.loads(data_sources_attr)
            
            # Choose one of the available video sources (e.g., the first one)
            video_quality_index = 0
            if video_resolution == "480p":
                video_quality_index = 0
            else:
                video_quality_index = 1

            video_url = data_sources[video_quality_index]['src']
            
            # Generate a unique filename for the video
            output_path = str(uuid.uuid4()) + ".mp4"
            
            # Download the video using the extracted URL
            response = requests.get(video_url)
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
            print("Video downloaded successfully:")
        else:
            raise Exception("Video sources not found in the LinkedIn post.")
    else:
        raise Exception("Video not found in the LinkedIn post.")


@app.route("/download", methods=['POST'])
def download():
    linkedin_post_url = request.form['video_url']
    video_resolution = request.form['video_resolution']
    try:
        download_linkedin_video(linkedin_post_url, video_resolution)
        flash("Video downloaded successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    return render_template("success.html")
    # return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)