from tinydb import TinyDB, Query
from models.player import Player  # Import de Player
from models.round import Round

class Tournament:
    """Gère un tournoi d'échecs avec plusieurs tours et joueurs. Sauvegarde fonctionnelle"""

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
        if numero_tour < 1 or numero_tour > len(self.tours):
            raise ValueError("Numéro de tour invalide.")

        tour = self.tours[numero_tour - 1]
        tour.enregistrer_resultats(resultats)

    def sauvegarder_tournoi(self, fichier: str):
        """Sauvegarde le tournoi sous format JSON."""
        db = TinyDB(fichier)
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
        db.insert(data)
        print(f"💾 Tournoi sauvegardé dans '{fichier}'")

    @staticmethod
    def charger_tournoi(fichier, nom_tournoi):
        db = TinyDB(fichier)
        Tournoi = Query()
        result = db.search(Tournoi.nom == nom_tournoi)
        if result:
            data = result[0]
            tournoi = Tournament(data['nom'], data['lieu'], data['date_debut'], data['date_fin'])
            for joueur_data in data['joueurs']:
                joueur = Player(joueur_data['nom'], joueur_data['prenom'], joueur_data['date_naissance'], joueur_data['id'])
                joueur.points = joueur_data['points']
                tournoi.ajouter_joueur(joueur)
            tournoi.tours = data['tours']
            return tournoi
        else:
            print(f"Le tournoi '{nom_tournoi}' n'a pas été trouvé.")
        return None