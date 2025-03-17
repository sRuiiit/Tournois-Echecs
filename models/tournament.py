import datetime
import json
from models.player import Player
from models.round import Round

class Tournament:
    """Gère un tournoi d'échecs avec plusieurs tours et joueurs."""

    def __init__(self, nom: str, lieu: str, date_debut: str, date_fin: str, nombre_tours: int = 4):
        """
        Initialise un tournoi avec son nom, son lieu et ses dates.

        :param nom: Nom du tournoi
        :param lieu: Lieu où se déroule le tournoi
        :param date_debut: Date de début (format YYYY-MM-DD)
        :param date_fin: Date de fin (format YYYY-MM-DD)
        :param nombre_tours: Nombre total de tours (par défaut: 4)
        """
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_tours = nombre_tours
        self.tours = []  # Liste des tours du tournoi
        self.joueurs = []  # Liste des joueurs inscrits
        self.description = ""  # Notes générales du directeur de tournoi

    def ajouter_joueur(self, joueur: Player):
        """
        Ajoute un joueur au tournoi.

        :param joueur: Instance de Player
        """
        self.joueurs.append(joueur)

    def demarrer_tournoi(self):
        """
        Démarre le tournoi en générant les tours et les matchs.
        """
        if len(self.joueurs) < 2:
            raise ValueError("Il faut au moins 2 joueurs pour démarrer un tournoi.")

        for i in range(self.nombre_tours):
            tour = Round(f"Round {i+1}", self.joueurs)
            tour.generer_paires()
            self.tours.append(tour)

    def enregistrer_resultats_tour(self, numero_tour: int, resultats: list[tuple[float, float]]):
        """
        Enregistre les résultats d'un tour donné.

        :param numero_tour: Numéro du tour (1, 2, etc.)
        :param resultats: Liste des scores pour chaque match
        """
        if numero_tour < 1 or numero_tour > len(self.tours):
            raise ValueError("Numéro de tour invalide.")

        self.tours[numero_tour - 1].enregistrer_resultats(resultats)

    def sauvegarder_tournoi(self, fichier: str):
        """
        Sauvegarde le tournoi sous format JSON.

        :param fichier: Nom du fichier JSON
        """
        data = {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "nombre_tours": self.nombre_tours,
            "joueurs": [{"nom": j.nom, "prenom": j.prenom, "id": j.identifiant_echecs, "points": j.points} for j in self.joueurs],
            "tours": [tour.nom for tour in self.tours],
            "description": self.description,
        }
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def __str__(self):
        """Retourne une représentation lisible du tournoi."""
        return f"Tournoi {self.nom} à {self.lieu}, {len(self.joueurs)} joueurs, {self.nombre_tours} tours."