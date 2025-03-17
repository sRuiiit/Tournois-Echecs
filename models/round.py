import datetime
from models.match import Match
from models.player import Player

class Round:
    """Représente un tour d'un tournoi d'échecs, contenant plusieurs matchs."""

    def __init__(self, nom: str, joueurs: list[Player]):
        """
        Initialise un tour avec un nom et une liste de joueurs.

        :param nom: Nom du tour (ex: "Round 1")
        :param joueurs: Liste des joueurs participant à ce tour
        """
        self.nom = nom
        self.joueurs = joueurs
        self.matchs = []
        self.date_debut = datetime.datetime.now()
        self.date_fin = None

    def generer_paires(self):
        """Génère les paires de joueurs pour les matchs en triant les joueurs selon leur score."""
        self.joueurs.sort(key=lambda joueur: joueur.points, reverse=True)
        self.matchs = []

        for i in range(0, len(self.joueurs), 2):
            if i + 1 < len(self.joueurs):
                match = Match(self.joueurs[i], self.joueurs[i + 1])
                self.matchs.append(match)

    def enregistrer_resultats(self, resultats: list[tuple[float, float]]):
        """Enregistre les résultats des matchs et met à jour les joueurs."""
        if len(resultats) != len(self.matchs):
            raise ValueError("Le nombre de résultats doit correspondre au nombre de matchs.")

        print(f"📌 Mise à jour des résultats pour {self.nom}...")  # Debug

        for i, (score1, score2) in enumerate(resultats):
            print(f"🆚 Match {i + 1} : {self.matchs[i].joueur1.nom} vs {self.matchs[i].joueur2.nom}")  # Debug
            print(
                f"   Avant : {self.matchs[i].joueur1.nom} ({self.matchs[i].joueur1.points} pts) - {self.matchs[i].joueur2.nom} ({self.matchs[i].joueur2.points} pts)")

            self.matchs[i].enregistrer_resultat(score1, score2)

            print(
                f"   Après : {self.matchs[i].joueur1.nom} ({self.matchs[i].joueur1.points} pts) - {self.matchs[i].joueur2.nom} ({self.matchs[i].joueur2.points} pts)")  # Debug

        self.date_fin = datetime.datetime.now()