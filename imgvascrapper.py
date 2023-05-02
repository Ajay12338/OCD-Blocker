from bs4 import BeautifulSoup
import requests as r
import os
import zipfile
#  from PIL import Image -> Problem with pillow (ModuleNotFoundError: No module named 'PIL')

#To create a folder called webscraped_images :)
parent_directory = "/Users/ajaysam/Desktop/OCD-Blocker/"
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
            fptr = open(f"/Users/ajaysam/Desktop/OCD-Blocker/webscraped_images/{img_num}.jpg",'wb')
            fptr.write(res)
            fptr.close()
        except:
            #  print("<Response [404]>")
            pass
        
 #This is the main url :)       
url = "https://httpstatusdogs.com/"
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
        url = "https://httpstatusdogs.com/" + url
        fetch_url_download(url,imgNum)
    imgNum += 1

#####################################################################
# Sending the folder to the server!!!!!!!!!!!!!!!!
#####################################################################
#Creating a zip file :))
folder_name = "./webscraped_images"
zip_file_name = f"{folder_name}.zip"
with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            zip_file.write(os.path.join(root, file))

# To send a  POST request to the server :))
url = ""
headers = {"Content-Type": "application/zip"}
files = {"file": open(zip_file_name, "rb")}
response = r.post(url, headers=headers, files=files)

#  200 -> Ok :)))) else not ok :((((
if response.status_code == 200:
    print("Folder uploaded successfully")
else:
    print(f"Error uploading folder: {response.text}")
    
# Delete the files bro :))))
os.remove(zip_file_name)
os.remove("/Users/ajaysam/Desktop/OCD-Blocker/webscraped_images")


    

    

    
    






