import os
import cv2
from paddleocr import PaddleOCR

# Create your tests here.
# OCR 准确度测试

path = "E:/Profile/Desktop/fwwb/DataForCompetitor/DataForCompetitor/"
img_dir = "train/"
txt = "train_label.txt"

labels = {}
res = []


def readImg():
    output = open(path + "output.txt", "w+", encoding="utf-8")
    imgs = os.listdir(path + img_dir)
    pt = 1
    for img in imgs:
        img_path = path + img_dir + img
        img_name = img.split(".jpg")[0]
        ocr_res = ocr(img_path)
        res.append({'name': img_name, 'res': ocr_res})
        out_str = img_dir + img + "\t" + ocr_res + "\n"
        print(out_str, file=output)
        print(">>> img:", img, " - ", ocr_res, " | ", pt, "/", len(imgs), "\n")
        pt += 1
    output.close()


def ocr(p) -> str:
    # pp ocr
    res_str = ''
    result = PaddleOCR(use_angle_cls=True, lang="ch").ocr(p, cls=True)
    if result is None:
        return ""

    for idx in range(len(result)):
        res = result[idx]
        if res is None:
            continue
        for line in res:
            if line is not None:
                res_str += line[1][0]
    return res_str


def readTxt():
    f = open(path + txt, "r", encoding='utf-8')
    lines = f.readlines()
    f.close()
    pt = 1
    for line in lines:
        line = line.replace("\r", "")
        line = line.replace("\n", "")
        line = line.replace("\t", "")
        line = line.split(".jpg")
        labels[line[0]] = line[1]
        print(">>> line:", line, " ", pt, "/", len(lines))
        pt += 1


def test():
    print("===== TEST =====")
    print("> readImg:")
    readImg()
    readTxt()

    rate = 0
    total = 122387
    for i in range(total):
        name = res[i]['name']
        ocr_res = res[i]['res']
        label_res = labels[name]
        if ocr_res == label_res:
            rate += 1
        print(">>> ocr:", ocr_res, " / ", label_res, " ", i, " /122387")
    print(">>> rate:", float(rate) / float(total))


if __name__ == '__main__':
    test()
