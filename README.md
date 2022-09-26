# toutiao_scrape
A simple script does scraping video list from Toutiao (Toutiao or Jinri Toutiao is a Chinese news and information content platform, a core product of the China-based company ByteDance）

Basically, you'll need to firstly prepare a static HTML file - **mid_school_grade8_math.htm** that contains the video list such as HTML structure like &lt;div class="detail-feed-video-item"&gt;...&lt;/div&gt;
(you should catch the video list by viewing html source in browser, see below.)

![How to capture the video list by the inspector in browser](dev_screenshots/github_toutiao_scrape_1.png)
![How to capture the video list by the inspector in browser](dev_screenshots/github_toutiao_scrape_2.png)

literally, the static html file name means a certain video list for the middle scholl grade 8 math, but you can put any video list written in HTML tagging format.

The main scraping script you run is **toutiao_video_collection.py**
```
python toutiao_video_collection.py
```

When running the main script, you probably need to change the **_cookie**[^note] variable fetching from your browser > inspector > network
Here is a simple footnote[^1].

A footnote can also have multiple lines[^2].  

You can also use words, to fit your writing style more closely[^note].

[^1]: My reference.
[^2]: Every new line should be prefixed with 2 spaces.  
  This allows you to have a footnote with multiple lines.
[^note]:
    Named footnotes will still render with numbers instead of the text but allow easier identification and linking.  
    This footnote also has been made with a different syntax using 4 spaces for new lines.


## Required python libs
```
pip install simplejson
pip install lxml
```

## Peformance
Most of videos have been separated as video / audio files (i.e, extension .mp4 with video frames and extension .m4a with audio)
after scraping the two video / audio files, ffmpeg does combine them as a single final video file as quite quickly using the method **c:v copy c:a copy**
the [moviepy](https://pypi.org/project/moviepy/) has ability to do same combination, but it's quite slowly, so it's not recommended in the use.

# Warning
You can use the codes for free for personal purpose only, you will be responsible for any legal suit in commercial usage.
