import face_recognition
import cv2
import numpy as np
import time
import winsound as sound
import database as db
#import faceRe as fr
import mysql.connector as sql



conn = sql.connect(host="localhost",user='root',passwd='dh33raj1')
cur = conn.cursor()
cur.execute('use known_persons;')
cur.execute("""CREATE TABLE IF NOT EXISTS Person(unqID varchar(50) PRIMARY KEY);""")
def entry(obj):
    for i in obj:

        query = "insert into Person values("+i+");"
        cur.execute(query)
        conn.commit()


def unknown_entry(length):

    newId=(str(length),)
    print(str(newId))
    query="INSERT INTO person (unqID) VALUES (%s)"
    cur.execute(query,newId)
    conn.commit()
    return 1


def retrieve():
    query="select * from Person;"
    cur.execute(query)
    li=cur.fetchall()
    lst=[]
    lst.clear()
    str(li)
    for i in li:
        lst.append(str(i[0]))
    print(lst)
    return lst


video_capture = cv2.VideoCapture(0)


known_images = list(retrieve())
print(known_images)
loadImages = []

loadImages_encode = []
loadImages_encode.clear()
for knImage in known_images:
    # Load a sample picture and learn how to recognize it.
    known_images1 = knImage
    x = (face_recognition.load_image_file("C:\\Users\\DHEERAJ SKYLARK\\PycharmProjects\\Dynamic_faceRecognition\\known_images\\" + known_images1 + ".jpg"))
    print((face_recognition.face_encodings(x)[0]))
    loadImages_encode.append(face_recognition.face_encodings(x)[0])

# Load a second sample picture and learn how to recognize it.
#biden_image = face_recognition.load_image_file("C:\\Users\\DHEERAJ SKYLARK\\PycharmProjects\\Dynamic_faceRecognition\\known_images\\biden.jpg")
#biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
known_face_encodings = []
known_face_encodings.clear()
# Create arrays of known face encodings and their names
for knEncode in loadImages_encode:
    known_face_encodings.append(knEncode)
known_face_names = []
known_face_names = known_images.copy()

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        if (name in known_images):
            #time.sleep(3.5)
            print("KNOWN PERSON")
        if (name=="Unknown"):
            sound.Beep(3000,5000)
            decision=input("Allow : [Y]/[N]")
            if(decision in ["Y","y","Yes","yes","YES"]):
                decision1=int(input("Allow : 1.Once or 2.Everytime"))
                if(decision1==1):
                    print("ALLOWED ONCE")
                if(decision1==2):
                    camera = cv2.VideoCapture(0)
                    #cv2.imshow("Capturing", frame)
                    length=len(known_images)
                    length=2020010000+length
                    length=str(length)
                    known_images.append(length)
                    while True:



                        if((cv2.waitKey(1)%256)==32):
                            cv2.imshow("Capturing", frame)
                            return_value, image = camera.read()
                            cv2.imwrite("C:\\Users\\DHEERAJ SKYLARK\\PycharmProjects\\Dynamic_faceRecognition\\known_images\\"+length+".jpg", image)
                            #camera.release()
                            sta = unknown_entry(length)
                            if (sta == 1):
                                print("ENTRY SUCCESSFUL")
                        if (cv2.waitKey(1) & 0xFF == ord("q")):
                            #cv2.destroyWindow("Capturing")
                            del (camera)
                            break

            if (decision in ["N","n","No","NO","no"]):
                continue




        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    """"# Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
known_images.clear()
cv2.destroyAllWindows()"""