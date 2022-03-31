from pathlib import Path
import copy
from cv2 import cv2
import tkinter
from tkinter import Frame, Button, Label, PhotoImage, Tk, Canvas, Entry, StringVar,messagebox
from . import helper
from datetime import datetime

# Path for images used in GUI
imagePath = (Path(__file__) / ".." / "Images").resolve()

# enrollment identity submission flag
identitySubmitted = False


# update flag value
def submitFlag(name, dob):
    if (name==None):
        messagebox.showerror(title="Error on Name", message="Please enter name!")
        return()
    else:
        try:
            date = datetime.strptime(dob, "%d/%m/%Y")
        except:
            messagebox.showerror(title="Error on DOB", message="Please enter correct date of birth with the following format: dd/mm/yyyy!")
            return()

    global identitySubmitted
    identitySubmitted = True


# Homescreen GUI Layout
def homescreen():
    frmMain = Frame(gui, bg="white")
    frmMain.grid(row=0, column=0, sticky="NESW")
    frmMain.grid_rowconfigure(0, weight=1)
    frmMain.grid_columnconfigure(0, weight=1)

    w = Label(frmMain, background='white', justify='center', font='Helvetica 24 bold',
              text='Identity Verification System')
    w.place(anchor=tkinter.CENTER, relx=.5, rely=.2)

    # Get Images for buttons
    enrollButtonImage = PhotoImage(file=str(imagePath / "enrollButton.png"))
    verifyButtonImage = PhotoImage(file=str(imagePath / "verifyButton.png"))

    # Set up Homescreen buttons
    enrollButton = Button(frmMain, image=enrollButtonImage, bg='white',
                          command=lambda: enroll(), height=60, width=305, borderwidth=0)
    enrollButton.image = enrollButtonImage
    enrollButton.place(anchor=tkinter.CENTER, relx=.5, rely=.45)

    verifyButton = Button(frmMain, image=verifyButtonImage, bg='white',
                          command=lambda: verify(), height=60, width=305, borderwidth=0)
    verifyButton.image = verifyButtonImage
    verifyButton.place(anchor=tkinter.CENTER, relx=.5, rely=.6)


# Verify Screens layout
def verify():
    frmVerify = Frame(gui, bg="white")
    frmVerify.grid(row=0, column=0, sticky="NESW")
    frmVerify.grid_rowconfigure(0, weight=1)
    frmVerify.grid_columnconfigure(0, weight=1)

    # Add Image
    homeButtonImage = PhotoImage(file=str(imagePath / "homeButton.png"))

    homeButton = Button(frmVerify, image=homeButtonImage, bg='white',
                        command=lambda: homescreen(), height=32, width=125, borderwidth=0)
    homeButton.image = homeButtonImage
    homeButton.place(anchor=tkinter.CENTER, relx=.075, rely=.055)

    w = Label(frmVerify, background='white', justify='center', font='Helvetica 15 bold',
              text='Tap wearable to scanner device.')
    w.place(anchor=tkinter.CENTER, relx=.5, rely=.06)

    # create canvas
    cameraCanvas = Canvas(frmVerify, bg="light grey", height=550, width=900)
    cameraCanvas.create_line(0, 0, 900, 550)
    cameraCanvas.create_line(0, 550, 900, 0)
    cameraCanvas.place(anchor=tkinter.CENTER, relx=.5, rely=.5)

    Tk.update(gui)

    # Wait for passport connection and data
    try:
        passportData = helper.waitForPassportData()
    except:
        verify()
        return()

    if passportData == None:
        messagebox.showerror(title= 'Scanner Connection Error', message='Failed to connect to scanner!')
        homescreen()
        return()

    # Get button images and setup GUI Buttons 
    startOverImage = PhotoImage(file=str(imagePath / "startOverButton.png"))
    startOverButton = Button(frmVerify, image=startOverImage, bg='white',
                             command=lambda: verify(), height=45, width=65, borderwidth=0)
    startOverButton.image = startOverImage
    startOverButton.place(anchor=tkinter.CENTER, relx=.95, rely=.05)
    w = Label(frmVerify, background='white', justify='center', font='Helvetica 15 bold',
              text='Look at the camera and make sure your whole face is in the frame.')
    w.place(anchor=tkinter.CENTER, relx=.5, rely=.06)

    # CV2 camera set up
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Capture user image logic
    captured = show_frame(cap, cameraCanvas)
    while not captured:
        captured = show_frame(cap, cameraCanvas)
    frameImage = PhotoImage(file='temp.png')
    cap.release()
    cv2.destroyAllWindows()

    # Show captured image to user
    cameraCanvas.create_image(100, 100, image=frameImage, anchor=tkinter.CENTER)
    cameraCanvas.Image = frameImage
    Tk.update(gui)

    # Compare user biometrics to passport data
    probePath = Path(".") / "temp.jpg"
    result = helper.compareBiometrics(passportData, probePath)

    # Display results
    radius = 125
    if result is not None:
        cameraCanvas.create_oval(450 - radius, 275 - radius, 450 + radius, 275 + radius, fill='green', outline='green')
        cameraCanvas.create_line(450 - 55, 275 + 45, 450 - 85, 275 + 20, capstyle=tkinter.ROUND, fill='white', width=8)
        cameraCanvas.create_line(450 - 55, 275 + 45, 450 + 70, 275 - 65, capstyle=tkinter.ROUND, fill='white', width=8)
        w = Label(frmVerify, background='green', justify='center', font='Helvetica 20 bold', text='Verified',
                  fg='white')
        w.place(anchor=tkinter.CENTER, relx=.5, rely=.6)
        cameraCanvas.create_rectangle(200, 425, 700, 525, fill="light grey", outline="light grey")
        identity = Label(frmVerify, background='light grey', justify='center', font='Helvetica 20 bold',
                         text='Name: ' + result[0] + '\nDate of Birth: ' + result[1])
        identity.place(anchor=tkinter.CENTER, relx=.5, rely=.775)

    else:
        cameraCanvas.create_oval(450 - radius, 275 - radius, 450 + radius, 275 + radius, fill='dark red',
                                 outline='dark red')
        cameraCanvas.create_line(450 - 65, 275 - 70, 450 + 70, 275 + 45, capstyle=tkinter.ROUND, fill='white', width=8)
        cameraCanvas.create_line(450 - 65, 275 + 45, 450 + 70, 275 - 70, capstyle=tkinter.ROUND, fill='white', width=8)
        w = Label(frmVerify, background='dark red', justify='center', font='Helvetica 20 bold', text='Failed',
                  fg='white')
        w.place(anchor=tkinter.CENTER, relx=.5, rely=.6)


# Enrollement Screen layout
def enroll():
    # Global flag used to display the camera in the background
    global identitySubmitted
    identitySubmitted = False

    frmEnroll = Frame(gui, bg="white")
    frmEnroll.grid(row=0, column=0, sticky="NESW")
    frmEnroll.grid_rowconfigure(0, weight=1)
    frmEnroll.grid_columnconfigure(0, weight=1)

    # Get button images and setup buttons
    homeButtonImage = PhotoImage(file=str(imagePath / "homeButton.png"))

    homeButton = Button(frmEnroll, image=homeButtonImage, bg='white',
                        command=lambda: homescreen(), height=32, width=125, borderwidth=0)
    homeButton.image = homeButtonImage
    homeButton.place(anchor=tkinter.CENTER, relx=.075, rely=.055)

    w = Label(frmEnroll, background='white', justify='center', font='Helvetica 15 bold',
              text='Connect wearable SD Card for enrollment.')
    w.place(anchor=tkinter.CENTER, relx=.5, rely=.06)

    # create canvas
    cameraCanvas = Canvas(frmEnroll, bg="light grey", height=550, width=900)
    cameraCanvas.create_line(0, 0, 900, 550)
    cameraCanvas.create_line(0, 550, 900, 0)
    cameraCanvas.place(anchor=tkinter.CENTER, relx=.5, rely=.5)

    Tk.update(gui)

    # Wait for SD Card to be ready
    helper.waitForPassportConnection()

    # Get button images and setup buttons
    startOverImage = PhotoImage(file=str(imagePath / "startOverButton.png"))
    startOverButton = Button(frmEnroll, image=startOverImage, bg='white',
                             command=lambda: enroll(), height=45, width=65, borderwidth=0)
    startOverButton.image = startOverImage
    startOverButton.place(anchor=tkinter.CENTER, relx=.95, rely=.05)
    w = Label(frmEnroll, background='white', justify='center', font='Helvetica 15 bold',
              text='Complete identity information below.')
    w.place(anchor=tkinter.CENTER, relx=.5, rely=.06)

    # create the text entry box for identity information
    labelText = StringVar()
    labelText.set("Name")
    labelDirName = Label(frmEnroll, textvariable=labelText, height=3, background='light grey')
    labelDirName.place(anchor=tkinter.CENTER, relx=.35, rely=.50)
    name = StringVar()
    name_field = Entry(frmEnroll, textvariable=name, width=40)
    name_field.place(anchor=tkinter.CENTER, relx=.52, rely=.50)

    labelText = StringVar()
    labelText.set("Date of Birth")
    labelDir = Label(frmEnroll, textvariable=labelText, height=3, background='light grey')
    labelDir.place(anchor=tkinter.CENTER, relx=.35, rely=.55)
    birthDate = StringVar()
    date_field = Entry(frmEnroll, textvariable=birthDate, width=40)
    date_field.place(anchor=tkinter.CENTER, relx=.52, rely=.55)

    # Submit button
    submitButtonImage = PhotoImage(file=str(imagePath / "submitButton.png"))

    submitButton = Button(frmEnroll, image=submitButtonImage, bg='light grey', background='light grey',
                          activebackground='light grey',
                          command=lambda: helper.submitIdentity(name.get(), birthDate.get()), height=32, width=95, borderwidth=0)
    submitButton.image = submitButtonImage
    submitButton.place(anchor=tkinter.CENTER, relx=.65, rely=.6)

    # CV2 camera set up
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Background frame while identity information is being entered
    while not identitySubmitted:
        image = show_frame_background(cap, cameraCanvas)

    submitButton.destroy()
    date_field.destroy()
    name_field.destroy()
    labelDir.destroy()
    labelDirName.destroy()

    w = Label(frmEnroll, background='white', justify='center', font='Helvetica 15 bold',
              text='Look at the camera and make sure your whole face is in the frame.')
    w.place(anchor=tkinter.CENTER, relx=.5, rely=.06)

    # Capture user image logic
    captured = show_frame(cap, cameraCanvas)
    while not captured:
        captured = show_frame(cap, cameraCanvas)
    frameImage = PhotoImage(file='temp.png')
    cap.release()
    cv2.destroyAllWindows()

    cameraCanvas.create_image(100, 100, image=frameImage, anchor=tkinter.CENTER)
    cameraCanvas.Image = frameImage
    Tk.update(gui)

    # Save data to SD Card in wearable
    result = helper.saveData(frameImage, name.get(), birthDate.get())

    # Display results
    if result is not None:
        radius = 125
        cameraCanvas.create_oval(450 - radius, 275 - radius, 450 + radius, 275 + radius, fill='green', outline='green')
        cameraCanvas.create_line(450 - 55, 275 + 45, 450 - 85, 275 + 20, capstyle=tkinter.ROUND, fill='white', width=8)
        cameraCanvas.create_line(450 - 55, 275 + 45, 450 + 70, 275 - 65, capstyle=tkinter.ROUND, fill='white', width=8)
        w = Label(frmEnroll, background='green', justify='center', font='Helvetica 20 bold', text='Success', fg='white')
        w.place(anchor=tkinter.CENTER, relx=.5, rely=.6)
        cameraCanvas.create_rectangle(200, 425, 700, 525, fill="light grey", outline="light grey")
        identity = Label(frmEnroll, background='light grey', justify='center', font='Helvetica 20 bold',
                         text='Name: ' + result[0] + '\nDate of Birth: ' + result[1])
        identity.place(anchor=tkinter.CENTER, relx=.5, rely=.775)

    else:
        radius = 125
        cameraCanvas.create_oval(450 - radius, 275 - radius, 450 + radius, 275 + radius, fill='dark red',
                                 outline='dark red')
        cameraCanvas.create_line(450 - 65, 275 - 70, 450 + 70, 275 + 45, capstyle=tkinter.ROUND, fill='white', width=8)
        cameraCanvas.create_line(450 - 65, 275 + 45, 450 + 70, 275 - 70, capstyle=tkinter.ROUND, fill='white', width=8)
        w = Label(frmEnroll, background='dark red', justify='center', font='Helvetica 20 bold', text='Failed',
                  fg='white')
        w.place(anchor=tkinter.CENTER, relx=.5, rely=.6)


# Display camera frame and return face detected flag
def show_frame(cap, cameraCanvas):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = copy.deepcopy(cv2image)

    scale_percent = 125  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("temp.png", resized)

    frameImage = PhotoImage(file='temp.png')
    cameraCanvas.create_image(100, 100, image=frameImage, anchor=tkinter.CENTER)
    Tk.update(gui)
    return helper.findFace(img)


# Display camera frame in background
def show_frame_background(cap, cameraCanvas):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = copy.deepcopy(cv2image)

    scale_percent = 125  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("temp.png", resized)

    frameImage = PhotoImage(file='temp.png')
    cameraCanvas.create_image(100, 100, image=frameImage, anchor=tkinter.CENTER)
    cameraCanvas.create_rectangle(250, 250, 650, 375, fill="light grey", outline="light grey")
    Tk.update(gui)
    return img

# Driver code
if __name__ == "__main__":
    # Create a GUI window
    gui = Tk()

    # Set the background colour of GUI window
    gui.configure(background="white")

    # Set the title of GUI window and remove tkinter icon
    gui.title("Identity Verification System")
    iconImage = PhotoImage(file=str(imagePath / "logo.png"))
    gui.iconphoto(False, iconImage)

    # Set the configuration of GUI window
    gui.geometry("1000x700")
    gui.grid_rowconfigure(0, weight=1)
    gui.grid_columnconfigure(0, weight=1)

    # Start the GUI on the homescreen
    homescreen()
    gui.mainloop()