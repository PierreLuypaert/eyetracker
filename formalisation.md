# Formalisation du projet oculomètre
## Objectif:
Implémentation d'un occulomètre
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
