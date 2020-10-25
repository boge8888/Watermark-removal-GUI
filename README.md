# Generative Image Inpainting for Watermark Removal + GUI

This is a fork of https://github.com/JiahuiYu/generative_inpainting (the official code release of inpainting with contextual attention https://arxiv.org/abs/1801.07892) which attempts to implement the features described in their subsequent paper introducing Gated Convolutions (https://arxiv.org/pdf/1806.03589.pdf) and some other experimental features such as multiresolution contextual attention.

We implemented a GUI to select the watermark region of a picture before processing.

generative inpainting
#1. make sure you have installed requested module

>tensorflow 1.x  
>pillow  
>opencv  
>tkinter  
>neuralgym (run pip install git+https://github.com/JiahuiYu/neuralgym)

2. run GUI.py

>Choose picture  
>Circle the position of water mark  
>Input picture and mask  
>Start processing  
>Output processed picture  

3. check the processed picture in your saving path  
Choose the photo you want to remove watermark->Circle the position of watermark->Get the result after generating

<img src="https://github.com/boge8888/Watermark-removal-GUI/blob/master/examples/places2/gui1.png" width="33%"/> <img src="https://github.com/boge8888/Watermark-removal-GUI/blob/master/examples/places2/gui2.png" width="33%"/> <img src="https://github.com/boge8888/Watermark-removal-GUI/blob/master/examples/places2/gui3.png" width="33%"/>

Sample results  
original picture->our trained model->pretrained model
