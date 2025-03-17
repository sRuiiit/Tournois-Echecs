from models.player import Player
from models.round import Round

# Création de 4 joueurs
joueurs = [
    Player(nom="Carlsen", prenom="Magnus", date_naissance="1990-11-30", identifiant_echecs="NO12345"),
    Player(nom="Nepo", prenom="Ian", date_naissance="1990-07-14", identifiant_echecs="RU67890"),
    Player(nom="Firouzja", prenom="Alireza", date_naissance="2003-06-18", identifiant_echecs="FR11223"),
    Player(nom="Ding", prenom="Liren", date_naissance="1992-10-24", identifiant_echecs="CN33445"),
]

# Création d'un tour et génération des paires
round1 = Round(nom="Round 1", joueurs=joueurs)
round1.generer_paires()
print(round1)  # Affichage des paires avant les résultats

# Enregistrement des résultats (Carlsen et Firouzja gagnent)
round1.enregistrer_resultats([(1, 0), (1, 0)])
print(round1)  # Affichage après les résultats

# Vérification des points des joueurs
for joueur in joueurs:
    print(joueur)