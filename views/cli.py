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
            print("\n--- Tournois ---")
            print("1. Créer")
            print("2. Lister les tournois existants")
            print("3. Effacer un tournoi")
            print("4. Démarrer le tournoi")
            print("--- Joueurs ---")
            print("5. Ajouter")
            print("6. Retirer")
            print("7. Lister")
            print("--- Résultats ---")
            print("8. Afficher les résultats")
            print("9. Quitter")

            choix = input("➡️  Faites votre choix : ")

            if choix == "1":
                self.creer_tournoi()
            elif choix == "2":
                self.lister_tournois()
            elif choix == "3":
                self.effacer_tournoi()
            elif choix == "4":
                self.demarrer_tournoi()
            elif choix == "5":
                self.ajouter_joueur()
            elif choix == "6":
                self.retirer_joueur()
            elif choix == "7":
                self.lister_joueurs()
            elif choix == "8":
                self.afficher_resultats()
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
        self.demander_sauvegarde()

    def lister_tournois(self):
        """Liste tous les tournois existants."""
        Tournament.lister_tournois(self.dossier_db)

    def effacer_tournoi(self):
        """Efface un tournoi existant."""
        id_tournoi = input("➡️  Entrez l'ID du tournoi à effacer (format TOUR-nnnn) : ")
        fichiers = [f for f in os.listdir(self.dossier_db) if f.endswith('.json')]
        for fichier in fichiers:
            chemin_complet = os.path.join(self.dossier_db, fichier)
            db = TinyDB(chemin_complet)
            tournoi = db.get(Query().id == id_tournoi)
            if tournoi:
                db.remove(Query().id == id_tournoi)
                print(f"🗑️ Tournoi '{tournoi['nom']}' effacé avec succès !")
                self.demander_sauvegarde()
                return
        print("⛔ Tournoi non trouvé.")

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
        self.demander_sauvegarde()

    def retirer_joueur(self):
        """Retire un joueur du tournoi."""
        self.tournoi = self.choisir_tournoi()
        if not self.tournoi:
            return

        identifiant_echecs = input("Identifiant de la Fédération d'échecs du joueur à retirer : ")
        self.tournoi.retirer_joueur(identifiant_echecs)
        self.demander_sauvegarde()

    def lister_joueurs(self):
        """Liste tous les joueurs et les tournois auxquels ils participent."""
        fichiers = [f for f in os.listdir(self.dossier_db) if f.endswith('.json')]
        if not fichiers:
            print("⛔ Aucun tournoi trouvé.")
            return

        joueurs_tournois = {}
        for fichier in fichiers:
            chemin_complet = os.path.join(self.dossier_db, fichier)
            db = TinyDB(chemin_complet)
            tournois = db.all()
            for tournoi in tournois:
                for joueur in tournoi['joueurs']:
                    joueur_id = joueur['id']
                    if joueur_id not in joueurs_tournois:
                        joueurs_tournois[joueur_id] = {
                            "nom": joueur['nom'],
                            "prenom": joueur['prenom'],
                            "tournois": []
                        }
                    joueurs_tournois[joueur_id]['tournois'].append(tournoi['nom'])

        print("\n📋 Liste des joueurs et leurs tournois :")
        for joueur_id, info in joueurs_tournois.items():
            print(f"{info['prenom']} {info['nom']} (ID: {joueur_id}) - Tournois : {', '.join(info['tournois'])}")

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
        self.demander_sauvegarde()

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

    def demander_sauvegarde(self):
        """Demande à l'utilisateur s'il souhaite sauvegarder les modifications."""
        choix = input("💾 Souhaitez-vous sauvegarder les modifications ? (o/n) : ")
        if choix.lower() == 'o':
            self.sauvegarder_tournoi()

    def choisir_tournoi(self):
        """Liste les tournois et demande à l'utilisateur de choisir l'ID du tournoi."""
        fichiers = [f for f in os.listdir(self.dossier_db) if f.endswith('.json')]
        if not fichiers:
            print("⛔ Aucun tournoi trouvé.")
            return None

        tournois_vus = set()
        print("\n📋 Liste des tournois :")
        for fichier in fichiers:
            chemin_complet = os.path.join(self.dossier_db, fichier)
            db = TinyDB(chemin_complet)
            tournois = db.all()
            for tournoi in tournois:
                if tournoi['id'] not in tournois_vus:
                    print(f"ID: {tournoi['id']}, Nom: {tournoi['nom']}")
                    tournois_vus.add(tournoi['id'])

        id_tournoi = input("➡️  Entrez l'ID du tournoi (format TOUR-nnnn) : ")
        for fichier in fichiers:
            chemin_complet = os.path.join(self.dossier_db, fichier)
            db = TinyDB(chemin_complet)
            tournoi = db.get(Query().id == id_tournoi)
            if tournoi:
                return Tournament.charger_tournoi(chemin_complet, tournoi['nom'])
        print("⛔ Tournoi non trouvé.")
        return None

# Si ce fichier est exécuté directement, lancer le menu CLI
if __name__ == "__main__":
    cli = CLI()
    cli.afficher_menu_principal()