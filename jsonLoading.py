import json as j
import csv
import cv2
import argparse

BASE_PATH = "C:\SFDeepfakeProject\\"
DATA_PATH = "dfdc_train_part_00\dfdc_train_part_0\\"
METADATA_NAME = "metadata.json"
FIELDS = ["Name", "Label", "Split", "Original", "Frame Size", "Frame Count", "Duration(Seconds)"]

def generateRealAndFake(jsonFile, fakeVid):
    f = open(BASE_PATH + DATA_PATH + jsonFile)
    data = j.load(f)
    pathToVid = BASE_PATH + DATA_PATH

    vidcap = cv2.VideoCapture(pathToVid + str(fakeVid))
    success, image = vidcap.read()
    if success:
        cv2.imwrite("first_frame_FAKE.jpg", image)

    vidcap = cv2.VideoCapture(pathToVid + data[str(fakeVid)]["original"])
    success, image = vidcap.read()
    if success:
        cv2.imwrite("first_frame_REAL.jpg", image)

def displayVideos(jsonFile, count):
    f = open(BASE_PATH + DATA_PATH + jsonFile)
    data = j.load(f)
    pathToVid = BASE_PATH + DATA_PATH
    for i in data:
        cap = cv2.VideoCapture(pathToVid + str(i))
        while (cap.isOpened()):
            ret, frame = cap.read()
            frame = cv2.resize(frame, (360, 240))
            cv2.imshow("video", frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        
        count-=1
        if (count == 0):
            break

    cap.release()
    cv2.destroyAllWindows()
    f.close()

def getFrameSize(file):
    cap = cv2.VideoCapture(file)
    ret, frame = cap.read()
    shape = frame.shape
    cap.release()
    return shape

def getVideoLength(file):
    cap = cv2.VideoCapture(file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    cap.release()
    retval = [round(fps), round(duration)]
    return retval

def getMetadata(jsonFile, outputFile, count):
    f = open(BASE_PATH + DATA_PATH + jsonFile)
    data = j.load(f)

    #loading data
    rows = []
    pathToVid = BASE_PATH + DATA_PATH
    for i in data:
        if (data[str(i)]["label"] == "FAKE"):
            curr = [str(i),"FAKE", data[str(i)]["split"], data[str(i)]["original"], getFrameSize(pathToVid+str(i)), str(getVideoLength(pathToVid+str(i))[0]),  str(getVideoLength(pathToVid+str(i))[1])]
            rows.append(curr)
        else:
            curr = [str(i),"REAL", data[str(i)]["split"], "Not Applicable", getFrameSize(pathToVid+str(i)), str(getVideoLength(pathToVid+str(i))[0]),  str(getVideoLength(pathToVid+str(i))[1])]
            rows.append(curr)
        
        count-=1
        if (count == 0):
            break

    #writing to csv file
    with open(outputFile, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(FIELDS)
        csvwriter.writerows(rows)
    
    f.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--count", required = True, help="number of videos to load into csv")
    ap.add_argument("-j", "--json", required = True, help="meta data json file")
    ap.add_argument("-o", "--output", required = True, help="output file")
    args = vars(ap.parse_args())
    count = int(args["count"])
    jsonFile = args["json"]
    outputFile = args["output"]
    
    getMetadata(jsonFile, outputFile, count)
    #displayVideos(jsonFile, count)
    generateRealAndFake(jsonFile, "owxbbpjpch.mp4")

if (__name__ == "__main__"):
    main()