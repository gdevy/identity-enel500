## External Imports
import time
import random
import subprocess
import sys
from pathlib import Path

## Internal Imports
from src.portal.scanner import scanner
from src.portal.biometrics.face_detection import detect_faces, validate_faces_bbox
from src.portal.biometrics.template import compare, create_template, pipeline


## Verification
scanner_ser = None
baud_rate = 38400

def initialiseCommunication():
    global scanner_ser,baud_rate
    scanner_ser = scanner.init_scanner(port_name = 'COM3',baud_rate = baud_rate)

# Get passport data to be verified
def waitForPassportData():
    try:
        global scanner_ser
        if scanner_ser == None:
            scanner_ser = scanner.init_scanner(port_name = 'COM3')
    except Exception as e:
        print(e)
        return None
    command, data = scanner.next_input(scanner_ser)
    assert (command == scanner.SerialCommand.INFO)
    fname, lname, dob = data['fname'], data['lname'], data['dob']
    print("First name: "+ fname)
    command, data = scanner.next_input(scanner_ser)
    assert (command == scanner.SerialCommand.TEMPLATE)
    template = data['template']

    passport_data = [template, (fname + " " + lname), dob]

    return passport_data


# Find face in image
def findFace(imagePath):
    return pipeline(imagePath)


# Verify template distance
def compareBiometrics(passportData, probePath):
    template = passportData[0]
    name = passportData[1]
    birthdate = passportData[2]
    dist, auth = compare(template, probePath)
    print(f"Result of auth: {auth}")
    
    global scanner_ser
    scanner.send_result(scanner_ser, auth)
    
    if not auth:
        return None
    else:
        return [name, birthdate]


## Enrollment 
drivePath = None
# Wait for wearable connection to began enrollment
def waitForPassportConnection():
    timeout = 20
    timeout_start = time.time()
    global drivePath
    while (drivePath == None) and (time.time() < timeout_start + timeout):
        if 'win' in sys.platform:
            drivelist = subprocess.Popen('wmic logicaldisk get name,description', shell=True, stdout=subprocess.PIPE)
            drivelisto, err = drivelist.communicate()
            driveLines = drivelisto.decode().split('\r\r\n')
            for drive in driveLines:
                if 'Removable Disk' in drive:
                    drivePath = drive.split()[2]
        elif 'linux' in sys.platform or 'macosx' in sys.platform :
            # TODO: Test on mac + get removable drive
            listdrives=subprocess.Popen('mount', shell=True, stdout=subprocess.PIPE)
            listdrivesout, err=listdrives.communicate()
            for idx,drive in enumerate(filter(None,listdrivesout)):
                listdrivesout[idx]=drive.split()[2]
            print(listdrivesout)
        else:
            raise Exception('Unknown OS platform')

    if drivePath == None:
        raise Exception('Could not find SD Card')



def saveData(image, name, birthdate):
    template = pipeline(image)
    if len(template)>0:
        template = str(template).replace("[","").replace("]","").replace("\n","").strip().replace("  "," ")
        try:
            global drivePath
            filepath = (Path(drivePath) / "TEMPLATE.txt").resolve()
            drivePath = None
            with open(filepath, 'w') as f:
                splitName = name.split()
                f.write(splitName[0]+"\n")
                f.write(splitName[1]+"\n")
                f.write(birthdate+"\n")
                f.write(str(template))
        except FileNotFoundError:
            print("Failed to write to file")
            return None
        return [name, birthdate]
    else:
        print("Failed to create template!")
        return None