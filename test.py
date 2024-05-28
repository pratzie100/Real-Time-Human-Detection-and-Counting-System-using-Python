# Real Time Human Detection & Counting
# code for front-end(GUI using Tkinter)
#--------------------------------------------------------------------------------------------------
# imported necessary libraries
from tkinter import * #import tkinter library in program
import tkinter as tk #tk is acronym
import tkinter.messagebox as mbox 
from tkinter import filedialog #HELPS IN CREATING FILE SELECTION WINDOWS
from PIL import ImageTk, Image #importing ImageTk module from PIL library
import cv2
from persondetection import DetectorAPI
#------------------------------------------------------------------------------------------------------

# Main Window & Configuration
window = tk.Tk()   #Creating instance of window(tkinter frame), basically creating window object or window widget #Tk() creates root window,using some inbuilt function of tkinter library
window.title("Real Time Human Detection & Counting")
window.iconbitmap('Images/icon.ico') #sets icon of window
window.geometry('1000x700')
window.configure(bg='pale turquoise')

# top label #heading of main window
start1 = tk.Label(text = "REAL-TIME-HUMAN\nDETECTION  &  COUNTING",font=("Arial",50,"underline"), bg="pale turquoise",fg="Navy")
start1.place(x = 70, y = 10)

# image on the main window
path = "Images/FRONT_IMG.png"
img1 = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image = img1)
panel.place(x = 175, y = 180)

# function defined to start the main application #to execute start button function
def start_fun():
    window.destroy()

# created a start button
Button(window,text="  START  ",command=start_fun,font=("Arial",25),bg="orange",fg="navy",cursor="hand2",borderwidth=6,relief="raised").place(x=170,y=570)

exit1 = False
# function created for exiting from window
def exit_win():
    global exit1
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        exit1 = True
        window.destroy()

# exit button created
Button(window,text="   EXIT   ",command=exit_win,font=("Arial",25),bg="red",fg="navy",cursor="hand2",borderwidth=6,relief="raised").place(x=660,y=570)

window.protocol("WM_DELETE_WINDOW", exit_win) #PROTOCOL HANDLER,defines interaction btw window manager and program,what happens when user try to explicitly close window using WM
window.mainloop() #lets tkinter to keep executing window until user exits window or goes to any other event from window



# ---------------------------- image section ----------------------------------------------------------------------------------------------------------------
def image_option():
    # new windowi created for image section
    windowi = tk.Tk()
    windowi.title("Human Detection from Image")
    windowi.iconbitmap('Images/icon.ico')
    windowi.geometry('1000x700')
    windowi.configure(bg='lavender')

    filename1=""

    # function defined to open the image #SELECT BUTTON FUNCTION
    def select_img():
        global filename1
        filename1 = filedialog.askopenfilename(title="Select Image file", parent = windowi)      #FILEDIALOG HELPS IN CREATING FILE SELECTION WINDOWS

        path_text1.delete("1.0", "end") #clear input text in text widget #clear filename
        path_text1.insert(END, filename1) #input filename in text widget

    # function defined to detect the image
    def det_img():
        global filename1

        image_path = filename1
        if(image_path==""):
            mbox.showerror("Error", "No Image File Selected!", parent = windowi)
            return
        info1.config(text="Status : Detecting...")

        mbox.showinfo("Status", "Detecting, Please Wait...", parent = windowi)
     
        detectByPathImage(image_path)

    # main detection process process here
    def detectByPathImage(path):
        obapi = DetectorAPI() #created object of DetectorAPI class
        threshold = 0.7
        image = cv2.imread(path)  #loads image from specified file(path)
        img = cv2.resize(image, (image.shape[1], image.shape[0])) #reduce no. of pixels #image.shape returns tuple of no. of rows and columns
        boxes, scores, classes, num = obapi.processFrame(img)
        person = 0
        for i in range(len(boxes)):
            if scores[i] > threshold: #condition for object to be a human
                box = boxes[i]
                person += 1
                accuracy=round(scores[i]*100,1)
                cv2.putText(img,'STATUS:',(10, 20),cv2.FONT_HERSHEY_COMPLEX, 0.5, (200,100,100), 1)
                cv2.putText(img,'DETECTION & COUNTING COMPLETED',(85,20),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255,0,0), 2)  # cv2.FILLED #BGR
                cv2.putText(img, f'P{person,accuracy}', (box[1] - 30, box[0] - 8), cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 255), 1)  # (75,0,130),

        cv2.putText(img,'TOTAL PERSON DETECTED:',(10, 40),cv2.FONT_HERSHEY_COMPLEX, 0.5, (200,100,100), 1)
        if(person<=0):
            cv2.putText(img,str(person),(240,40),cv2.FONT_HERSHEY_COMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        else:
            cv2.putText(img,str(person),(240,40),cv2.FONT_HERSHEY_COMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.imshow("Human Detection from Image", img)
        info1.config(text="Status : Detection & Counting Completed")
        cv2.waitKey(0) # waiting till any key is pressed
        cv2.destroyAllWindows()

    # Content of image window # ----------------------
    lbl1 = tk.Label(windowi,text="DETECT  FROM\nIMAGE", font=("Forte", 50, "underline"),bg="lavender",fg="brown")
    lbl1.place(x=230, y=20)
    lbl2 = tk.Label(windowi,text="Selected Image", font=("Arial", 30),bg="lavender",fg="green")
    lbl2.place(x=80, y=240)

    #making text widget
    path_text1 = tk.Text(windowi, height=1, width=37, font=("Arial", 30), bg="light yellow", fg="orange",borderwidth=5, relief="sunken") #text widget
    path_text1.place(x=80, y = 290)

    Button(windowi, text="SELECT", command=select_img, cursor="hand2", font=("Arial", 20), bg="light green", fg="blue").place(x=600, y=230)
    
    Button(windowi, text="DETECT",command=det_img, cursor="hand2", font=("Arial", 20), bg = "orange", fg = "blue").place(x = 760, y = 230)

    info1 = tk.Label(windowi,font=( "Arial", 30),fg="gray",bg="lavender") #info widget or status widget
    info1.place(x=100, y=445)
    # info2 = tk.Label(windowi,font=("Arial", 30), fg="gray")
    # info2.place(x=100, y=500)

    def exit_wini():
        if mbox.askokcancel("Exit", "Do you want to exit?", parent = windowi):
            windowi.destroy()
    windowi.protocol("WM_DELETE_WINDOW", exit_wini)


# ---------------------------- video section ---------------------------------------------------------------------------------------------------------
def video_option():
    # new windowv created for video section
    windowv = tk.Tk()
    windowv.title("Human Detection from Video")
    windowv.iconbitmap('Images/icon.ico')
    windowv.geometry('1000x700')
    windowv.configure(bg='lightcyan1')


    filename2=""

    # function defined to open the video
    def open_vid():
        global filename2
        filename2 = filedialog.askopenfilename(title="Select Video file", parent=windowv)
        path_text2.delete("1.0", "end")
        path_text2.insert(END, filename2)

    # function defined to detect inside the video
    def det_vid():
        global filename2

        video_path = filename2
        if (video_path == ""):
            mbox.showerror("Error", "No Video File Selected!", parent = windowv)
            return
        info1.config(text="Status : Detecting...")
        mbox.showinfo("Status", "Detecting, Please Wait...", parent=windowv)
        detectByPathVideo(video_path)

    # the main process of detection in video takes place here
    def detectByPathVideo(path):
        # function defined to plot the people detected in video
        video = cv2.VideoCapture(path)
        obapi = DetectorAPI()
        threshold = 0.7

        check, frame = video.read()
        if check == False:
            print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
            return

        while video.isOpened(): 
            # check is True if reading was successful
            check, frame = video.read() #check if frame is read correctly
            if(check==True):
                img = cv2.resize(frame, (800, 500))
                boxes, scores, classes, num = obapi.processFrame(img)
                person = 0
                for i in range(len(boxes)):
                    if scores[i] > threshold:
                        box = boxes[i]
                        person += 1
                        accuracy=round(scores[i]*100,1)
                        cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)  # cv2.FILLED
                        cv2.putText(img, f'P{person,accuracy}', (box[1]-30, box[0]-8), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1 )#(75,0,130),
                        
                if(person<=0):
                    cv2.putText(img,'STATUS:',(10, 450),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    cv2.putText(img,'WAITING',(85,450),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
                    cv2.putText(img,'REAL-TIME PEOPLE COUNTER:',(10, 470),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    cv2.putText(img,str(person),(265,470),cv2.FONT_HERSHEY_COMPLEX, 0.5,(0,0,0),1,cv2.LINE_AA)
                else: 
                    cv2.putText(img,'STATUS:',(10, 450),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    cv2.putText(img,'DETECTING',(85,450),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
                    cv2.putText(img,'REAL-TIME PEOPLE COUNTER:',(10, 470),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    cv2.putText(img,str(person),(265,470),cv2.FONT_HERSHEY_COMPLEX, 0.5,(0,0,0),1,cv2.LINE_AA)

                cv2.imshow("Human Detection from Video", img)
                key = cv2.waitKey(1)#wait for 1ms and return code of key q 
                if key & 0xFF == ord('q'):
                    break
            else:
                break

        video.release()
        info1.config(text="Status : Detection & Counting Completed")
        cv2.destroyAllWindows()

    lbl1 = tk.Label(windowv, text="DETECT  FROM\nVIDEO", font=("Forte", 50, "underline"),bg="lightcyan1", fg="brown")
    lbl1.place(x=230, y=20)
    lbl2 = tk.Label(windowv, text="Selected Video", font=("Arial", 30), bg="lightcyan1",fg="green")
    lbl2.place(x=80, y=200)
    path_text2 = tk.Text(windowv, height=1, width=37, font=("Arial", 30), bg="light yellow", fg="orange", borderwidth=2,relief="solid")
    path_text2.place(x=80, y=260)

    Button(windowv, text="SELECT", command=open_vid, cursor="hand2", font=("Arial", 20), bg="light green", fg="blue").place(x=220, y=350)
    
    Button(windowv, text="DETECT", command=det_vid, cursor="hand2", font=("Arial", 20), bg="orange", fg="blue").place(x=620, y=350)

    info1 = tk.Label(windowv, font=("Arial", 30), fg="gray",bg="lightcyan1")  
    info1.place(x=100, y=440)

    #function defined to exit from windowv section
    def exit_winv():
        if mbox.askokcancel("Exit", "Do you want to exit?", parent = windowv):
            windowv.destroy()
    windowv.protocol("WM_DELETE_WINDOW", exit_winv)


# ---------------------------- camera section -------------------------------------------------------------------------------------
def camera_option():
    # new window created for camera section
    windowc = tk.Tk()
    windowc.title("Human Detection from Camera")
    windowc.iconbitmap('Images/icon.ico')
    windowc.geometry('1000x700')
    windowc.configure(bg='light yellow')

    # function defined to open the camera
    def open_cam():

        info1.config(text="Status : Opening Camera...")
        mbox.showinfo("Status", "Opening Camera...Please Wait...", parent=windowc)
            
        if True:
            detectByCamera()

    # function defined to detect from camera
    def detectByCamera():
        
        video = cv2.VideoCapture(0)
        odapi = DetectorAPI()
        threshold = 0.7

        while True:
            check, frame = video.read()
            img = cv2.resize(frame, (800, 600))
            boxes, scores, classes, num = odapi.processFrame(img)
            person = 0
            for i in range(len(boxes)):
                if scores[i] > threshold:
                    box = boxes[i]
                    person += 1
                    accuracy=round(scores[i]*100,1)
                    cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (0,255,0), 4)  # cv2.FILLED
                    cv2.putText(img, f'P{person,accuracy}', (box[1] - 30, box[0] - 8),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255 ), 1)  # (75,0,130),
    
            if(person<=0):
                cv2.putText(img,'STATUS:',(10, 20),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
                cv2.putText(img,'WAITING',(85,20),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
                cv2.putText(img,'REAL-TIME PEOPLE COUNTER:',(10, 40),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
                cv2.putText(img,str(person),(265,40),cv2.FONT_HERSHEY_COMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            else:    
                cv2.putText(img,'STATUS:',(10, 20),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
                cv2.putText(img,'DETECTING',(85,20),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
                cv2.putText(img,'REAL-TIME PEOPLE COUNTER:',(10, 40),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
                cv2.putText(img,str(person),(265,40),cv2.FONT_HERSHEY_COMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)

            cv2.imshow("Human Detection from Camera", img)
            key = cv2.waitKey(1) 
            if key & 0xFF == ord('q'):
                break

        video.release()

        info1.config(text="Status : Detection & Counting Completed")
        cv2.destroyAllWindows()

    lbl1 = tk.Label(windowc, text="DETECT  FROM\nCAMERA", font=("Forte", 50, "underline"),bg="light yellow", fg="brown")  
    lbl1.place(x=230, y=20)

    Button(windowc, text="OPEN CAMERA", command=open_cam, cursor="hand2", font=("Arial", 20), bg="light green", fg="blue").place(x=370, y=230)

    info1 = tk.Label(windowc, font=("Arial", 30), fg="gray",bg="light yellow")  
    info1.place(x=100, y=330)

    # function defined to exit from the camera window
    def exit_winc():
        if mbox.askokcancel("Exit", "Do you want to exit?", parent = windowc):
            windowc.destroy()
    windowc.protocol("WM_DELETE_WINDOW", exit_winc)
#----------------------------------------------------------------------------------------------------------------------------------------------------
if exit1==False: #simply means user didnt exited the application, pressed start button
    # OPTIONS WINDOW
    window1 = tk.Tk()
    window1.title("Real Time Human Detection & Counting")
    window1.iconbitmap('Images/icon.ico')
    window1.geometry('1000x700')
    window1.configure(bg='pink')
    # OPTIONS WINDOW CONTENT
    #HEADING OF OPTION WINDOW
    lbl1 = tk.Label(text="OPTIONS", font=("Cooper Black", 40),bg='pink',fg="maroon")
    lbl1.place(x=340, y=20)

    # 1st image on the OPTIONS window
    pathi = "Images/OW_image.jpg"
    imgi = ImageTk.PhotoImage(Image.open(pathi))
    paneli = tk.Label(window1, image = imgi)
    paneli.place(x = 90, y = 110)

    # 2nd image on the OPTIONS window
    pathv = "Images/OW_video.jpg"
    imgv = ImageTk.PhotoImage(Image.open(pathv))
    panelv = tk.Label(window1, image = imgv)
    panelv.place(x = 660, y = 230)# 720, 260

    # 3rd image on the OPTIONS window
    pathc = "Images/OW_camera.jpg"
    imgc = ImageTk.PhotoImage(Image.open(pathc))
    panelc = tk.Label(window1, image = imgc)
    panelc.place(x = 90, y = 395)

    # created button for all three option
    Button(window1,text="DETECT  FROM  IMAGE",command=image_option,cursor="hand2",font=("Arial",30),bg="light green",borderwidth=8,fg="Navy").place(x=450,y=130)
    Button(window1,text="DETECT  FROM  VIDEO",command=video_option,cursor="hand2",font=("Arial",30),bg="light blue",borderwidth=8,fg="navy").place(x=110,y=300) #90, 300
    Button(window1,text="DETECT  FROM  CAMERA",command=camera_option,cursor="hand2",font=("Arial",30),bg="light green",borderwidth=8,fg="navy").place(x=350,y=470)

    # function defined to exit from window1
    def exit_win1():
        if mbox.askokcancel("Exit", "Do you want to exit?"):
            window1.destroy()

    # created exit button
    Button(window1, text="   EXIT   ",command=exit_win1,  cursor="hand2", font=("Arial", 25), bg = "red", fg = "AZURE").place(x = 440, y = 600)

    window1.protocol("WM_DELETE_WINDOW", exit_win1)
    window1.mainloop()


