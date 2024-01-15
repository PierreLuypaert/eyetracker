"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import time
import numpy as np

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)


def calculer_barycentre(point1, point2, point3, point4):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    barycentre_x = (x1 + x2 + x3 + x4) / 4
    barycentre_y = (y1 + y2 + y3 + y4) / 4

    return int(barycentre_x), int(barycentre_y)

def calibrate(gaze, webcam, isHorizontal, side):
    ratio_values = []

    while len(ratio_values) < 50:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text1 = f"Calibration en cours, veuillez regarder l'extrémité {side} de l'écran"
        text2 = f"Encore {50 - len(ratio_values)} valeurs"
        if isHorizontal:
            ratio = gaze.horizontal_ratio()
        else:
            ratio = gaze.vertical_ratio()

        if ratio:
            ratio_values.append(ratio)
        
        cv2.putText(frame, text1, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        cv2.putText(frame, text2, (90, 100), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 140), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 175), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("Demo", frame)
        if cv2.waitKey(1) == 27:
            break
    if side=="gauche" or side =="inférieure":
        edge = sorted(ratio_values)[-4]
    else:
        edge = sorted(ratio_values)[4]
    return edge

right_edge = calibrate(gaze, webcam, isHorizontal=True, side="droite")
print(f"{right_edge = }")

time.sleep(1.5)

left_edge = calibrate(gaze, webcam, isHorizontal=True, side="gauche")
print(f"{left_edge = }")

time.sleep(1.5)

up_edge = calibrate(gaze, webcam, isHorizontal=False, side="supérieure")
print(f"{right_edge = }")

time.sleep(1.5)

down_edge = calibrate(gaze, webcam, isHorizontal=False, side="inférieure")
print(f"{down_edge = }")

count = 0
memo = []
while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()
    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    horinzontal_ratio = gaze.horizontal_ratio()
    vertical_ratio = gaze.vertical_ratio()

    if horinzontal_ratio and vertical_ratio:
        count += 1

        # Créer une image noire
        height, width = 1080, 1920  # Définir la résolution de l'écran (vous pouvez ajuster cela selon vos besoins)
        height_square, width_square = 150, 150
        
        black_background = np.zeros((height, width, 3), dtype=np.uint8)

        # Définir les coordonnées et les dimensions du bloc rouge
        print(up_edge, vertical_ratio, down_edge)
        print(right_edge, horinzontal_ratio, left_edge)
        
        x, y = int((left_edge-horinzontal_ratio)/(left_edge-right_edge)*width), int((vertical_ratio-up_edge)/(down_edge-up_edge)*height)
        
        x = min( max( x , 0  ), width-width_square )
        y = min( max( y , 0  ), height-height_square )

        x, y, w, h = x, y, width_square, height_square  # Vous pouvez ajuster ces valeurs selon vos besoins
        
        memo.append((x,y))
        if len(memo) >= 4:
            bx, by = calculer_barycentre(*memo[-4:])
        else:
            bx, by = x, y
        # Remplir le bloc rouge sur l'image noire
        black_background[by:by+h, bx:bx+w] = [0, 0, 255]  # Rouge: B=0, G=0, R=255

        # Afficher l'image en plein écran
        cv2.namedWindow("Fenetre", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Fenetre", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.putText(black_background, f"{count} {x} {y}", (900, 100), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        cv2.imshow("Fenetre", black_background)


    hauteur, largeur, _ = frame.shape
    cv2.imshow("Webcam", cv2.resize(frame, (largeur//2, hauteur//2)))

    time.sleep(0.05)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
