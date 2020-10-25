
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from Image_processing import *  # Using the other file i made
# from project.Image_processing import dither, grayscale


def center(title):  # Function for centering program title by adjust to frame size.
    w = int(parent.winfo_width() / 3.5)
    s = "Image process GUI".rjust(w // 2)
    parent.title(s)


def quit_instush(event):  # Function for closing program (Quit Button)
    parent.destroy()


def get_pics(event):  # Taking pictures only from selected folder
    global path_ent
    global direct
    global pics

    path_ent = path_entry.get()  # Getting folder directory
    image_list.delete(0, END)  # Clean entry
    pics = []  # Name of pictures only (without the whole path)
    pic_num = 0
    if path_ent == "":
        messagebox.showinfo("Empty path", "Please insert path before pressing \"Get photos!\"")
        browse_button.config(relief=RAISED)
    else:
        try:
            direct = os.listdir(path_ent)  # List of all paths in opening folder
            for file in direct:
                if file[-3:] == "gif" or file[-3:] == "jpg" or file[-3:] == "bmp" or file[-3:] == "png":
                    image_list.insert("end", file)  # Adding only pic files to listbox
                    pics.append(file)  # Adding only pic names to pics
                    pic_num += 1
                    browse_button.config(relief=RAISED)
            if pic_num == 0:  # If there is no pics in folder send info box
                messagebox.showinfo("Empty folder", "Please enter folder that contains pictures")
                path_entry.delete(0, END)
        except:  # If path is not valid send error box
            messagebox.showerror("Wrong Path", "Please enter valid path (Only english path!)")
            path_entry.delete(0, END)
            browse_button.config(relief=RAISED)


def browse(event):  # Browse button getting picture's folder path
    global path
    path_entry.delete(0, END)
    path = filedialog.askdirectory()
    path_entry.insert(0, path)  # Inserts path to entry
    return ()


def browse2(event):  # Browse button getting path for save entry
    global save
    save_entry.delete(0, END)
    save = filedialog.askdirectory()
    save_entry.insert(0, save)  # Inserts path to save entry


def save_pic(event):  # Save button getting save path from save entry
    save_ent = save_entry.get()
    desired_files = []  # List of all picture names with suffix
    for place in image_list.curselection():  # Taking all file places from curselection and append to list of chosen pics
        desired_files.append(pics[place])  # Pics - global variable including all pictures names from image list box
    try:
        for pic in desired_files:  # For each file from selected pictures
            open_dir = path_ent + "/" + pic
            save_dir = save_ent + "/" + pic[:-4] + "_processed" + pic[-4:]  # Taking care of suffix by slicing
            # mask_dir=''#need to finish
            if sel_pro == "Rotate":  # sel_pro is a global variable that takes user's process selection.
                rotatePicture(open_dir, save_dir)
            elif sel_pro == "Mirror":  # Sending for relevant function (by process) for saving with right saving path
                mirrorPicture(open_dir, save_dir)
            elif sel_pro == "Resize":
                resizePicture(open_dir, save_dir)
            elif sel_pro == "Edge":
                if thr == NONE:  # In case threshold is not defined
                    messagebox.showinfo("No threshold", "Please insert threshold and press Go!")
                elif 0 < thr < 255:
                    edge(open_dir, save_dir, thr)
                else:  # In case og invalid input
                    messagebox.showinfo("Wrong input", "Please insert valid threshold value (between 0 - 255)")
            elif sel_pro == "Dither":  # IMPORTANT This function is "heavy" you can save only one pic at a time
                dither(open_dir, save_dir)
            elif sel_pro == "Grayscale":
                grayscale(open_dir, save_dir)
            elif sel_pro == "Watermark":
                watermark(open_dir, save_dir)
    except:  # In case save entry is empty or wrong path in save entry
        messagebox.showerror("No saving directory", "Please make sure you have insert valid directory to save entry")
    saving_folder = os.listdir(save_ent)  # Takes all save folder files
    fsum = 0  # Counter for saved processed pictures
    for file in saving_folder:  # Verify that all pictures were saved and sending a proper message
        for pic in desired_files:
            if file == pic[:-4] + "_processed" + pic[-4:]:
                fsum += 1
    if fsum == len(desired_files):  # If all selected pictures have been save
        messagebox.showinfo("Save", "Your files saved successfully in folder:\n " + save_ent)
    else:
        messagebox.showerror("Save Error", "Saving process went wrong!\n not all files have been saved")


def pic_preview(event):
    # Previews first picture from user selection from image list box and resize it to GUI dimensions
    global frst_pic_name

    preview = Frame(image_fr, width=244, height=194, highlightthickness=0)  # Clean pic place if no file was chosen
    preview.configure(bg="lightskyblue")
    preview.place(x=300, y=65)
    if image_list.curselection() != ():  # Only if there is at least one file selection from image list box.
        chosen_pics = image_list.curselection()
        frst = chosen_pics[0]  # First chosen picture place from all pics.
        # pics = List of all picture names with suffix, frst_pic_name = first selected pic name with suffix
        frst_pic_name = pics[frst]
        pic_dirc = Image.open(path_ent + "/" + str(frst_pic_name))  #
        pic_mani = pic_dirc.copy()  # Copied picture used to preview in right size
        w, h = pic_mani.size
        n_w = 240 / float(w) * float(w)
        n_h = 180 / float(h) * float(h)
        n_dim = (int(n_w), int(n_h))
        resized_pic = pic_mani.resize(n_dim)
        img = ImageTk.PhotoImage(resized_pic)
        preview = Label(image_fr, image=img, bd=1, relief=RAISED)
        preview.image = img
        preview.place(x=300, y=68)


def go(event):  # Activate edge process on image and preview it
    global thr  # Value of demanded threshold

    if sel_pro == "Edge":  # sel_pro -> selected process
        thr = int(thresh1.get())
        if 0 < thr < 255:  # Legal value of threshold
            proced_img = edge(image_path, save_path, thr)  # Calling to function with threshold value
            processed_preview(proced_img)
        else:  # In case threshold value is invalid
            messagebox.showinfo("Wrong input", "Please insert valid threshold value (between 0 - 255)")


def processed_preview(image):
    preview_img = image.copy()  # Copied picture used to preview in right size
    w, h = preview_img.size
    n_w = 240 / float(w) * float(w)
    n_h = 180 / float(h) * float(h)
    n_dim = (int(n_w), int(n_h))
    resize_pic = preview_img.resize(n_dim)
    img = ImageTk.PhotoImage(resize_pic)
    preview = Label(image_fr, image=img, bd=1, relief=RAISED)
    preview.image = img
    preview.place(x=300, y=263)


def main_Process(event):  # Main function for activate process on picture by selection from process list
    global sel_pro  # Global parameters that needed to other functions as well
    global thresh1  # For clearing threshold
    global thresh
    global gogo
    global image_path
    global save_path
    global processed_img

    try:
        if process_list.curselection() != ():  # Just in case there is selection from process list
            selected = process_list.curselection()
            sel_pro = process_names[selected[0]]
            # image_path = folder directory + first image name, access to previewed picture
            image_path = (path_ent + "/" + str(frst_pic_name))
            save_path = ""  # Used for preview pictures with function in "image_processing" without saving them
            if sel_pro == "Rotate":
                processed_img = rotatePicture(image_path, save_path)
            elif sel_pro == "Mirror":
                processed_img = mirrorPicture(image_path, save_path)
            elif sel_pro == "Resize":
                processed_img = resizePicture(image_path, save_path)
            elif sel_pro == "Edge":  # In case of edge function, ask for threshold from user
                thresh = Label(image_fr, bg="lightskyblue", text="Insert\nthreshold:")
                thresh.place(x=225, y=390)
                thresh1 = Entry(image_fr, bg="lightcyan", width=9)
                thresh1.grid(row=6, column=1, sticky=E + S)
                gogo = Button(image_fr, text="Go!", padx=4, bg="royalblue3", fg="white",
                              font="ariel 9 bold")
                gogo.place(x=190, y=420)
                gogo.bind("<Button-1>", go)
            elif sel_pro == "Dither":
                    processed_img = dither(image_path, save_path)
            elif sel_pro == "Grayscale":
                    processed_img = grayscale(image_path, save_path)
            elif sel_pro == "Watermark":
                    processed_img=watermark(image_path, save_path)
            if sel_pro != "Edge":  # Preview for processed image (edge preview is in go function)
                processed_preview(processed_img)
    except:  # There is no image selected by user
        messagebox.showinfo("No image selected", "You have to choose pictures before pressing process")


def clear(event):  # Clear all button to clear GUI - Reset
    preview = Frame(image_fr, width=244, height=388, highlightthickness=0)  # Clean pic place if no file was chosen
    preview.configure(bg="lightskyblue")
    preview.place(x=300, y=65)
    image_list.delete(0, END)
    path_entry.delete(0, END)
    save_entry.delete(0, END)
    try:
        gogo.grid_remove()
        thresh.grid_remove()
        thresh1.grid_remove()
    except:
        print("Clear")


def parent_win():  # Main GUI function arranging all frames into the parent frame
    global intro
    global image_fr
    global pics
    global save_quit
    global path_entry
    global image_list
    global process_list
    global process_names
    global save_entry
    global get_photos
    global browse_button

    #  Parent frame deviation (divided to 3 parts) , Geometry by grid
    intro = Frame(parent)
    image_fr = Frame(parent)
    image_fr.configure(bg="lightskyblue")
    save_quit = Frame(parent)
    save_quit.configure(bg="lightskyblue")

    # Order frames in parent window
    intro.grid(row=0, columnspan=4)
    image_fr.grid(row=1, column=0)
    save_quit.grid(row=2)

    # Intro frame
    intro_lb = Label(intro, padx=220, pady=10, text="Application GUI", bg="Teal",
                     fg="royalblue3", relief=RIDGE, bd=1, font=("Aharoni 14 bold"))
    intro_lb.grid(columnspan=4)

    # Image frame
    search_label = Label(image_fr, bg="lightskyblue", font="ariel 9 bold", text="Please enter image path:")
    search_label.grid(row=0, column=0, sticky=W)
    path_entry = Entry(image_fr, bg="lightcyan")
    path_entry.grid(row=1, ipadx=80, columnspan=2)

    # (Get photos!) & (Browse...) Buttons
    get_photos = Button(image_fr, text="Get photos!", bg="royalblue3", fg="white", font="ariel 9 bold")
    get_photos.grid(row=1, column=2, padx=5)
    get_photos.bind("<Button-1>", get_pics)
    browse_button = Button(image_fr, padx=8, text="Browse...", bg="royalblue3", fg="white",
                           font="ariel 9 bold")
    browse_button.grid(row=1, column=3, padx=55)
    browse_button.bind("<Button-1>", browse)

    # Image frame -> Label + Pics listbox + Scrollbar + Choose button
    ur_img = Label(image_fr, bg="lightskyblue", font="ariel 9 bold", text="Your folder Images: ")
    ur_img.grid(row=2, column=0, sticky=W, pady=5)
    scrollbar = Scrollbar(image_fr, orient="vertical", bg="royalblue3")  # Scrollbars for listboxs.
    image_list = Listbox(image_fr, selectmode=MULTIPLE, highlightthickness=1, width=27, bg="lightcyan",
                         selectbackground="light slate blue", yscrollcommand=scrollbar.set, exportselection=0)
    image_list.grid(row=3, column=0, sticky=W)
    scrollbar.config(command=image_list.yview)
    scrollbar.grid(row=3, sticky=E, ipady=56)

    choose = Button(image_fr, padx=10, text="Choose >", bg="royalblue3", fg="lightgoldenrod1", font="ariel 9 bold")
    choose.grid(row=3, column=1, sticky=E)
    choose.bind("<Button>", pic_preview)

    # Image frame -> Label + Process listbox + Scrollbar + buttons

    process_label = Label(image_fr, bg="lightskyblue", font="ariel 9 bold", text="Process operation selection:")
    process_label.grid(row=5, column=0, sticky=W, pady=10)
    scrollbar_2 = Scrollbar(image_fr, orient="vertical")
    process_list = Listbox(image_fr, selectmode=SINGLE, highlightthickness=1, width=27, bg="lightcyan",
                           selectbackground="light slate blue", yscrollcommand=scrollbar_2.set)
    process_list.grid(row=6, column=0, sticky=W)
    process_names = ["Rotate", "Mirror", "Resize", "Edge", "Dither", "Grayscale", "Watermark"]
    for proc in process_names:
        process_list.insert("end", proc)
    scrollbar_2.config(command=image_list.yview)
    scrollbar_2.grid(row=6, sticky=E, ipady=56)

    process_list.columnconfigure(0, weight=1)
    process = Button(image_fr, padx=10, text="Process >", bg="royalblue3", fg="lightgoldenrod1",
                     font="ariel 9 bold")
    process.bind("<Button>", main_Process)
    process.grid(row=6, column=1, sticky=E)
    clear_all = Button(image_fr, padx=10, text="Clear\nAll", bg="royalblue3", fg="lightgoldenrod1", font="ariel 9 bold")
    clear_all.bind("<Button-1>", clear)
    clear_all.place(x=200, y=242)

    # save_quit frame -> Label + entry + (Browse...) & (Save) & (Quit) Buttons
    save_label = Label(save_quit, bg="lightskyblue", font="ariel 9 bold",
                       text="Please enter processed image path:")
    save_label.grid(row=0, column=0, sticky=W)
    save_entry = Entry(save_quit, bg="lightcyan")
    save_entry.grid(row=1, column=0, ipadx=80, sticky=W + E)
    browse_button_2 = Button(save_quit, padx=10, text="Browse...", bg="royalblue3", fg="white",
                             font="ariel 9 bold")
    browse_button_2.grid(row=1, column=1, padx=20)
    browse_button_2.bind("<Button-1>", browse2)
    save = Button(save_quit, text="Save", bg="royalblue3", fg="white", font="ariel 12 bold")
    save.grid(row=2, column=0, ipadx=40, pady=15)
    save.bind("<Button-1>", save_pic)
    quit = Button(save_quit, text="Quit", bg="royalblue3", fg="white", font="ariel 12 bold")
    quit.grid(row=2, column=1, ipadx=40, padx=40)
    quit.bind("<Button-1>", quit_instush)
    parent.mainloop()

# Root frame - parent.
parent = Tk()
parent.geometry("570x595")
parent.configure(bg="lightskyblue")
parent.bind("<Configure>", center)  # Called when window size changed.
parent_win()
