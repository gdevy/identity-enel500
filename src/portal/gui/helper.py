## External Imports
import time
import random

## Internal Imports
from src.portal.scanner.serial import parse_serial_command, SerialCommand
from src.portal.scanner.scanner import init_scanner, get_template
from src.portal.biometrics.face_detection import detect_faces, validate_faces_bbox
from src.portal.biometrics.template import compare


## Verification

# Get passport data to be verified
def waitForPassportData():
    scanner_ser = init_scanner()
    command = scanner_ser.readLine()
    command, data = parse_serial_command(command, scanner_ser)

    if command == SerialCommand.INFO:
        firstName = data['fname']
        lastName = data['lname']
        dob = data['dob']

    command = scanner_ser.readLine()
    command, data = parse_serial_command(command, scanner_ser)
    if command == SerialCommand.TEMPLATE:
        template = data['template']
    
    passportData = [template,(firstName+" "+lastName),dob]
    return passportData


# Find face in image
def findFace(image):
    faces = detect_faces(image)
    faceValidation = validate_faces_bbox(faces)
    return faceValidation[0]


# Verify template distance
def compareBiometrics(passportData,probePath):
    template = passportData[0]
    name = passportData[1]
    birthdate = passportData[2]
    dist, auth = compare(template, probePath)
    print(f"Result of auth: {auth}")

    if not auth:
        return None
    else:
        return [name, birthdate]


## Enrollment 

# Wait for wearable connection to began enrollment
def waitForPassportConnection():
    # TODO
    # Send start
    # Wait for connection to enroll then return
    time.sleep(1)

# Send identity data to wearable (ENROLLMENT)
def submitIdentity():
    # TODO 
    # Send your identity information to wearable
    # Set success flag
    return True


def saveData(image, name, birthdate):
    # TODO
    #Create Template from Image
    #Combiine Template and data
    #Send Serial
    result = random.randint(0, 3)
    if result <= 1:
        return None
    else:
        return [name, birthdate]