import cv2
import numpy as np
import os

drawing = False # 鼠标左键按下时，该值为True，标记正在绘画
mode = False # True 画矩形，False 画圆
ix, iy = -1, -1 # 鼠标左键按下时的坐标


def draw(path):
    # img = np.zeros((512, 512, 3), np.uint8)
    # img = cv2.imread('0.png', cv2.IMREAD_COLOR)
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img2 = np.zeros(img.shape, np.uint8)
    size = 5
    def draw_circle(event, x, y, flags, param):
        global ix, iy, drawing, mode

        if event == cv2.EVENT_LBUTTONDOWN:
            # 鼠标左键按下事件
            drawing = True
            ix, iy = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            # 鼠标移动事件
            if drawing == True:
                if mode == True:
                    cv2.rectangle(img, (ix, iy), (x, y), (255, 255, 255), -1)
                    cv2.rectangle(img2, (ix, iy), (x, y), (255, 255, 255), -1)
                else:
                    cv2.circle(img, (x, y), size, (255, 255, 255), -1)
                    cv2.circle(img2, (x, y), size, (255, 255, 255), -1)

        elif event == cv2.EVENT_LBUTTONUP:
            # 鼠标左键松开事件
            drawing = False
            if mode == True:
                cv2.rectangle(img, (ix, iy), (x, y), (255, 255, 255), -1)
                cv2.rectangle(img2, (ix, iy), (x, y), (255, 255, 255), -1)
            else:
                cv2.circle(img, (x, y), size, (255, 255, 255), -1)
                cv2.circle(img2, (x, y), size, (255, 255, 255), -1)
    cv2.namedWindow('image',0)
    cv2.resizeWindow('image', 600, 600)
    cv2.setMouseCallback('image', draw_circle)  # 设置鼠标事件的回调函数
    cv2.imshow('image', img)

    while (1):
        cv2.namedWindow('image', 0)
        cv2.resizeWindow('image', 600, 600)
        cv2.setMouseCallback('image', draw_circle)  # 设置鼠标事件的回调函数
        cv2.imshow('image', img)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('m'):
            mode = not mode
        elif k==ord('a'):
            size-=1 #shrink cursor
        elif k==ord('s'):
            size+=1 #enlarge cursor
        elif k == 27:
            break
    # cv2.imwrite('2.png', img)
    cv2.imwrite('mask.png', img2)
    mask_path=os.getcwd()+'\mask.png'
    cv2.destroyAllWindows()
    return mask_path