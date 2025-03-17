from models.player import Player
from models.tournament import Tournament

# Création du tournoi
tournoi = Tournament(nom="Open Chess", lieu="Paris", date_debut="2025-03-17", date_fin="2025-03-20")

# Ajout des joueurs
joueurs = [
    Player(nom="Carlsen", prenom="Magnus", date_naissance="1990-11-30", identifiant_echecs="NO12345"),
    Player(nom="Nepo", prenom="Ian", date_naissance="1990-07-14", identifiant_echecs="RU67890"),
    Player(nom="Firouzja", prenom="Alireza", date_naissance="2003-06-18", identifiant_echecs="FR11223"),
    Player(nom="Ding", prenom="Liren", date_naissance="1992-10-24", identifiant_echecs="CN33445"),
]

for joueur in joueurs:
    tournoi.ajouter_joueur(joueur)

# Démarrer le tournoi
tournoi.demarrer_tournoi()
print(tournoi)  # Affichage du tournoi après démarrage

# Enregistrer les résultats du premier tour
resultats_tour1 = [(1, 0), (0.5, 0.5)]
tournoi.enregistrer_resultats_tour(1, resultats_tour1)

# Sauvegarde du tournoi
tournoi.sauvegarder_tournoi("data/tournoi.json")

# Affichage des infos mises à jour
for joueur in tournoi.joueurs:
    print(joueur)