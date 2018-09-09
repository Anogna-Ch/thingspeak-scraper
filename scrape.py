import sys
import urllib2
from bs4 import BeautifulSoup
import re
from urlparse import *
import json
from os import walk
from langdetect import detect



#TODO
# add videos
# api_key might get trigger apis

# https://thingspeak.com/channels/22793 gets most things...

#need gauges (offline and online) and gauge options
#need api calls
#need /apps/matlab_visualizations/

# not counting gauges correctly  /html/body  gauge1_div gauge2_div (gauges are only widget atm)
# <div id="window_1158981" class="window-container">

reload(sys)  
sys.setdefaultencoding('utf8')

filenames = []
remote = True # change to go to the web
base_url = 'https://thingspeak.com/'
max_page = 0
dump = "["

class Matlab:
    title = ""

    def __init__(self):
        self.title = ""

    def fix(self, value):
        return value.encode('utf-8').strip().replace('"', "'").replace("\\", "-")

    def fix_all(self):
        self.title = self.fix(self.title)

    def to_json(self):
        self.fix_all()
        json_str = '"title": ' + self.title

class Maps:
    title = ""

    def __init__(self):
        self.title = ""

    def fix(self, value):
        return value.encode('utf-8').strip().replace('"', "'").replace("\\", "-")

    def fix_all(self):
        self.title = self.fix(self.title)

    def to_json(self):
        self.fix_all()
        json_str = '"title": ' + self.title

class Gauge:
    max_val = ""
    min_val = ""
    gauge_name = ""
    interval_val = ""
    options = ""

    def __init__(self):
        self.max_val = ""
        self.min_val = ""
        self.gauge_name = ""
        self.interval_val = ""
        self.options = ""

    def fix(self, value):
        return value.encode('utf-8').strip().replace('"', "'").replace("\\", "-")

    def fix_all(self):
        self.max_val = self.fix(self.max_val)
        self.min_val = self.fix(self.min_val)
        self.gauge_name = self.fix(self.gauge_name)
        self.interval_val = self.fix(self.interval_val)
        self.options = self.fix(self.options)

    def to_json(self):
        self.fix_all()
        json_str = '"max_val": "'+self.max_val+'", "min_val": '+self.min_val+'", "gauge_name:" '+self.gauge_name+'", "interval_val": ' +self.interval_val+'", "options": ' + self.options+'"'
        return json_str


class Chart:
    title = ""
    second_title = ""
    xaxis = ""
    yaxis = ""
    chart_type = ""
    results  = ""
    header = ""
    url = ""

    def __init__(self):
        self.title = ""
        self.second_title = ""
        self.xaxis = ""
        self.yaxis = ""
        self.chart_type = ""
        self.results  = ""
        self.header = ""
        self.url = ""

    def fix(self, value):
        return value.encode('utf-8').strip().replace('"', "'").replace("\\", "-")

    def fix_all(self):
        self.title = self.fix(self.title)
        self.second_title = self.fix(self.second_title)
        self.xaxis = self.fix(self.xaxis)
        self.yaxis = self.fix(self.yaxis)
        self.chart_type = self.fix(self.chart_type)
        self.results  = self.fix(self.results)
        self.header = self.fix(self.header)
        self.url = self.fix(self.url)

    def to_json(self):
        self.fix_all()
        json_str = '"title": "'+self.title+'", "second_title": "'+self.second_title+'", "xaxis": "'+self.xaxis+'", "yaxis": "'+self.yaxis+'", "chart_type": "'+self.chart_type+'", "results": "'+self.results+'", "header": "'+self.header+'"'
        return json_str


class Comment:
    author = ""
    creation_time = ""
    text = ""
    
    def __init__(self):
        author = ""
        creation_time = ""
        text = ""
    
    def fix(self, value):
        return value.encode('utf-8').strip().replace('"', "'").replace("\\", "-")

    def fix_all(self):
        self.author = self.fix(self.author)
        self.creation_time = self.fix(self.creation_time)
        self.text = self.fix(self.text)
    
    def to_json(self):
        self.fix_all()
        json_str = '"author": "' + self.author + ', "creation_time": "' + self.creation_time + ', "text": "' + self.text + '"'  
        return json_str

class Channel:
    name = ""
    url = ""
    author = ""
    disc = ""
    tags = ""
    charts = ""
    comments = ""
    create_time = ""
    shares = ""
    language = ""
    num_videos = 0
    maps = ""
    matlabs = ""

    html = ""

    def pretty_print(self):
        print "\tname: " + self.name.encode('utf-8').strip()
        print "\turl: " + self.url.encode('utf-8').strip()
        print "\tauthor: " + self.author.encode('utf-8').strip()
        print "\tdisc: " + self.disc.encode('utf-8').strip()
        print "\ttags: " + str(self.tags).encode('utf-8').strip()
        print "\tcharts:" + str(self.charts).encode('utf-8').strip()
        print "\tcomments:" + str(self.comments).encode('utf-8').strip()
        print "\tcreate_time:" + str(self.create_time).encode('utf-8').strip()
        print "\tshares:" + str(self.shares).encode('utf-8').strip()
        print "\tlanguage:" + str(self.language).encode('utf-8').strip()
        print "\tnum_videos:" + str(self.num_videos).encode('utf-8').strip()
        print "\tmaps:" + str(self.maps).encode('utf-8').strip()
        print "\tmatlabs:" + str(self.matlabs).encode('utf-8').strip()
        #print "\thtml:" + self.html.encode('utf-8').strip()

    def dump_html(self):
        f = open("html/"+self.url.encode("utf-8").split("/")[-1]+".html", "w")
        f.write(self.html.encode("utf-8"))

    def fix(self, value):
        return value.encode('utf-8').strip().replace('"', "'").replace("\\", "-")

    def fix_all(self):
        self.name = self.fix(self.name)
        self.url = self.fix(self.url)
        self.author = self.fix(self.author)
        self.disc = self.fix(self.disc)
        self.tags = self.fix(self.tags)
        self.shares = self.fix(self.shares)
        self.charts = self.fix(self.charts)
        self.comments = self.fix(self.comments)
        self.create_time = self.fix(self.create_time)
        self.num_videos = self.fix(self.num_videos)
        self.maps = self.fix(self.maps)
        self.matlabs = self.fix(self.matlabs)

    def language_check(self):
        if not len(self.disc) == 0:
            self.disc = unicode(self.disc, errors='replace')
            self.language = detect(self.disc.lower())
        else:
            self.name = unicode(self.name, errors='replace')
            self.language = detect(self.name.lower())

    def to_json(self):
        self.fix_all()
        self.language_check()
        json_str = '{"name": "' + self.name + '", "url": "' + self.url + '", "author": "' + self.author + '", "disc": "' + self.disc + '", "tags": "' + self.tags + '", "shares": "' + self.shares + '", "charts": "' + self.charts + '", "comments": ' + self.comments + '", "maps": "' + self.maps + '", "matlabs": ' + self.matlabs + '", "language": "' + self.language + '"}' 
        return json_str
    
    def dump_json(self):
        f = open("json/"+self.url.encode("utf-8").split("/")[-1]+".json", "w")
        f.write(self.to_json().encode("utf-8"))

cur_channel = Channel()


def find_links_in_page(soup):
    channels = soup.find_all('a', attrs={'class':'link-no-hover'})
    links = []
    for channel in channels:
        links.append(channel.get('href'))
    return links

def find_if_needed(link):
    if link.split("/")[-1] + ".html" in filenames:
        return False
    return True

def fetch_new_channel(link):
    global cur_channel
    if find_if_needed(link):
        channel = urllib2.urlopen(base_url+link)
        html = channel.read()
        cur_channel.url = base_url+link
        channel_soup = BeautifulSoup(html, 'html.parser')
        cur_channel.html = html.decode('utf-8')
        return channel_soup
    return None

def fetch_local_channel(filename):
    global cur_channel
    f = open("./html/"+filename,"r")
    h_str = f.read()
    f.close()
    channel_soup = BeautifulSoup(h_str, 'html.parser')
    cur_channel.url = base_url+filename
    cur_channel.html = h_str.decode('utf-8')
    return channel_soup

def fetch_new_page(num):
    page = urllib2.urlopen(base_url+"channels/public?page="+str(num))
    page_soup = BeautifulSoup(page, 'html.parser')
    return page_soup

def parse_matlab(chart_soup):
    print "matlab"

def parse_maps(chart_soup):
    print "maps"

def parse_gauge(chart_soup):
    print "gauge"
    cur = Gauge()
    response = urllib2.urlopen(base_url + header)
    iframe_soup = BeautifulSoup(response)
    print iframe_soup
#        print chart_soup
    cur.header = header
    cur.title = title
    return cur.to_json()
    exit()

def parse_chart(chart_soup):
    print "chart"
    cur = Chart()
    title = chart_soup.find('div','window-title').text
    header = chart_soup.find('iframe','window-iframe').get('src')
    qs = urlparse(header)[4]
    o = parse_qs(qs)
    try:
        cur.chart_type = str(o['type'][0])
    except:
        pass
    try:
        cur.results = str(o['results'][0])
    except:
        pass
    try:
        cur.second_title = str(o['title'][0])
    except:
        pass
    try:
        cur.yaxis = str(o['yaxis'][0])
    except:
        pass
    try:
        cur.xaxis = str(o['xaxis'][0])
    except:
        pass
    cur.header = header
    cur.title = title
    return cur.to_json()

def extract_chart_data(charts_soup):
    global cur_channel
    charts = []
    json_charts = '['
    charts.append(parse_chart(chart_soup))
    for chart in charts:
        json_charts += "{ " + chart + "},"
    json_charts = json_charts[:-1] + "]"
    cur_channel.charts = json_charts 

def extract_gauge_data(gauges_soup):
    global cur_channel
    gauges = []
    json_gauges = '['
    for gauge_soup in gauges_soup:
        gauges.append(parse_gauge(gauge_soup))
    for gauge in gauges:
        json_gauges += "{ " + gauge + "},"
    json_gauges = json_gauges[:-1] + "]"
    cur_channel.gauges = json_gauges 

def extract_map_data(maps_soup):
    global cur_channel
    maps = []
    json_maps = '['
    for map_soup in maps_soup:
        maps.append(parse_map(map_soup))
    for cur_map in maps:
        json_maps += "{ " + cur_map + "},"
    json_maps = json_maps[:-1] + "]"
    cur_channel.maps = json_maps 

def extract_matlab_data(matlabs_soup):
    global cur_channel
    matlabs = []
    json_matlabs = '['
    for matlab_soup in matlabs_soup:
        matlabs.append(parse_matlab(matlab_soup))
    for matlab in matlabs:
        json_matlabs += "{ " + matlab + "},"
    json_matlabs = json_matlabs[:-1] + "]"
    cur_channel.matlabs = json_matlabs 

def make_json_str(to_convert):
    json_str = '['
    for item in to_convert:
        json_str += "{ " + matlab + "},"
    json_str = json_str[:-1] + "]"
    return json_str

def extract_visualizations(channels_soup):
    global cur_channel
    charts = []
    maps = []
    gauges = []
    matlabs = []
    charts_soup = channels_soup.find_all('div', attrs={'class':'window-container'})
    for chart_soup in charts_soup:
        header = chart_soup.find('iframe','window-iframe').get('src')
        if 'plugin' in header:
            gauges.append(parse_gauge(chart_soup, header))
        if 'youtube' in header:
            cur_channel.num_videos = cur_channel.num_videos + 1
        if 'matlab_visualizations' in header:
            matlabs.append(parse_matlab(chart_soup))
        if 'channels' in header and 'maps' in header:
            maps.append(parse_maps(chart_soup))
        if 'channels' in header and 'charts' in header:
            charts.append(parse_chart(chart_soup))
    cur_channel.matlabs = make_json_str(matlabs)
    cur_channel.charts = make_json_str(charts)
    cur_channel.gauges = make_json_str(gauges)
    cur_channel.maps = make_json_str(maps)
    print cur_channel.matlabs
    print cur_channel.gauges
    print cur_channel.maps


def extract_meta_data(channel_soup):
    global cur_channel
    name = channel_soup.find('h1', attrs={'id':'channel-name-header'}).text
    author = channel_soup.find('ul', attrs={'id':'table-channel-metadata'}).find_all('li')[1].text.split(":")[1].strip()
    disc = channel_soup.find_all('div', attrs={'class':'col-xs-6 col-sm-4'})[1].text.split('\n')[1].strip()
    try:
        shares = channel_soup.find('a', attrs={'class':'addthis_button_expanded', 'title':'More'}).text.strip()
    except:
        shares = "0"
    l_json = channel_soup.find('div', attrs={'id':'wrap'}).find_all('script', attrs={'src': None, 'type': None})[0].text.split('\n')[2:-2][0][17:]
    
    #num_videos = channel_soup.find_all('div', attrs={'id': 'player'})
    #print num_videos

    cur_channel.author = author
    cur_channel.disc = disc
    cur_channel.name = name
    cur_channel.shares = shares
    #cur_channel.num_videos = num_videos

def extract_tags(channel_soup):
    global cur_channel
    tags = []
    tag_soup = channel_soup.find_all('a', attrs={'id':'channel-tags'})
    json_tags = '['
    for tag in tag_soup:
        tags.append(tag.text)
    for tag in tags:
        json_tags += '"' + tag + '",'
    json_tags = json_tags[:-1] + "]"
    cur_channel.tags = json_tags

def parse_comment(comment_soup):
    cur = Comment()
    cur.author = comment_soup.find('span', attrs={'class':'username'}).find('a').text.strip()
    cur.creation_time = comment_soup.find('span', attrs={'class':'prettydate'}).text.strip()
    cur.text = comment_soup.find('div', attrs={'class': None, 'id': None}).text.replace("\n","").strip()
    return cur.to_json()

def extract_comments(channel_soup):
    global cur_channel
    comments = []
    comments_soup = channel_soup.find('div', attrs={'class':'commentlink'}).find_all('table', attrs={'class':'commenttable'})
    json_comments = '['
    for comment_soup in comments_soup:
        comments.append(parse_comment(comment_soup))
    for comment in comments:
        json_comments += "{ " + comment + "},"
    json_comments = json_comments[:-1] + "]"
    cur_channel.comments = json_comments
    #print json_comments

def extract_channel(channel_soup):
    extract_meta_data(channel_soup)
    extract_tags(channel_soup)
    extract_comments(channel_soup)
    extract_visualizations(channel_soup)

def run(times):
    global dump
    global remote
    if remote is True:
        for x in xrange(1, times+1):
            #sys.stderr.write("page " + str(x) + " of " + str(times+1))
            page_soup = fetch_new_page(x)
            links = find_links_in_page(page_soup)
            for link in links:
                channel_soup = fetch_new_channel(link)
                if not channel_soup is None:
                    extract_channel(channel_soup)
                    json = cur_channel.to_json()
                    dump += json + ","
                    cur_channel.dump_html()
                    cur_channel.dump_json()
                else:
                    print "skipping"
        dump = dump[:-1]
        dump = dump + "]"
#        print dump
    else:
        for x in xrange(0, times):
            channel_soup = fetch_local_channel(filenames[x])
            extract_channel(channel_soup)
            json = cur_channel.to_json()
            dump += json + ","
            cur_channel.dump_json()
            cur_channel.pretty_print()


def prefetch():
    global max_page, filenames, remote
    filenames = []
    for (dirpath, dirnames, filenames_os) in walk("./html"):
        for filename in filenames_os:
            if ".html" in filename and not len(filename) == 5 :
                filenames.append(filename)
        break

    if remote is True:
        page = urllib2.urlopen(base_url+"channels/public")
        soup = BeautifulSoup(page, 'html.parser')
        pages = soup.find_all('li')
        max_page = 0
        for page in pages:
            try:
                if int(page.text) > max_page:
                    max_page = int(page.text)
            except:
                continue

prefetch()
#run(max_page) #run with everything fetching remote
#run(len(filenames))
run(10)






