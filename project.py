import tkinter as tk
from tkinter import Label, Toplevel, messagebox
import requests
from bs4 import BeautifulSoup
import csv
from PIL import Image, ImageTk

# function to send request to server
def sendRequest(url, userName):
    r = requests.get(url)
    code = r.status_code

    if code == 200:
        return r.text
    else:
        messagebox.showerror("Error", f"Failed to connect with Instagram profile {userName}")

def finish():
    exit()

# function to get image url  
def get_profile_image_url(url):
    # request to server 
    response = requests.get(url)
    # Check the request
    if response.status_code == 200: 
        soup = BeautifulSoup(response.text, 'html.parser')

        # finding the meta tag
        meta_tag = soup.find('meta', property='og:image')

        # obtaining the image url from meta tag
        if meta_tag:
            return meta_tag['content']
    return None

# function to download profile image in jpg file
def download_profile_image(userName,url):
    # getting the profile image url
    image_url = get_profile_image_url(url)
    file_path=f"{userName}.jpg"
    
    if image_url:
        # Send a GET request to the image URL
        image_response = requests.get(image_url)

        # Check if the request was successful
        if image_response.status_code == 200:
            # Save the image to the specified file path
            with open(file_path, 'wb') as f:
                f.write(image_response.content)
            messagebox.showinfo("Success", f"Profile image downloaded successfully as {file_path}.")
            return True
    print("Failed to download profile image.")

# fuction for scrapping meta tag 
def scrapping(text):
    soup = BeautifulSoup(text, "html.parser")
    meta_content = soup.find('meta', {'name': 'description'})['content']
    return meta_content

# function to display the details of profile 
def display_info(meta_content, userName):
    file_path=f"{userName}.jpg"
    meta_content_list = list(meta_content.split(" "))
    followers = meta_content_list[0]
    followings = meta_content_list[2]
    posts = meta_content_list[4]
    global my_img
    top = Toplevel()
    top.geometry("450x250")
    top.title("Profile Details")
    my_img = ImageTk.PhotoImage(Image.open(file_path))
    Label(top, image=my_img).pack()
    Label(top, text=f"The Instagram information of profile ({userName}) are as follows:\n\nFollowers: {followers}\nFollowings: {followings}\nPosts: {posts}").pack()
    # writing data in csv file of profile
    my_file=open("profileloader.csv",'a')

    profile_writer=csv.writer(my_file,delimiter="\t")

    profile_writer.writerow([userName,followers,followings,posts])

    my_file.close()

def load_profile():
    user_name = entry.get()
    url = f"https://www.instagram.com/{user_name}/"
    html_code = sendRequest(url, user_name)
    if html_code:
        meta_content = scrapping(html_code)
        download_profile_image(user_name,url)
        display_info(meta_content, user_name)

# fuction to implement gui properties
def create_gui_properties():
    root = tk.Tk()
    root.title("Instagram Profile Loader")

    root.geometry("410x200+500+300")
    root.minsize(200,200)

    label1= tk.Label(text="Welcome to Instagram Profile Loader..!",font="comicsansms 16 bold")
    label1.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

    label = tk.Label(root, text="Enter the username:")
    label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    global entry
    entry = tk.Entry(root)
    entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    load_button = tk.Button(root, text="Load Profile", command=load_profile,fg="white",bg="grey")
    load_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    exit_button=tk.Button(root,text="Exit",command=finish,fg="white",bg="grey")
    exit_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    root.mainloop()

#__main__

create_gui_properties()
