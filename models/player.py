class Player:
    """Représente un joueur d'échecs avec un identifiant unique."""

    def __init__(self, nom: str, prenom: str, date_naissance: str, identifiant_echecs: str):
        """
        Initialise un joueur avec ses informations personnelles.

        :param nom: Nom de famille du joueur
        :param prenom: Prénom du joueur
        :param date_naissance: Date de naissance (format YYYY-MM-DD)
        :param identifiant_echecs: Identifiant unique de la Fédération d'échecs (ex: AB12345)
        """
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.identifiant_echecs = identifiant_echecs
        self.points = 0  # Score du joueur dans le tournoi

    def __str__(self):
        """Retourne une représentation lisible du joueur."""
        return f"{self.prenom} {self.nom} (ID: {self.identifiant_echecs}) - {self.points} pts"

    def ajouter_points(self, points: float):
        """
        Ajoute des points au joueur après un match.
        """
        print(f"🟢 Ajout de {points} pts à {self.prenom} {self.nom} (avant: {self.points} pts)")  # Debug
        self.points += points
        print(f"✅ Nouveau score de {self.prenom} {self.nom} : {self.points} pts")  # Debug