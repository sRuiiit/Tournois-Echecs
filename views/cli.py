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
            print("3. Démarrer le tournoi")
            print("4. Voir les résultats")
            print("5. Sauvegarder le tournoi")
            print("6. Lister les tournois existants")
            print("7. Quitter")

            choix = input("➡️  Faites votre choix : ")

            if choix == "1":
                self.creer_tournoi()
            elif choix == "2":
                self.ajouter_joueur()
            elif choix == "3":
                self.demarrer_tournoi()
            elif choix == "4":
                self.afficher_resultats()
            elif choix == "5":
                self.sauvegarder_tournoi()
            elif choix == "6":
                self.lister_tournois()
            elif choix == "7":
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

    def ajouter_joueur(self):
        """Ajoute un joueur au tournoi."""
        if not self.tournoi:
            print("⛔ Veuillez d'abord créer un tournoi.")
            return

        nom = input("Nom du joueur : ")
        prenom = input("Prénom du joueur : ")
        date_naissance = input("Date de naissance (YYYY-MM-DD) : ")
        identifiant_echecs = input("Identifiant de la Fédération d'échecs : ")

        joueur = Player(nom, prenom, date_naissance, identifiant_echecs)
        self.tournoi.ajouter_joueur(joueur)
        print(f"✅ Joueur {prenom} {nom} ajouté avec succès !")

    def demarrer_tournoi(self):
        """Démarre le tournoi et permet de saisir les résultats."""
        if not self.tournoi:
            print("⛔ Veuillez d'abord créer un tournoi.")
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
        if not self.tournoi:
            print("⛔ Aucun tournoi en cours.")
            return

        print(f"\n🏆 Résultats du tournoi '{self.tournoi.nom}':")
        for joueur in sorted(self.tournoi.joueurs, key=lambda j: j.points, reverse=True):
            print(f"{joueur.prenom} {joueur.nom} - {joueur.points} pts")

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

# Si ce fichier est exécuté directement, lancer le menu CLI
if __name__ == "__main__":
    cli = CLI()
    cli.afficher_menu_principal()