import os
from tinydb import TinyDB, Query
from models.player import Player
from models.tournament import Tournament

class CLI:
    """command line interface pour gérer le tournoi d'échecs."""

    def __init__(self):
        """Initialise les variables du programme. Crée un tournoi vide."""
        self.tournoi = None
        self.dossier_db = 'data'  # Chemin vers le dossier de la base de données

    def afficher_menu_principal(self):
        """Affiche le menu principal et gère les choix de l'utilisateur."""
        while True:
            print("\n🎉 Bienvenue dans le gestionnaire de tournois d'échecs 🎉")
            print("1. Créer un nouveau tournoi")
            print("2. Ajouter un joueur")
            print("3. Retirer un joueur")
            print("4. Démarrer le tournoi")
            print("5. Voir les résultats")
            print("6. Sauvegarder le tournoi")
            print("7. Lister les tournois existants")
            print("8. Afficher le tableau des résultats")
            print("9. Quitter")

            choix = input("➡️  Faites votre choix : ")

            if choix == "1":
                self.creer_tournoi()
            elif choix == "2":
                self.ajouter_joueur()
            elif choix == "3":
                self.retirer_joueur()
            elif choix == "4":
                self.demarrer_tournoi()
            elif choix == "5":
                self.afficher_resultats()
            elif choix == "6":
                self.sauvegarder_tournoi()
            elif choix == "7":
                self.lister_tournois()
            elif choix == "8":
                self.tableau_resultats()
            elif choix == "9":
                print("👋 Merci d'avoir utilisé le gestionnaire de tournois !")
                break
            else:
                print("⛔ Choix invalide, veuillez réessayer.")

    def creer_tournoi(self):
        """Crée un nouveau tournoi."""
        nom = input("Nom du tournoi : ")
        lieu = input("Lieu du tournoi : ")
        date_debut = input("Date de début (YYYY-MM-DD) : ")
        date_fin = input("Date de fin (YYYY-MM-DD) : ")
        self.tournoi = Tournament(nom, lieu, date_debut, date_fin)
        print(f"✅ Tournoi '{nom}' créé avec succès !")

    def choisir_tournoi(self):
        """Liste les tournois et demande à l'utilisateur de choisir l'ID du tournoi."""
        fichiers = [f for f in os.listdir(self.dossier_db) if f.endswith('.json')]
        if not fichiers:
            print("⛔ Aucun tournoi trouvé.")
            return None

        print("\n📋 Liste des tournois :")
        for fichier in fichiers:
            chemin_complet = os.path.join(self.dossier_db, fichier)
            db = TinyDB(chemin_complet)
            tournois = db.all()
            for tournoi in tournois:
                print(f"ID: {tournoi.doc_id}, Nom: {tournoi['nom']}")

        id_tournoi = int(input("➡️  Entrez l'ID du tournoi : "))
        for fichier in fichiers:
            chemin_complet = os.path.join(self.dossier_db, fichier)
            db = TinyDB(chemin_complet)
            tournoi = db.get(doc_id=id_tournoi)
            if tournoi:
                return Tournament.charger_tournoi(chemin_complet, tournoi['nom'])
        print("⛔ Tournoi non trouvé.")
        return None

    def ajouter_joueur(self):
        """Ajoute un joueur au tournoi."""
        self.tournoi = self.choisir_tournoi()
        if not self.tournoi:
            return

        nom = input("Nom du joueur : ")
        prenom = input("Prénom du joueur : ")
        date_naissance = input("Date de naissance (YYYY-MM-DD) : ")
        identifiant_echecs = input("Identifiant de la Fédération d'échecs : ")

        joueur = Player(nom, prenom, date_naissance, identifiant_echecs)
        self.tournoi.ajouter_joueur(joueur)
        print(f"✅ Joueur {prenom} {nom} ajouté avec succès !")

    def retirer_joueur(self):
        """Retire un joueur du tournoi."""
        self.tournoi = self.choisir_tournoi()
        if not self.tournoi:
            return

        identifiant_echecs = input("Identifiant de la Fédération d'échecs du joueur à retirer : ")
        self.tournoi.retirer_joueur(identifiant_echecs)

    def demarrer_tournoi(self):
        """Démarre le tournoi et permet de saisir les résultats."""
        self.tournoi = self.choisir_tournoi()
        if not self.tournoi:
            return
        if len(self.tournoi.joueurs) < 2:
            print("⛔ Il faut au moins 2 joueurs pour démarrer un tournoi.")
            return

        self.tournoi.demarrer_tournoi()
        print(f"🏁 Tournoi '{self.tournoi.nom}' démarré avec {len(self.tournoi.joueurs)} joueurs !")

        # Demander les résultats après chaque tour
        for numero_tour, tour in enumerate(self.tournoi.tours, 1):
            print(f"\n📊 {tour.nom} - Résultats :")
            resultats = []

            for match in tour.matchs:
                print(f"{match.joueur1.nom} vs {match.joueur2.nom}")
                score1 = float(input(f"Score de {match.joueur1.nom} (0, 0.5 ou 1) : "))
                score2 = float(input(f"Score de {match.joueur2.nom} (0, 0.5 ou 1) : "))
                resultats.append((score1, score2))

            # Enregistrer les résultats du tour
            self.tournoi.enregistrer_resultats_tour(numero_tour, resultats)
            print(f"✅ Résultats enregistrés pour {tour.nom} !")

    def afficher_resultats(self):
        """Affiche les résultats du tournoi."""
        self.tournoi = self.choisir_tournoi()
        if not self.tournoi:
            return

        self.tournoi.afficher_resultats()

    def sauvegarder_tournoi(self):
        """Sauvegarde le tournoi en JSON."""
        if not self.tournoi:
            print("⛔ Aucun tournoi à sauvegarder.")
            return

        fichier = f"data/{self.tournoi.nom.lower().replace(' ', '_')}.json"
        self.tournoi.sauvegarder_tournoi(fichier)
        print(f"💾 Tournoi sauvegardé dans '{fichier}'")

    def lister_tournois(self):
        """Liste tous les tournois existants."""
        Tournament.lister_tournois(self.dossier_db)

    def tableau_resultats(self):
        """Affiche un tableau des résultats pour chaque tournoi."""
        Tournament.tableau_resultats(self.dossier_db)

# Si ce fichier est exécuté directement, lancer le menu CLI
if __name__ == "__main__":
    cli = CLI()
    cli.afficher_menu_principal()