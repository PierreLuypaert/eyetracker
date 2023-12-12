import cv2
import numpy as np
from random import randint

# Charger le classificateur de visages Haarcascades
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialiser la capture vidéo depuis la caméra
cap = cv2.VideoCapture(0)

# Compteur pour l'incrément du nom du fichier
counter=0
taille_point_rouge = 30
folder_name = "eyes_detection"
# Taille de l'écran
screen_width, screen_height = 1920, 1080  # Mettez les dimensions de votre écran
# Créer une fenêtre pour le point rouge
red_point_window = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
red_point_x, red_point_y = randint(0, screen_width - 1 -taille_point_rouge), randint(0, screen_height - 1 -taille_point_rouge)
red_point_window[:] = 0  # Réinitialiser l'image
red_point_window[red_point_y:red_point_y+taille_point_rouge, red_point_x:red_point_x+taille_point_rouge] = (0, 0, 255)
while True:
    # Lire une image depuis la caméra
    ret, frame = cap.read()

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans l'image
    eyes = eyes_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(eyes)>1:
        (x1, y1, w1, h1) = eyes[0]
        (x2, y2, w2, h2) = eyes[1]


        eyes_sorted = []
        if ( x1 > x2): 
            eyes_sorted.append(eyes[1])
            eyes_sorted.append(eyes[0])
        else:
            eyes_sorted.append(eyes[0])
            eyes_sorted.append(eyes[1])

        
        (x1, y1, w1, h1) = eyes_sorted[0]
        (x2, y2, w2, h2) = eyes_sorted[1]
        # Créer une région d'intérêt (ROI)
        roi1 = gray[y1:y1 + h1, x1:x1 + w1]  # Utiliser l'échelle de gris
        roi2 = gray[y2:y2 + h2, x2:x2 + w2]  # Utiliser l'échelle de gris

        roi1_resized = cv2.resize(roi1, (100, 100))
        roi2_resized = cv2.resize(roi2, (100, 100))

        # Seuillage de l'image résultante (ROI)
        _, thresh1 = cv2.threshold(roi1_resized, 60, 255, cv2.THRESH_BINARY)
        _, thresh2 = cv2.threshold(roi2_resized, 60, 255, cv2.THRESH_BINARY)

        # Concaténer les deux images binaires
        combined_thresh = np.concatenate((thresh1, thresh2), axis=1)

        # Afficher l'image résultante (ROI)
        cv2.imshow('Combined Eyes Detection', combined_thresh)

        # Vérifier si la touche 'P' est pressée pour enregistrer les pixels
        key = cv2.waitKey(1)
        if key & 0xFF == ord('p'):
            # Incrémenter le compteur pour les visages
            counter += 1

            # Sauvegarder les pixels dans un fichier texte
            filename_eyes = f"{folder_name}/pixels_eyes_{counter}.txt"
            np.savetxt(filename_eyes, combined_thresh, fmt='%d', delimiter=', ')
            print(f"Pixels des yeux sauvegardés sous {filename_eyes}")

            filename = f"{folder_name}/eyes_{counter}.png"
            cv2.imwrite(filename, combined_thresh)
            print(f"Image enregistrée sous {filename}")       

            # Sauvegarder les coordonnées du point rouge dans un fichier texte
            filename_points = f"{folder_name}/points_increment_{counter}.txt"
            with open(filename_points, 'w') as f:
                f.write(f"{red_point_x}, {red_point_y}")
            print(f"Coordonnées du point rouge sauvegardées sous {filename_points}")

            # Changer l'emplacement du point rouge de manière aléatoire
            red_point_x, red_point_y = randint(0, screen_width - 1 -taille_point_rouge-100), randint(0, screen_height - 1 -taille_point_rouge-100)
            red_point_window[:] = 0  # Réinitialiser l'image
            red_point_window[red_point_y:red_point_y+taille_point_rouge, red_point_x:red_point_x+taille_point_rouge] = (0, 0, 255)  # Mettre le point rouge
        

        # Afficher la fenêtre du point rouge
        cv2.imshow('Red Point', red_point_window)
        
# Libérer les ressources et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
