# toutiao_scrapetoutiao_scrape
Scraping video list from Toutiao site
Basically, you'll need to firstly prepare a static HTML file - **mid_school_grade8_math.htm** that contains the video list like &lt;div class="detail-feed-video-item"&gt;...&lt;/div&gt;
(you should catch the video list by viewing html source in browser, see below.)

![How to capture the video list by the inspector in browser](dev_screenshots/github_toutiao_scrape_1.png)
![How to capture the video list by the inspector in browser](dev_screenshots/github_toutiao_scrape_2.png)

literally, the static html file name means a certain video list for the middle scholl grade 8 math, but you can put any video list written in HTML tagging format.

The main scraping script you run is **toutiao_video_collection.py**
'''
python toutiao_video_collection.py
'''
you might change the variable **_cookie** that's same one as you saw in browser when you visited any video url.

