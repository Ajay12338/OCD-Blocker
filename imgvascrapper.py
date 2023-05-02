from bs4 import BeautifulSoup
import requests as r
import os
#  from PIL import Image -> Problem with pillow (ModuleNotFoundError: No module named 'PIL')

#To create a folder called webscraped_images :)
parent_directory = "C:/Users/bhara/Web Scraping"
dir_name = "webscraped_images"
path = os.path.join(parent_directory,dir_name)
#  print(path)
try:
    os.mkdir(path)
except:
     pass

def fetch_url_download(url:str,img_num) -> str:
        try:
            res =  r.get(url).content
            fptr = open(f"C:/Users/bhara/Web Scraping/webscraped_images/img{img_num}.jpg",'wb')
            fptr.write(res)
            fptr.close()
        except:
            #  print("<Response [404]>")
            pass
        
        
url = "https://www.google.com/search?q=cats&rlz=1C1UEAD_enIN1048IN1048&sxsrf=APwXEdd9ifjb9mkg3NRCwgJLcFAPzOYmdA:1682846246312&source=lnms&tbm=isch&sa=X&ved=2ahUKEwib5uPlotH-AhUZcGwGHSPwDk4Q_AUoAXoECAEQAw&biw=1280&bih=648&dpr=1.5"
height_of_img = 0
width_of_img = 0
dict_of_all_src_set = {}
## api:str = f'https://picsum.photos/ {height} {width}'
html:str = r.get(url).text
main_soup_obj = BeautifulSoup(html,"html.parser")

#  print(main_soup_obj.prettify())

all_imgtags = main_soup_obj.find_all('img')

for i in range(len(all_imgtags)):
    src_link = all_imgtags[i]['src']
    try:
        srcset_link = all_imgtags[i]['srcset']
    except:
        #  print("There are no srcset for this img tag")
        dict_of_all_src_set[i] = [src_link,None]
        continue
    dict_of_all_src_set[i] = [src_link,srcset_link]

print(dict_of_all_src_set)
#  download all images in the folder webscraped_images :)
imgNum = 0
for keys in dict_of_all_src_set: 
    url = dict_of_all_src_set[keys][0]  #  to get all the src links from img
    ## print(url)
    if url[0:8] == "https://":
         fetch_url_download(url,imgNum)   
    else:
        url = "	https://" + url
        fetch_url_download(url,imgNum)
    imgNum += 1



    

    

    
    






