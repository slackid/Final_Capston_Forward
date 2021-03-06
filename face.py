import face_recognition
import numpy as np
import os
import csv
import cv2
import pandas as pd
from datetime import datetime


class face_function():
    def registerimage(self, cv2image, stu_num, name):
        face_landmarks_list = face_recognition.face_landmarks(cv2image)
        if face_landmarks_list:

            #이미지 밝기 향상
            contrast = 1.1
            brightness = 1
            cv2image[:, :, 2] = np.clip(contrast * cv2image[:, :, 2] + brightness, 0, 255)


            #이미지 얼굴 영역 추출
            filtered_image = self.apply_brightness_contrast(cv2image, -127, 127)

            hsv = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2HSV)
            #lower_blue = np.array([0, 180, 55])
            lower_blue = np.array([0, 90, 0])
            upper_blue = np.array([20, 255, 200])

            hsvmask = cv2.inRange(hsv, lower_blue, upper_blue)
            kernel = np.ones((10, 10), np.uint16)
            hsvmask = cv2.morphologyEx(hsvmask, cv2.MORPH_OPEN, kernel)
            hsvmask = cv2.morphologyEx(hsvmask, cv2.MORPH_CLOSE, kernel)

            res = cv2.bitwise_xor(cv2image, filtered_image, mask=hsvmask)

            ##area crop
            nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(hsvmask)

            #라벨이 존재 할 시
            if np.sum(labels) != 0:
                for i in range(nlabels):
                    if i < 2:
                        continue

                    area = stats[i, cv2.CC_STAT_AREA]
                    left = stats[i, cv2.CC_STAT_LEFT]
                    top = stats[i, cv2.CC_STAT_TOP]
                    width = stats[i, cv2.CC_STAT_WIDTH]
                    height = stats[i, cv2.CC_STAT_HEIGHT]

                    if area > 2500:
                        cv2.rectangle(res, (left - 30, top - 30), (left + width + 30, top + height + 3), (0, 0, 255), 1)

                    face_locations = face_recognition.face_locations(cv2image)
                    face_encodings = face_recognition.face_encodings(cv2image, face_locations)
                    face_encodings = np.asarray(face_encodings)

                    ## 특징값 저장
                    df = pd.DataFrame(face_encodings)
                    csvfiledir = "students/" + str(stu_num) + "_" + name + "/" + "captured_feature_data.csv"

                    # 파일이 이미 존재한다면
                    if (os.path.isfile(csvfiledir)):
                        countA = 0
                        countB = 0

                        #저장된 csv값과 얼굴 특징 비교, 출석 알고리즘
                        with open(csvfiledir, 'r') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')

                            for row in reader:

                                countA = countA+1
                                face_feature = list(map(float, row))

                                face_distances = face_recognition.face_distance(face_feature, face_encodings)

                                print('저장된 데이터와 ', 100-(face_distances*100), '% 일치합니다.')
                                if face_distances<0.3:
                                    df.to_csv(csvfiledir, mode='a', index=False, header=None)
                                    break
                                else:
                                    countB = countB + 1
                        csvfile.close()

                        #csv의 모든 특징 매치 후 일치하지 않는다면 False
                        if countA == countB:
                            print('check')
                            return False

                    #파일이 없다면
                    else:
                        df.to_csv(csvfiledir, index=False, header=None)

                    return True

            #이미지 밝기 낮음
            else:
                print('밝기 낮음')
                return False
        #얼굴 인식 안됨
        else:
            print('얼굴 인식 안됨')
            return False


    def check_face_num(self, cv2_image):
        face_landmark_list = face_recognition.face_landmarks(cv2_image)
        if face_landmark_list:
            face_locations = face_recognition.face_locations(cv2_image)

            if len(face_locations) == 1:
                print('이미지 얼굴 좌표 :', face_locations)
                return True
            else:
                return False

    def apply_brightness_contrast(self, input_img, brightness=0, contrast=0):
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow) / 255
            gamma_b = shadow
            buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
        else:
            buf = input_img.copy()
        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127 * (1 - f)
            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
        return buf