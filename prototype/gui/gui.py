from tkinter import *
import time
import cv2
import copy
import random
import pathlib


count = 0
identitySubmitted = False

def submitIdentity():
    global identitySubmitted
    identitySubmitted = True

def waitForPassportData():
    #TODO
    # Send start
    # Wait for data
    time.sleep(1)

def waitForPassportConnection():
    #TODO
    # Send start
    # Wait for data
    time.sleep(1)

def findFace(image):
    #TODO
    # Detect face
    global count
    count = count+1
    if count==20:
        return True
    else:
        False

def compareBiometrics():
    #TODO
    result = random.randint(0, 3) 
    if (result<=1):
        return None
    else:
        return ['Mary James','29 December, 1984']

def saveData(image,name,birthdate):
    #TODO
    result = random.randint(0, 3) 
    if (result<=1):
        return None
    else:
        return [name,birthdate]

def home(imagePath):
    frmMain = Frame(gui,bg="white")
    #Configure the row/col of our frame and root window to be resizable and fill all available space
    frmMain.grid(row=0, column=0, sticky="NESW")
    frmMain.grid_rowconfigure(0, weight=1)
    frmMain.grid_columnconfigure(0, weight=1)
    
    w = Label(frmMain, background='white',justify='center',font= ('Helvetica 24 bold'),text='Identity Verification System')
    w.place(anchor = CENTER, relx = .5, rely = .2)

    # Add Image
    enrollButtonImage = PhotoImage(file = str(imagePath/"enrollButton.png"))
    verifyButtonImage = PhotoImage(file = str(imagePath/"verifyButton.png"))

    enrollButton = Button(frmMain, image = enrollButtonImage, bg='white',
                    command=lambda: enroll(imagePath), height=60, width=305, borderwidth=0 )
    enrollButton.image = enrollButtonImage
    enrollButton.place(anchor = CENTER, relx = .5, rely = .45)
 
    verifyButton =  Button(frmMain, image = verifyButtonImage, bg='white',
                    command=lambda: verify(imagePath), height=60, width=305, borderwidth=0 )
    verifyButton.image = verifyButtonImage
    verifyButton.place(anchor = CENTER, relx = .5, rely = .6)


def verify(imagePath):
    global count
    count = 0
    frmVerify = Frame(gui,bg="white")
    #Configure the row/col of our frame and root window to be resizable and fill all available space
    frmVerify.grid(row=0, column=0, sticky="NESW")
    frmVerify.grid_rowconfigure(0, weight=1)
    frmVerify.grid_columnconfigure(0, weight=1)

   # Add Image
    homeButtonImage = PhotoImage(file = str(imagePath/"homeButton.png"))
    
    homeButton = Button(frmVerify, image = homeButtonImage, bg='white',
                    command=lambda: home(imagePath), height=32, width=125, borderwidth=0 )
    homeButton.image = homeButtonImage
    homeButton.place(anchor = CENTER, relx = .075, rely = .055)


    w = Label(frmVerify, background='white',justify='center',font= ('Helvetica 15 bold'),  text='Tap wearable to scanner device.')
    w.place(anchor = CENTER, relx = .5, rely = .06)

    # create canvas
    cameraCanvas = Canvas(frmVerify, bg="light grey", height=550, width=900)
    cameraCanvas.create_line(0,0,900,550)
    cameraCanvas.create_line(0,550,900,0)
    cameraCanvas.place(anchor = CENTER, relx = .5, rely = .5)

    Tk.update(gui)

    waitForPassportData()

    startOverImage = PhotoImage(file = str(imagePath/"startOverButton.png"))
    startOverButton = Button(frmVerify, image = startOverImage, bg='white',
                    command=lambda: verify(imagePath), height=45, width=65, borderwidth=0 )
    startOverButton.image = startOverImage
    startOverButton.place(anchor = CENTER, relx = .95, rely = .05)
    w = Label(frmVerify, background='white',justify='center',font= ('Helvetica 15 bold'),  text='Look at the camera and make sure your whole face is in the frame.')
    w.place(anchor = CENTER, relx = .5, rely = .06)
    
    #CV2 camera set up
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

    #Capture logic
    captured = show_frame(cap,cameraCanvas)
    while not captured:
        captured = show_frame(cap,cameraCanvas)
    print(captured)
    cap.release()
    cv2.destroyAllWindows()
    
    frameImage = PhotoImage(file='temp.png')
    cameraCanvas.create_image(100,100,image=frameImage,anchor=CENTER)
    cameraCanvas.Image= frameImage
    Tk.update(gui)
    result = compareBiometrics()

    radius = 125
    
    if (result!=None):
        cameraCanvas.create_oval(450-radius,275-radius,450+radius,275+radius,fill='green',outline='green')
        cameraCanvas.create_line(450-55,275+45,450-85,275+20, capstyle=ROUND, fill='white', width=8)
        cameraCanvas.create_line(450-55,275+45,450+70,275-65, capstyle=ROUND, fill='white', width=8)
        w = Label(frmVerify, background='green',justify='center',font= ('Helvetica 20 bold'),  text='Verified',fg= 'white')
        w.place(anchor = CENTER, relx = .5, rely = .6)
        cameraCanvas.create_rectangle(200, 425,700,525, fill= "light grey",outline="light grey")
        identity = Label(frmVerify, background='light grey',justify='center',font= ('Helvetica 20 bold'),  text='Name: '+result[0]+'\nDate of Birth: '+result[1])
        identity.place(anchor = CENTER, relx = .5, rely = .775)

    else:
        cameraCanvas.create_oval(450-radius,275-radius,450+radius,275+radius,fill='dark red',outline='dark red')
        cameraCanvas.create_line(450-65,275-70,450+70,275+45, capstyle=ROUND, fill='white', width=8)
        cameraCanvas.create_line(450-65,275+45,450+70,275-70, capstyle=ROUND, fill='white', width=8)
        w = Label(frmVerify, background='dark red', justify='center',font= ('Helvetica 20 bold'),  text='Failed',fg= 'white')
        w.place(anchor = CENTER, relx = .5, rely = .6)


def show_frame(cap, cameraCanvas):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = copy.deepcopy(cv2image)
 
    scale_percent = 125 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite("temp.png", resized)

    frameImage = PhotoImage(file='temp.png')
    cameraCanvas.create_image(100,100,image=frameImage,anchor=CENTER)
    Tk.update(gui)
    return findFace(img)

def show_frame_background(cap, cameraCanvas):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = copy.deepcopy(cv2image)
 
    scale_percent = 125 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite("temp.png", resized)

    frameImage = PhotoImage(file='temp.png')
    cameraCanvas.create_image(100,100,image=frameImage,anchor=CENTER)
    cameraCanvas.create_rectangle(250, 250,650,375, fill= "light grey",outline="light grey")
    Tk.update(gui)
    return img


def enroll(imagePath):
    global count
    count = 0
    global identitySubmitted
    identitySubmitted = False
    frmEnroll = Frame(gui,bg="white")
    #Configure the row/col of our frame and root window to be resizable and fill all available space
    frmEnroll.grid(row=0, column=0, sticky="NESW")
    frmEnroll.grid_rowconfigure(0, weight=1)
    frmEnroll.grid_columnconfigure(0, weight=1)

   # Add Image
    homeButtonImage = PhotoImage(file = str(imagePath/"homeButton.png"))
    
    homeButton = Button(frmEnroll, image = homeButtonImage, bg='white',
                    command=lambda: home(imagePath), height=32, width=125, borderwidth=0 )
    homeButton.image = homeButtonImage
    homeButton.place(anchor = CENTER, relx = .075, rely = .055)


    w = Label(frmEnroll, background='white',justify='center',font= ('Helvetica 15 bold'),  text='Connect wearable with USB.')
    w.place(anchor = CENTER, relx = .5, rely = .06)

    # create canvas
    cameraCanvas = Canvas(frmEnroll, bg="light grey", height=550, width=900)
    cameraCanvas.create_line(0,0,900,550)
    cameraCanvas.create_line(0,550,900,0)
    cameraCanvas.place(anchor = CENTER, relx = .5, rely = .5)

    Tk.update(gui)

    waitForPassportConnection()

    startOverImage = PhotoImage(file = str(imagePath/"startOverButton.png"))
    startOverButton = Button(frmEnroll, image = startOverImage, bg='white',
                    command=lambda: enroll(imagePath), height=45, width=65, borderwidth=0 )
    startOverButton.image = startOverImage
    startOverButton.place(anchor = CENTER, relx = .95, rely = .05)
    w = Label(frmEnroll, background='white',justify='center',font= ('Helvetica 15 bold'),  text='Complete identity information below.')
    w.place(anchor = CENTER, relx = .5, rely = .06)

    
    # create the text entry box for
    # showing the expression .
    labelText=StringVar()
    labelText.set("Name")
    labelDirName=Label(frmEnroll, textvariable=labelText, height=3,background='light grey')
    labelDirName.place(anchor = CENTER, relx = .35, rely = .50)
    name = StringVar()
    name_field = Entry(frmEnroll, textvariable=name, width=40)
    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    name_field.place(anchor = CENTER, relx = .52, rely = .50)
    
    labelText=StringVar()
    labelText.set("Date of Birth")
    labelDir=Label(frmEnroll, textvariable=labelText, height=3,background='light grey')
    labelDir.place(anchor = CENTER, relx = .35, rely = .55)
    birthDate = StringVar()
    date_field = Entry(frmEnroll, textvariable=birthDate, width=40)
    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    date_field.place(anchor = CENTER, relx = .52, rely = .55)

    # Add Image
    submitButtonImage = PhotoImage(file = str(imagePath/"submitButton.png"))
    
    submitButton = Button(frmEnroll, image = submitButtonImage, bg='light grey',background='light grey', activebackground='light grey',
                    command=lambda: submitIdentity(), height=32, width=95, borderwidth=0 )
    submitButton.image = submitButtonImage
    submitButton.place(anchor = CENTER, relx = .65, rely = .6)


    #CV2 camera set up
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

    while not identitySubmitted:
        image = show_frame_background(cap,cameraCanvas)
    
    submitButton.destroy()
    date_field.destroy()
    name_field.destroy()
    labelDir.destroy()
    labelDirName.destroy()


    w = Label(frmEnroll, background='white',justify='center',font= ('Helvetica 15 bold'),  text='Look at the camera and make sure your whole face is in the frame.')
    w.place(anchor = CENTER, relx = .5, rely = .06)



    #Capture logic
    captured = show_frame(cap,cameraCanvas)
    while not captured:
        captured = show_frame(cap,cameraCanvas)
    cap.release()
    cv2.destroyAllWindows()
    
    frameImage = PhotoImage(file='temp.png')
    cameraCanvas.create_image(100,100,image=frameImage,anchor=CENTER)
    cameraCanvas.Image= frameImage
    Tk.update(gui)
    result = saveData(frameImage,name.get(),birthDate.get())

    radius = 125
    
    if (result!=None):
        cameraCanvas.create_oval(450-radius,275-radius,450+radius,275+radius,fill='green',outline='green')
        cameraCanvas.create_line(450-55,275+45,450-85,275+20, capstyle=ROUND, fill='white', width=8)
        cameraCanvas.create_line(450-55,275+45,450+70,275-65, capstyle=ROUND, fill='white', width=8)
        w = Label(frmEnroll, background='green',justify='center',font= ('Helvetica 20 bold'),  text='Success',fg= 'white')
        w.place(anchor = CENTER, relx = .5, rely = .6)
        cameraCanvas.create_rectangle(200, 425,700,525, fill= "light grey",outline="light grey")
        identity = Label(frmEnroll, background='light grey',justify='center',font= ('Helvetica 20 bold'),  text='Name: '+result[0]+'\nDate of Birth: '+result[1])
        identity.place(anchor = CENTER, relx = .5, rely = .775)

    else:
        cameraCanvas.create_oval(450-radius,275-radius,450+radius,275+radius,fill='dark red',outline='dark red')
        cameraCanvas.create_line(450-65,275-70,450+70,275+45, capstyle=ROUND, fill='white', width=8)
        cameraCanvas.create_line(450-65,275+45,450+70,275-70, capstyle=ROUND, fill='white', width=8)
        w = Label(frmEnroll, background='dark red', justify='center',font= ('Helvetica 20 bold'),  text='Failed',fg= 'white')
        w.place(anchor = CENTER, relx = .5, rely = .6)


def input():
    frmEnroll = Frame(gui,bg="white")
    #Configure the row/col of our frame and root window to be resizable and fill all available space
    frmEnroll.grid(row=0, column=0, sticky="NESW")
    frmEnroll.grid_rowconfigure(0, weight=1)
    frmEnroll.grid_columnconfigure(0, weight=1)

    # create the text entry box for
    # showing the expression .
    identity = StringVar()
    expression_field = Entry(frmEnroll, textvariable=identity)
 
    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    expression_field.grid(columnspan=4, ipadx=70)


# Driver code
if __name__ == "__main__":

    cwd = pathlib.Path.cwd()
    imagePath = cwd/ "prototype"/"gui"/"Images"
    
    # create a GUI window
    gui = Tk()
 
    # set the background colour of GUI window
    gui.configure(background="white")
 
    # set the title of GUI window and remove tkinter icon
    gui.title("Identity Verification System")
    gui.wm_attributes('-toolwindow', 'True')
    
    # set the configuration of GUI window
    gui.geometry("1000x700")
    gui.grid_rowconfigure(0, weight=1)
    gui.grid_columnconfigure(0, weight=1)
     # start the GUI
    home(imagePath)
    gui.mainloop()