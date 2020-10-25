import cv2
import os
import os.path
from PIL import Image
# img_file: path of picture
# path_save:save path
# width：width
# height：height

def img_resize(img_file, path_save, width,height):
    img = Image.open(img_file)
    new_image = img.resize((width,height),Image.BILINEAR)
    new_image.save(os.path.join(path_save,os.path.basename(img_file)))

def read_directory(directory_name,path_save):
    for filename in os.listdir(directory_name):
        # print(filename)
        # img = cv2.imread(directory_name + "/" + filename)
        #
        # cv2.imshow(filename, img)
        # cv2.waitKey(0)
        #
        # cv2.imwrite("D://wangyang//face1" + "/" + filename, img)
        img_file=os.path.join(directory_name, filename)
        img_resize(img_file, path_save, 256, 256)

if __name__ == '__main__':
    # img_resize(r'C:\Users\william\Desktop\jinmao.jpg',r'D:\Assignment\project',256,256)
    read_directory(r'D:\Assignment\project\voc\JPEGImages', r'D:\Assignment\project\256')