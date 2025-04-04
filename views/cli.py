import os
from tinydb import TinyDB, Query
from models.player import Player
from models.tournament import Tournament

class CLI:
    """Interface en ligne de commande pour gérer le tournoi d'échecs."""

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
            print("5. Créer")
            print("6. Ajouter à un tournoi")
            print("7. Retirer d'un tournoi")
            print("8. Lister")
            print("--- Résultats ---")
            print("9. Afficher les résultats")
            print("10. Quitter")

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
                self.creer_joueur()
            elif choix == "6":
                self.attribuer_joueur_tournoi()
            elif choix == "7":
                self.retirer_joueur()
            elif choix == "8":
                self.lister_joueurs()
            elif choix == "9":
                self.afficher_resultats()
            elif choix == "10":
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
        fichiers = [f for f in os.listdir(self.dossier_db) if f.endswith('.json')]
        if not fichiers:
            print("⛔ Aucun tournoi trouvé.")
            return

        for fichier in fichiers:
            chemin_complet = os.path.join(self.dossier_db, fichier)
            db = TinyDB(chemin_complet)
            tournois = db.all()
            for tournoi in tournois:
                tournoi_id = tournoi.get('id', 'ID non disponible')
                print(f"ID: {tournoi_id}, Nom: {tournoi['nom']}")

    def effacer_tournoi(self):
        """Efface un tournoi existant."""
        self.tournoi = self.choisir_tournoi()
        if not self.tournoi:
            return

        fichier_tournoi = f"{self.tournoi.nom.lower().replace(' ', '_')}.json"
        chemin_complet = os.path.join(self.dossier_db, fichier_tournoi)

        if os.path.exists(chemin_complet):
            os.remove(chemin_complet)
            print(f"🗑️ Tournoi '{self.tournoi.nom}' effacé avec succès !")
        else:
            print("⛔ Tournoi non trouvé.")

    def creer_joueur(self):
        """Crée un joueur indépendamment d'un tournoi."""
        nom = input("Nom du joueur : ")
        prenom = input("Prénom du joueur : ")
        date_naissance = input("Date de naissance (YYYY-MM-DD) : ")
        identifiant_echecs = input("Identifiant de la Fédération d'échecs : ")

        joueur = Player(nom, prenom, date_naissance, identifiant_echecs)
        fichier_joueur = f"data/joueurs.json"
        db = TinyDB(fichier_joueur)
        db.insert({
            "nom": nom,
            "prenom": prenom,
            "date_naissance": date_naissance,
            "identifiant_echecs": identifiant_echecs
        })
        print(f"✅ Joueur {prenom} {nom} créé avec succès !")

    def attribuer_joueur_tournoi(self):
        """Attribue un joueur existant à un tournoi."""
        self.tournoi = self.choisir_tournoi()
        if not self.tournoi:
            return

        fichier_joueur = f"data/joueurs.json"
        db = TinyDB(fichier_joueur)
        joueurs = db.all()

        if not joueurs:
            print("⛔ Aucun joueur trouvé.")
            return

        print("\n📋 Liste des joueurs :")
        for index, joueur in enumerate(joueurs, start=1):
            print(f"{index}. {joueur['prenom']} {joueur['nom']} (ID: {joueur['identifiant_echecs']})")

        choix = int(input("➡️  Entrez le numéro du joueur : ")) - 1
        if 0 <= choix < len(joueurs):
            joueur_data = joueurs[choix]
            joueur = Player(joueur_data['nom'], joueur_data['prenom'], joueur_data['date_naissance'], joueur_data['identifiant_echecs'])
            self.tournoi.ajouter_joueur(joueur)
            self.demander_sauvegarde()
        else:
            print("⛔ Choix invalide.")

    def retirer_joueur(self):
        """Retire un joueur du tournoi."""
        self.tournoi = self.choisir_tournoi()
        if not self.tournoi:
            return

        joueur = self.choisir_joueur()
        if joueur:
            self.tournoi.retirer_joueur(joueur.identifiant_echecs)
            self.demander_sauvegarde()

    def lister_joueurs(self):
        """Liste tous les joueurs et les tournois auxquels ils participent."""
        fichier_joueur = f"data/joueurs.json"
        db_joueurs = TinyDB(fichier_joueur)
        joueurs = db_joueurs.all()

        if not joueurs:
            print("⛔ Aucun joueur trouvé.")
            return

        joueurs_tournois = {joueur['identifiant_echecs']: {
            "nom": joueur['nom'],
            "prenom": joueur['prenom'],
            "tournois": []
        } for joueur in joueurs}

        fichiers = [f for f in os.listdir(self.dossier_db) if f.endswith('.json')]
        for fichier in fichiers:
            chemin_complet = os.path.join(self.dossier_db, fichier)
            db = TinyDB(chemin_complet)
            tournois = db.all()
            for tournoi in tournois:
                if 'joueurs' in tournoi:
                    for joueur in tournoi['joueurs']:
                        joueur_id = joueur['identifiant_echecs']
                        if joueur_id in joueurs_tournois:
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
        """Liste les tournois et demande à l'utilisateur de choisir un tournoi par numéro."""
        fichiers = [f for f in os.listdir(self.dossier_db) if f.endswith('.json')]
        if not fichiers:
            print("⛔ Aucun tournoi trouvé.")
            return None

        tournois = []
        print("\n📋 Liste des tournois :")
        for fichier in fichiers:
            chemin_complet = os.path.join(self.dossier_db, fichier)
            db = TinyDB(chemin_complet)
            tournois.extend(db.all())

        for index, tournoi in enumerate(tournois, start=1):
            tournoi_id = tournoi.get('id', 'ID non disponible')
            print(f"{index}. ID: {tournoi_id}, Nom: {tournoi['nom']}")

        choix = int(input("➡️  Entrez le numéro du tournoi : ")) - 1
        if 0 <= choix < len(tournois):
            tournoi = tournois[choix]
            return Tournament.charger_tournoi(
                os.path.join(self.dossier_db, f"{tournoi['nom'].lower().replace(' ', '_')}.json"), tournoi['nom'])
        else:
            print("⛔ Choix invalide.")
            return None

    def choisir_joueur(self):
        """Liste les joueurs et demande à l'utilisateur de choisir un joueur par numéro."""
        if not self.tournoi or not self.tournoi.joueurs:
            print("⛔ Aucun joueur trouvé.")
            return None

        print("\n📋 Liste des joueurs :")
        for index, joueur in enumerate(self.tournoi.joueurs, start=1):
            print(f"{index}. {joueur.prenom} {joueur.nom} (ID: {joueur.identifiant_echecs})")

        choix = int(input("➡️  Entrez le numéro du joueur : ")) - 1
        if 0 <= choix < len(self.tournoi.joueurs):
            return self.tournoi.joueurs[choix]
        else:
            print("⛔ Choix invalide.")
            return None

# Si ce fichier est exécuté directement, lancer le menu CLI
if __name__ == "__main__":
    cli = CLI()
    cli.afficher_menu_principal()