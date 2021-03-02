from requests_html import HTMLSession
session = HTMLSession()
query = 'kum faya kum'
url = "https://www.youtube.com/results?search_query="+ str(query)
r = session.get(url)
r.html.render(sleep=1, keep_page=True, scrolldown=1, timeout=8.0 * 10)
videos = r.html.find('#video-title')
videoList = []
for item in videos:
    video = {
        'title': item.text,
        'link': item.absolute_links
    }
    videoList.append(video)
links = ''
firstItem = videoList[0]['link']
for i in firstItem:
	links = i
print(links)