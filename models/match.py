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
        self.score1 = 0  # Score du joueur 1
        self.score2 = 0  # Score du joueur 2

    def enregistrer_resultat(self, score1: float, score2: float):
        """
        Enregistre le résultat du match et met à jour les scores des joueurs.

        :param score1: Score attribué au joueur1 (0, 0.5 ou 1)
        :param score2: Score attribué au joueur2 (0, 0.5 ou 1)
        """
        if (score1, score2) not in [(1, 0), (0, 1), (0.5, 0.5)]:
            raise ValueError("Les scores doivent être (1,0), (0,1) ou (0.5,0.5)")

        self.score1 = score1
        self.score2 = score2

        # Mise à jour des points des joueurs
        self.joueur1.ajouter_points(score1)
        self.joueur2.ajouter_points(score2)

    def __str__(self):
        """Retourne une représentation lisible du match."""
        return f"{self.joueur1} vs {self.joueur2} - Score: {self.score1}-{self.score2}"