from models.player import Player


class Match:
    """Représente un match entre deux joueurs avec attribution des points."""

    def __init__(self, joueur1: Player, joueur2: Player):
        """
        Initialise un match entre deux joueurs.

        :param joueur1: Premier joueur
        :param joueur2: Deuxième joueur
        """
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score1 = 0
        self.score2 = 0

    def enregistrer_resultat(self, score1: float, score2: float):
        """Enregistre le résultat du match et met à jour les joueurs."""
        print(f"📌 Résultat du match : {self.joueur1.nom} ({score1}) vs {self.joueur2.nom} ({score2})")  # Debug

        self.joueur1.ajouter_points(score1)
        self.joueur2.ajouter_points(score2)

        self.score1 = score1
        self.score2 = score2
    def __str__(self):
        """Retourne une représentation lisible du match."""
        return f"{self.joueur1} vs {self.joueur2} - Score: {self.score1}-{self.score2}"