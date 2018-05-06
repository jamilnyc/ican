import sys

sys.path.append('../utils')
import aws
import csv
from S3 import S3

bucket = "icandata"

gandalf = "../img/special/CK1JSA.jpg"

r = '../data/recyclable.csv'
c = '../data/compost.csv'
s = '../data/special.csv'


def imageRec(image):
    '''
    imageRecognition takes in a image file
    Return the labels and texts detected from the image
    The labels and texts are ordered by confidence
    :image: file path
    :rtype: str()
    '''
    with open(image, 'rb') as f:
        pic = f.read()
    rek = aws.getClient('rekognition', 'us-east-1')
    res1 = rek.detect_labels(Image={"Bytes": pic})  # , MaxLabels=10, MinConfidence=.7)
    res2 = rek.detect_text(Image={"Bytes": pic})  # , MaxLabels=10, MinConfidence=.7)
    label = res1["Labels"]
    text = res2["TextDetections"]
    # print label
    label.sort(reverse=True, key=lambda x: x['Confidence'])
    # print label
    labellst = []
    for item in label:
        if item != '':
            labellst.append(item["Name"])
    # print nmlst
    # print text
    txt = []
    text.sort(reverse=True, key=lambda x: x["Confidence"])
    for item in text:
        if item != '' and item["DetectedText"].lower() not in txt:
            txt.append(item["DetectedText"].lower())
    labellst = labellst[:10]
    txt = txt[:10]
    d = {"labels": labellst, "texts": txt}
    return genTxt(d)


def genLabel(info):
    '''
    generateLabel takes in the image info,
    generate label from ['recyclable', 'compost', 'special', 'other']
    using the data set we have
    Return 1 for recycle, 2 for compost, 4 for special, 8 for other
    :info: Dict{'labels': [], 'texts': []}
    :rtype: Str()
    '''
    # print "genLabel"
    with open(r, 'r') as f:
        data = csv.reader(f)
        rec = list(data)[0]
    with open(c, 'r') as f:
        data = csv.reader(f)
        compost = list(data)[0]
    with open(s, 'r') as f:
        data = csv.reader(f)
        special = list(data)[0]
    slabel = info["labels"] + info["texts"]
    score = {
        "rec": 0,
        "comp": 0,
        "spec": 0,
    }
    # print slabel
    # print compost
    for l in slabel:
        if l.lower() in rec:
            score['rec'] += 1
        elif l.lower() in compost:
            score["comp"] += 1
        elif l.lower() in special:
            score['spec'] += 1
    cat = ""
    tmp = 0
    # print "scores", score['rec'], score['comp'], score['spec']
    for category, num in score.items():
        if cat == '':
            cat = category
            tmp = num
        elif num > tmp:
            tmp = num
            cat = category
    print tmp, cat
    if tmp == 0:
        # other stuff
        return 1 << 3
    else:
        if cat == 'rec':
            return 1
        elif cat == 'comp':
            return 1 << 1
        elif cat == 'spec':
            return 1 << 2
    return False


def genTxt(info):
    '''
    Generate text from info
    :info: dict{"labels": [], "texts": []}
    :rtype: str()
    '''
    txt = ''
    for label in info['labels'] + info['texts']:
        txt += label + ', '
    return txt[:-2]


def appendToCsvFile(fileName, data):
    with open(fileName, 'ab') as f:
        writer = csv.writer(f)
        # for d in data:
        writer.writerow(data)
    return


def pushToS3(fileName):
    print "Pushing to S3 . . . "
    s3Wrapper = S3(fileName)
    s3Wrapper.uploadData()


'''
def main(filename):
    info = imageRec(gandalf)
    print info
        #category = genLabel(info)
        #text = genTxt(info)
        #data.append([text, category])
    #appendToCsvFile(filename, data)
    #pushToS3(filename)
    '''

if __name__ == "__main__":
    main('trainData.csv')

