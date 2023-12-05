import cv2
import numpy as np
from random import randint

# Charger le classificateur de visages Haarcascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialiser la capture vidéo depuis la caméra
cap = cv2.VideoCapture(0)

# Compteur pour l'incrément du nom du fichier
counter=0
taille_point_rouge = 30

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
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces)>0:
        (x, y, w, h) = faces[0]
        # Créer une région d'intérêt (ROI)
        roi = gray[y:y + h, x:x + w]  # Utiliser l'échelle de gris

        # Redimensionner l'image en 500x500 pixels
        roi_resized = cv2.resize(roi, (500, 500))

        # Dessiner un rectangle autour du visage détecté
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Afficher l'image résultante (ROI)
        cv2.imshow('Face Detection', roi_resized)

        # Vérifier si la touche 'P' est pressée pour enregistrer les pixels
        key = cv2.waitKey(1)
        if key & 0xFF == ord('p'):
            # Incrémenter le compteur pour les visages
            counter += 1

            # Sauvegarder les pixels dans un fichier texte
            filename_faces = f"detection/pixels_faces_{counter}.txt"
            np.savetxt(filename_faces, roi_resized, fmt='%d', delimiter=', ')
            print(f"Pixels du visage sauvegardés sous {filename_faces}")

            filename = f"detection/face_{counter}.png"
            cv2.imwrite(filename, roi_resized)
            print(f"Image enregistrée sous {filename}")        
            
            # Sauvegarder les coordonnées du point rouge dans un fichier texte
            filename_points = f"detection/points_increment_{counter}.txt"
            with open(filename_points, 'w') as f:
                f.write(f"{red_point_x}, {red_point_y}")
            print(f"Coordonnées du point rouge sauvegardées sous {filename_points}")

            # Changer l'emplacement du point rouge de manière aléatoire
            red_point_x, red_point_y = randint(0, screen_width - 1 -taille_point_rouge), randint(0, screen_height - 1 -taille_point_rouge)
            red_point_window[:] = 0  # Réinitialiser l'image
            red_point_window[red_point_y:red_point_y+taille_point_rouge, red_point_x:red_point_x+taille_point_rouge] = (0, 0, 255)  # Mettre le point rouge


        # Quitter la boucle si la touche 'q' est pressée
        elif key & 0xFF == ord('q'):
            break


        # Afficher la fenêtre du point rouge
        cv2.imshow('Red Point', red_point_window)

# Libérer les ressources et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
