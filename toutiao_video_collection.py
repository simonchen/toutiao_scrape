# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Scraping videos on Toutiao
# Purpose:
#
# Author:      chen
#
# Created:     24/09/2022
# Copyright:   (c) chen 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys, time, subprocess, re, urllib, urllib.request
import simplejson
import xpath
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
#from htmlentity import html_tags_strip, html_entity_decode, hex_decode

_enable_log = True
_cur_dir = os.path.dirname(__file__)
# the cookie is hard-coded fetched from Chrome/Firefox browser when you visits any video url
_cookie = 'MONITOR_WEB_ID=9ba60de7-c6ef-4717-8936-708c47979bde; ttwid=1%7C3Djhd1jtgzA0MNfgJpwuPU2Oa4NN8YA505yBu-lC8y8%7C1664041017%7Cd92369472ba8511f324e68649872368d5d0a04fe1f29eea82317a8ce723b588b; tt_webid=7130883709490923016; ttcid=d23d730e3e664f83a3d7097f73051dca60; csrftoken=4157c19d87f112f2487bbb619670869d; s_v_web_id=verify_l6q4rbv6_P5bgRc8K_3PJ9_4Idv_86E3_w5CcBlw7ftAF; _S_WIN_WH=1280_618; _S_DPR=1.25; _S_IPAD=0; msToken=6ngK53XO8Hw5B60Be1kgmBAytRIHpmMjAtL2uc7Ql3FB2DDxLrHxbiByghDOrdvM-MYdPDSbSVarR4ICds5ivzYhxoP6ZnYgzTK26_885Xlq; _tea_utm_cache_24={%22utm_source%22:%22weixin%22%2C%22utm_medium%22:%22toutiao_android%22%2C%22utm_campaign%22:%22client_share%22}; local_city_cache=%E5%8C%97%E4%BA%AC; _tea_utm_cache_1300={%22utm_source%22:%22weixin%22%2C%22utm_medium%22:%22toutiao_android%22%2C%22utm_campaign%22:%22client_share%22}; tt_scid=qmjyjtTOWgp71vLo3b3ntkkVOTQzEDWJBP2tnrNOfg5N3i3526y4ZGxphmnjM2wMaebd'
video_html_file = '%s/mid_school_grade8_math.htm' %_cur_dir
video_temp_dir = '%s/temp' %_cur_dir
if not os.path.isdir(video_temp_dir):
    os.mkdir(video_temp_dir)
video_output_dir = '%s/output' %_cur_dir
if not os.path.isdir(video_output_dir):
    os.mkdir(video_output_dir)
#print(video_html_file)

def _regular_filename(file_name):
    return re.sub('[\\\/\:\*\?"<>\|]', '_', file_name, flags=re.IGNORECASE)

def _download(link, file_name):
    try:
        with open(file_name, "wb") as f:
            print("Downloading %s" % file_name)
            response = urllib.request.urlopen(link)
            total_length = response.headers.get('Content-Length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                while True:
                    data = response.read(amt=4096)
                    if not data: break
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                    sys.stdout.flush()
    except Exception as e:
        print(str(e))
        return False

    return True

def _merge_video_obsoleted(video_file, audio_file, output_path=''):
    clip_video = VideoFileClip(video_file, audio=False)
    clip_audio = AudioFileClip(audio_file)

    clip_video.audio = clip_audio
    clip_video.write_videofile(output_path)
    clip_video.close()

def _merge_video(video_file, audio_file, output_path=''):
    ffmpeg_exe = os.path.join(_cur_dir, 'ffmpeg', 'ffmpeg-win32-v4.2.2.exe')
    cmd = [ffmpeg_exe, '-y', '-i "%s"' %video_file, '-i "%s"' %audio_file, '-c:v', 'copy', '-c:a', 'copy', '"%s"' %output_path]
    print(' '.join(cmd))
    cmd = subprocess.Popen(' '.join(cmd))
    cmd.wait()

def main():
    success_videos, fail_videos = [], []
    success_log = os.path.join(video_output_dir, 'success.log')
    fail_log = os.path.join(video_output_dir, 'fail.log')

    f = open(video_html_file, 'r', encoding='utf-8')
    html = f.read().encode('utf-16') # chinese double-bytes as clearly
    elems = xpath.search(html, "//div[@class='detail-feed-video-item']")
    print(len(elems))
    video_details = []
    for e in elems:
        vhtml = xpath.inner_html(e)
        vlink = xpath.search(vhtml, "//a[@class='left-img']")
        vtitle = xpath.search(vhtml, "//a[@class='title']")
        video_details.append((vlink[0].attrib.get('href'), vtitle[0].attrib.get('title')))
    for vd in video_details:
        url, title = vd
        filename = _regular_filename(title)
        print ('%s, %s\n' %(url, title))
        final_video_path = os.path.join(video_output_dir, filename+'.mp4')
        if os.path.exists(final_video_path):
            print('\033[93m*** [VIDEO] %s has been downloaded, SKIP ***\033[0m' %(filename+'.mp4'))
            continue
        opener = urllib.request.build_opener()
        opener.addheaders = [('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0')]
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url, headers={'Cookie': _cookie, 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'})
        resp = urllib.request.urlopen(req)
        #print(resp.headers)
        html = resp.read().decode('utf-8')
        elems = xpath.search(html, "//script[@id='RENDER_DATA']")
        if elems:
            json_str = urllib.parse.unquote(elems[0].text_content())
            try:
                json = simplejson.loads(json_str, encoding='utf-8')
                videoPlayInfo = json['data']['initialVideo']['videoPlayInfo']
                dynamic_video = videoPlayInfo.get('dynamic_video')
                if dynamic_video:
                    dynamic_video_list = dynamic_video['dynamic_video_list']
                    dynamic_audio_list = dynamic_video['dynamic_audio_list']
                else:
                    dynamic_video_list = videoPlayInfo.get('video_list')
                    dynamic_audio_list = None
            except Exception as e:
                print(str(e))
                fail_videos.append('%s, %s' %(title, url))
                continue
            # extracting video downloadable link (HD-720p)
            video_max_size = 0
            dynamic_video_url = None
            for video in dynamic_video_list:
                video_meta = video['video_meta']
                size = video_meta['size']
                if size > video_max_size:
                    video_max_size = size
                    dynamic_video_url = video['main_url']
            video_path, audio_path = '', ''
            is_video_download, is_audio_download = False, False
            if dynamic_video_url:
                video_path = os.path.join(video_temp_dir, filename+'_video.mp4')
                print('\ndynamic_video_url=%s' %dynamic_video_url)
                is_video_download = _download(dynamic_video_url, video_path)
            # extracting audio downloadable link
            if dynamic_audio_list:
                dynamic_audio_url = dynamic_audio_list[0]['main_url']
                audio_path = os.path.join(video_temp_dir, filename+'_audio.m4a')
                print('\ndynamic_audio_url=%s' %dynamic_audio_url)
                is_audio_download = _download(dynamic_audio_url, audio_path)
            # merge video / audio files
            if is_video_download and is_audio_download:
                #final_video_path = os.path.join(video_output_dir, filename+'.mp4')
                _merge_video(video_path, audio_path, final_video_path)
                print('\n\033[92mSuccessfully output video: %s\033[0m' %final_video_path)
                success_videos.append('%s, %s' %(title, url))
                time.sleep(5)
            elif is_video_download and not dynamic_audio_list:
                os.rename(video_path, final_video_path)
                print('\n\033[92mSuccessfully output video: %s\033[0m' %final_video_path)
                success_videos.append('%s, %s' %(title, url))
                time.sleep(5)
            else:
                fail_videos.append('%s, %s' %(title, url))
            #print(json_str)
        #sys.exit(0)
    f = open(success_log, 'w')
    f.write('\r\n'.join(success_videos))
    f.close()
    f = open(fail_log, 'w')
    f.write('\r\n'.join(fail_videos))
    f.close()

if __name__ == '__main__':
    #main()
    if len(sys.argv) > 1:
        if sys.argv[1] == '-test_merge_video':
            video_file = r"d:\toutiao\temp\初中数学初二数学八年级数学  第1讲：平移和旋转（1）_video.mp4"
            audio_file = r"d:\toutiao\temp\初中数学初二数学八年级数学  第1讲：平移和旋转（1）_audio.m4a"
            final_video_file = r"d:\toutiao\output\初中数学初二数学八年级数学  第1讲：平移和旋转（1）.mp4"
            _merge_video(video_file,audio_file, final_video_file)
    else:
        main()
