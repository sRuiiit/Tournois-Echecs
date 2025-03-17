from models.round import Round
from models.player import Player
import json

class Tournament:
    """Gère un tournoi d'échecs avec plusieurs tours et joueurs."""

    def __init__(self, nom: str, lieu: str, date_debut: str, date_fin: str, nombre_tours: int = 4):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_tours = nombre_tours
        self.tours = []
        self.joueurs = []
        self.description = ""

    def ajouter_joueur(self, joueur: Player):
        self.joueurs.append(joueur)

    def demarrer_tournoi(self):
        if len(self.joueurs) < 2:
            raise ValueError("Il faut au moins 2 joueurs pour démarrer un tournoi.")

        for i in range(self.nombre_tours):
            tour = Round(f"Round {i+1}", self.joueurs)
            tour.generer_paires()
            self.tours.append(tour)

    def enregistrer_resultats_tour(self, numero_tour: int, resultats: list[tuple[float, float]]):
        """Enregistre les résultats d'un tour donné."""
        if numero_tour < 1 or numero_tour > len(self.tours):
            raise ValueError("Numéro de tour invalide.")

        print(f"📊 Enregistrement des résultats du tour {numero_tour}...")  # Debug
        tour = self.tours[numero_tour - 1]

        print(f"🔍 Avant mise à jour : {[(j.prenom, j.nom, j.points) for j in self.joueurs]}")  # Debug

        tour.enregistrer_resultats(resultats)

        print(f"✅ Après mise à jour : {[(j.prenom, j.nom, j.points) for j in self.joueurs]}")  # Debug