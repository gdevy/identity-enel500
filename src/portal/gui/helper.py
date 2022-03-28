## External Imports
import time
import random

## Internal Imports
from src.portal.scanner import scanner
from src.portal.biometrics.face_detection import detect_faces, validate_faces_bbox
from src.portal.biometrics.template import compare


## Verification

# Get passport data to be verified
def waitForPassportData():
    scanner_ser = scanner.init_scanner()

    command, data = scanner.next_input(scanner_ser)
    assert (command == scanner.SerialCommand.INFO)
    fname, lname, dob = data['fname'], data['lname'], data['dob']

    command, data = scanner.next_input(scanner_ser)
    assert (command == scanner.SerialCommand.TEMPLATE)
    template = data['template']
    passport_data = [template, (fname + " " + lname), dob]

    return passport_data


# Find face in image
def findFace(image):
    faces = detect_faces(image)
    faceValidation = validate_faces_bbox(faces)
    return faceValidation[0]


# Verify template distance
def compareBiometrics(passportData, probePath):
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

def saveData(image, name, birthdate):
    # TODO
    # Create Template from Image
    # Combiine Template and data
    # Send Serial
    result = random.randint(0, 3)
    if result <= 1:
        return None
    else:
        return [name, birthdate]