import requests
import json
import argparse
import sys
# to get the user instructions
parser = argparse.ArgumentParser(description='Pixabay image scraper with python')
parser.add_argument('-s','--search', help='Word to search in pixabay', required=True)
parser.add_argument('-p','--path', help='Path where the images should be saved (absolute or relative to this file)', required=True)
args = vars(parser.parse_args())

# to download the files
def download(links,path):
    s = 0
    en = len(links)
    for src in links:
        filename = src.split('/')[-1]
        open(path+"/"+filename, 'wb').write(requests.get(src, allow_redirects=True).content)
        s+=1
        print("downloaded {} / {} images".format(s,en), end='\r')

def req(q,p="1",key="3540998-03f8fdf91ee48e78d251af01b",typ="photo",links=[]):
    print("Downloading {} images from pixabay, all of these images are open source".format(q))
    base = "https://pixabay.com/api/" + "?key="+ key + "&q="+ q + "&image_type="+ typ
    links = []
    continu = True
    row = 0
    while(continu==True):
        lenn = len(links)
        print("{} links".format(lenn, row), end='\r')
        url = base+q+typ+"&pagi="+str(p)
        try:
            r = json.loads(requests.get(url).text)
            append = 0
            for i in r["hits"]:
                if((i["largeImageURL"] in links) == False) :
                    links.append(i["largeImageURL"])
                    append += 1
            if(append == 0):
                row += 1
                if(row == 5):
                    return links
            else:
                row = 0
            p += 1
        except Exception as e:
            try:
                if("HTTPSConnectionPool" in e):
                    continu = True
                else:
                    continu = False
            except Exception as e:
                continu = False
    return links
l = req(args["search"], 1)
print("")
download(l, args["path"])
