# toutiao_scrape
Scraping video list from Toutiao site
Basically, you need to firstly prepare a static HTML file that contains the video list like &lt;div class="detail-feed-video-item"&gt;...&lt;/div&gt;
(you can catch the video list by viewing html source in browser).

The main scraping script is **toutiao_video_collection.py**
you should change the variable **_cookie** that's same one as you saw in browser when you visit any video url.

## Prepare a static HTML file 
