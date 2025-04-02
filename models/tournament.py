import os
import time
from tinydb import TinyDB, Query
from models.player import Player
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
        self.timestamp = time.time()  # Ajout du timestamp
        self.id = None  # L'ID sera défini lors de la sauvegarde

    def ajouter_joueur(self, joueur: Player):
        self.joueurs.append(joueur)
        print(f"✅ Joueur {joueur.prenom} {joueur.nom} ajouté au tournoi '{self.nom}'.")

    def retirer_joueur(self, identifiant_echecs: str):
        self.joueurs = [joueur for joueur in self.joueurs if joueur.identifiant_echecs != identifiant_echecs]
        print(f"✅ Joueur avec l'identifiant {identifiant_echecs} retiré du tournoi '{self.nom}'.")

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
        Tournoi = Query()

        # Utiliser le timestamp pour générer un ID unique
        self.id = f"TOUR-{int(self.timestamp) % 10000:04d}"

        data = {
            "id": self.id,
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "nombre_tours": self.nombre_tours,
            "joueurs": [{"nom": j.nom, "prenom": j.prenom, "id": j.identifiant_echecs, "points": j.points} for j in self.joueurs],
            "tours": [tour.nom for tour in self.tours],
            "description": self.description,
            "timestamp": self.timestamp
        }
        db.insert(data)
        print(f"💾 Tournoi sauvegardé dans '{fichier}' avec l'ID {self.id}")

    @staticmethod
    def charger_tournoi(fichier, nom_tournoi):
        db = TinyDB(fichier)
        Tournoi = Query()
        result = db.search(Tournoi.nom == nom_tournoi)
        if result:
            data = result[0]
            tournoi = Tournament(data['nom'], data['lieu'], data['date_debut'], data['date_fin'])
            tournoi.id = data['id']
            tournoi.timestamp = data['timestamp']
            for joueur_data in data['joueurs']:
                joueur = Player(joueur_data['nom'], joueur_data['prenom'], joueur_data['date_naissance'], joueur_data['id'])
                joueur.points = joueur_data['points']
                tournoi.ajouter_joueur(joueur)
            tournoi.tours = data['tours']
            return tournoi
        else:
            print(f"Le tournoi '{nom_tournoi}' n'a pas été trouvé.")
        return None

    @staticmethod
    def lister_tournois(dossier):
        """Liste tous les tournois existants dans le dossier spécifié."""
        fichiers = [f for f in os.listdir(dossier) if f.endswith('.json')]
        if fichiers:
            for fichier in fichiers:
                chemin_complet = os.path.join(dossier, fichier)
                db = TinyDB(chemin_complet)
                tournois = db.all()
                for tournoi in tournois:
                    print(f"ID: {tournoi['id']}, Nom: {tournoi['nom']}")
        else:
            print("Aucun tournoi trouvé.")

    def afficher_resultats(self):
        """Affiche les résultats du tournoi."""
        print(f"\n🏆 Résultats du tournoi '{self.nom}':")
        for joueur in sorted(self.joueurs, key=lambda j: j.points, reverse=True):
            print(f"{joueur.prenom} {joueur.nom} - {joueur.points} pts")

    @staticmethod
    def tableau_resultats(dossier):
        """Affiche un tableau des résultats pour chaque tournoi."""
        fichiers = [f for f in os.listdir(dossier) if f.endswith('.json')]
        if fichiers:
            for fichier in fichiers:
                chemin_complet = os.path.join(dossier, fichier)
                db = TinyDB(chemin_complet)
                tournois = db.all()
                for tournoi in tournois:
                    print(f"\n🏆 Résultats du tournoi '{tournoi['nom']}':")
                    for joueur in sorted(tournoi['joueurs'], key=lambda j: j['points'], reverse=True):
                        print(f"{joueur['prenom']} {joueur['nom']} - {joueur['points']} pts")
        else:
            print("Aucun tournoi trouvé.")