from models.player import Player

# Création d'un joueur
joueur1 = Player(nom="Carlsen", prenom="Magnus", date_naissance="1990-11-30", identifiant_echecs="NO12345")

# Affichage des infos du joueur
print(joueur1)

# Ajout de points après un match
joueur1.ajouter_points(1)
print(joueur1)  # Doit afficher 1 pt

joueur1.ajouter_points(0.5)
print(joueur1)  # Doit afficher 1.5 pts