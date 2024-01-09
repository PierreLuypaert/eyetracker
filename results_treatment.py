predictions = [
    [1156.6406, 668.7152],
    [380.49518, 663.21423],
    [1517.1211, 826.4623],
    [207.91968, 618.1046],
    [803.3808, 64.16281],
    [1443.8503, 223.68275],
    [198.4791, 173.58522],
    [964.3989, 347.24356],
    [586.07275, 137.4227],
    [1626.0854, 144.99167],
    [335.89844, 728.0176],
    [1700.915, 259.5384],
    [1555.4039, 253.15106],
    [1339.888, 174.1554],
    [823.076, -24.909943],
    [1179.4878, 416.04852],
    [1204.9639, 603.48724],
    [580.15845, 195.21146],
    [382.75732, 38.537476],
    [1425.8201, 684.09235],
    [342.7599, 154.48372],
    [688.07043, 91.044495],
    [440.81616, 676.77185],
    [139.32251, 529.0676],
    [568.07086, 101.4129],
    [1255.9564, 533.41547],
    [1547.7731, 517.69965]
]
y_test = [32, 53, 26, 59, 50, 71, 55, 41, 13, 54, 38, 58, 8, 42, 79, 69, 24, 18, 36, 45, 14, 80, 51, 64, 1, 74, 62]

from PIL import Image, ImageDraw
counter = 1

for index,y in enumerate(y_test):
# Lire les coordonnées depuis le fichier texte
	try:
		with open("eyes_detection/points_increment_"+str(y)+".txt", 'r') as fichier:
			contenu = fichier.read()
			# Supprimer les parenthèses et diviser les coordonnées
			x, y = map(int, contenu.strip('()\n').split(','))
	except FileNotFoundError:
		print("Le fichier texte spécifié n'a pas été trouvé.")
		exit()
	except ValueError:
		print("Le fichier texte ne contient pas des coordonnées valides.")
		exit()
	except Exception as e:
		print("Une erreur s'est produite :", str(e))
		exit()

	# Créer une image noire de la taille de l'écran
	largeur_ecran = 1920  # Remplacez par la largeur de votre écran
	hauteur_ecran = 1080  # Remplacez par la hauteur de votre écran
	image = Image.new('RGB', (largeur_ecran, hauteur_ecran), color='black')
	draw = ImageDraw.Draw(image)

	# Dessiner un carré rouge de 10x10 aux coordonnées (x, y)
	taille_carre = 50
	coin_sup_gauche = (x, y)
	coin_inf_droit = (x + taille_carre, y + taille_carre)
	draw.rectangle([coin_sup_gauche, coin_inf_droit], fill='red')


	taille_carre = 50
	coin_sup_gauche = (predictions[index][0], predictions[index][1])
	print(predictions[index][0])
	print(predictions[index][1])
	coin_inf_droit = (predictions[index][0] + taille_carre, predictions[index][1] + taille_carre)
	draw.rectangle([coin_sup_gauche, coin_inf_droit], fill='green')

	filename = f"results/eyes_{counter}.png"
	counter+=1
	image.save(filename)