# Conception du projet oculomètre

|

## Rappel de la formalisation
## Objectif:
Implémentation d'un oculomètre
Minimiser l'écart entre les coordonnées estimées et les coordonnées réelles

## Input :
Flux vidéo de la Webcam


## Output:
- Coordonnées x,y de l'endroit que l'on regarde sur l'écran
- Dans une GUI, faire un cercle centré sur le point de coordonnées x,y
    - le rayon du cercle s'agrandit lors des fixations
    - on affiche des traits pour les saccades (Si frame rate de la webcam suffisant)

## Mécanisme de validation:
- Utiliser un occulomètre de référence pour comparer nos estimations
- Faire un cercle qui se déplace et demander à l'utilisateur de regarder ce cercle, on pourra comparer les coordonnées du cercle et les coordonnées estimées par notre solution

|

# Conception retenue
1. Récupération de la vidéo

	Extraction du flux vidéo de la webcam utilisateur
2. Traitement de l'image

	2.1 Détection du visage
	2.2 Détection des yeux
	2.3 Extraction des caractéristiques des yeux

3. Prédiction de la position du regard
	3.1 Par apprentissage d'un modèle
	3.2 Par trigonométrie
4. Interface graphique

	4.1 Module de calibrage
	4.2 Fenêtre d'affichage du cercle, représentation la position du regard calculée en temps réel
5. Validation

	5.1 Comparaison des résultats avec un oculomètre de référence.  
	5.2 Interaction avec un cercle mobile pour évaluer la précision du système.

