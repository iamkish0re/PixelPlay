from PIL import Image 
import PIL 
  
# creating a image object (main image) 
im1 = Image.open(r"D:\Wallpaper\365604.jpg") 
  
# save a image using extension
im1 = im1.save("geeks.jpg")