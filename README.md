# toutiao_scrape
Scraping video list from Toutiao site
Basically, you need to firstly prepare a static HTML file - **mid_school_grade8_math.htm** that contains the video list like &lt;div class="detail-feed-video-item"&gt;...&lt;/div&gt;
(you should catch the video list by viewing html source in browser).
literally, the static html file name means a certain video list for the middle scholl grade 8 math, but you can put any video list written in HTML tagging format.

The main scraping script is **toutiao_video_collection.py**
you should change the variable **_cookie** that's same one as you saw in browser when you visit any video url.

## Prepare a static HTML file 
