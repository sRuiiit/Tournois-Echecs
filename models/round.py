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
        self.matchs = []  # Liste des matchs de ce tour
        self.date_debut = datetime.datetime.now()  # Timestamp du début
        self.date_fin = None  # Sera défini à la fin du tour

    def generer_paires(self):
        """
        Génère les paires de joueurs pour les matchs en triant les joueurs selon leur score.
        """
        self.joueurs.sort(key=lambda joueur: joueur.points, reverse=True)  # Trier par score décroissant
        self.matchs = []

        for i in range(0, len(self.joueurs), 2):
            if i + 1 < len(self.joueurs):
                match = Match(self.joueurs[i], self.joueurs[i + 1])
                self.matchs.append(match)

    def enregistrer_resultats(self, resultats: list[tuple[float, float]]):
        """
        Enregistre les résultats de chaque match et met à jour les scores des joueurs.

        :param resultats: Liste de tuples (score1, score2) pour chaque match
        """
        if len(resultats) != len(self.matchs):
            raise ValueError("Le nombre de résultats doit correspondre au nombre de matchs.")

        for i, (score1, score2) in enumerate(resultats):
            self.matchs[i].enregistrer_resultat(score1, score2)

        self.date_fin = datetime.datetime.now()  # Enregistrer la fin du tour

    def __str__(self):
        """Retourne une représentation lisible du tour et des matchs."""
        matchs_str = "\n".join(str(match) for match in self.matchs)
        return f"{self.nom} (Début: {self.date_debut}, Fin: {self.date_fin})\n{matchs_str}"