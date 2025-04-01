import json
import os
from models.tournament import Tournament
from models.player import Player

def test_sauvegarder_tournoi():
    # Créer un tournoi et ajouter des joueurs
    tournoi = Tournament("Test Tournoi", "Paris", "2023-01-01", "2023-01-02")
    joueur1 = Player("Doe", "John", "1990-01-01", "12345")
    joueur2 = Player("Smith", "Jane", "1992-02-02", "67890")
    tournoi.ajouter_joueur(joueur1)
    tournoi.ajouter_joueur(joueur2)

    # Créer le répertoire de sauvegarde s'il n'existe pas
    fichier = "data/test_tournoi.json"
    os.makedirs(os.path.dirname(fichier), exist_ok=True)

    # Sauvegarder le tournoi
    tournoi.sauvegarder_tournoi(fichier)

    # Vérifier que le fichier a été créé
    assert os.path.exists(fichier), "Le fichier de sauvegarde n'a pas été créé."

    # Charger les données du fichier et vérifier le contenu
    with open(fichier, 'r') as f:
        data = json.load(f)
        assert data["nom"] == "Test Tournoi", "Le nom du tournoi est incorrect."
        assert data["lieu"] == "Paris", "Le lieu du tournoi est incorrect."
        assert data["date_debut"] == "2023-01-01", "La date de début est incorrecte."
        assert data["date_fin"] == "2023-01-02", "La date de fin est incorrecte."
        assert len(data["joueurs"]) == 2, "Le nombre de joueurs est incorrect."
        assert data["joueurs"][0]["nom"] == "Doe", "Le nom du premier joueur est incorrect."
        assert data["joueurs"][1]["nom"] == "Smith", "Le nom du deuxième joueur est incorrect."

    # Nettoyer le fichier de test
    os.remove(fichier)
    print("Test de sauvegarde réussi.")

# Exécuter le test
test_sauvegarder_tournoi()