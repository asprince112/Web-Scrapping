import requests
import sys
from bs4 import BeautifulSoup
import pprint



x = input('Please give a number of the page you wanna view: ')
data = 'https://www.thephotoforum.com/forums/landscape-cityscape.49/page-'
res = requests.get(data + str(x))
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.PreviewTooltip')
dislistitem = soup.select('.discussionListItem')

def sort_by_views(dict):
    return sorted(dict, key= lambda k:k['views'], reverse=True)


def get_every_title_and_url():
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = 'https://www.thephotoforum.com/' + links[idx].get('href', None)
        views = dislistitem[idx].select('.minor > dd')
        num = int(views[0].getText())
        if num > 200:
            hn.append({'title': title, 'views': num, 'link': href})
    return sort_by_views(hn)



def data():
    dicts = get_every_title_and_url()
    
    link_list = []
    for i in dicts:
        link_list.append(i['link'])
    
    photo_list = []
    for page in link_list:
        tem_list = []
        res = requests.get(page)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.find_all('blockquote', class_='messageText SelectQuoteContainer ugc baseHtml')
        for idx, item in enumerate(links):
            photos = item.select('img')
            for i in photos:
                dd = i.get('src')
                if '.png' not in dd and '.gif' not in dd:
                    if dd[0:4] != 'http':
                        dd = 'https://www.thephotoforum.com/' + dd
                        tem_list.append(dd)
                    else:
                        tem_list.append(dd)    
        photo_list.append(tem_list)
    
    
    l1 = dicts
    l2 = photo_list
    for i in enumerate(l1):
        for j in enumerate(l2):
            if i[0] == j[0]:
                i[1]['link'] = j[1]
    
    return l1


    
def final_result():
    str1 = ''
    for i in data():
        str1 += '<h2>' + i['title'] + '</h2><br>'
        for y in i['link']:
            str1 += '<img src="' + y + '"<br>' + ' '

    return str1
    


html_str1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<style>
img {
    width: 400px;
    height: 400px;
    object-fit: cover;
}
</style>
<body> """ 

html_str2 = """   
</body>
</html>

"""
            
html_str = html_str1 + final_result() + html_str2

Html_file= open("List.html","w")
Html_file.write(html_str)
Html_file.close()
