# Un troisième fichier uTest.py qui contiendra les tests unitaires.

import graphique
import book
import tempfile
import os
from unittest.mock import patch


def creation_fichier_temporaire(texte, bibliotheque):
    fichier_temporaire = tempfile.NamedTemporaryFile()
    fichier_temporaire.write(texte)
    fichier_temporaire.seek(os.SEEK_SET)
    nom_fichier_temporaire = str(fichier_temporaire.name)
    bibliotheque.creation_liste_a_partir_un_fichier(nom_fichier_temporaire)
    fichier_temporaire.close()


def test_unitaire_sur_les_bibliotheques():
    """
Cette fonction réalise les tests unitaires en lien avec la classe bibliothèque.
    :return:
    """
    # Tests unitaires sur la fonction qui permet de vider la liste
    biblio_test = book.Bibliotheque()
    biblio_test.creation_liste_a_partir_un_fichier("livre1.txt")
    biblio_test.supprimer_liste()
    assert biblio_test.get_liste_des_livres() == []


def test_unitaire_sur_les_livres():
    """
Cette fonction réalise les tests unitaires en lien avec la classe livre.
    :return:
    """
    # Tests unitaires sur la fonction qui permet le chargement du livre
    biblio_test = book.Bibliotheque()
    texte_normal = b"""AA000,TITRE PAR DEFAULT,100,30
BV378,LA VIE DEVANT SOI,1640,90"""
    texte_info_manquante = b"""AA000,TITRE PAR DEFAULT,100
BV378,LA VIE DEVANT SOI,1640,90"""
    texte_page_non_numerique = b"""AA000,TITRE PAR DEFAULT,100,a
BV378,LA VIE DEVANT SOI,1640,r4"""
    # Test fonctionnement normal de la création d'une liste
    creation_fichier_temporaire(texte_normal, biblio_test)
    assert biblio_test.get_liste_de_livre() == [['AA000', 'TITRE PAR DEFAULT', '100', '30'],
                                                ['BV378', 'LA VIE DEVANT SOI',
                                                 '1640', '90']]
    # Test avec des informations manquantes
    test_text_reussi_info_manquant = True
    try:
        creation_fichier_temporaire(texte_info_manquante, biblio_test)
    except:
        test_text_reussi_info_manquant = False

    assert test_text_reussi_info_manquant == False

    # Test avec un nombre de page non numérique
    test_text_reussi_page_non_numerique = True
    try:
        creation_fichier_temporaire(texte_page_non_numerique, biblio_test)
    except:
        test_text_reussi_page_non_numerique = False
    assert test_text_reussi_page_non_numerique == False


@patch('test.input')
def test_unitaire_sur_interface_graphique(mock_input):
    """
Cette fonction réalise les tests unitaires en lien avec la classe interface_graphique.
    :return:
    """
    # Tests unitaires sur la fonction qui permets le tri par information passer
    biblio_test = book.Bibliotheque()
    biblio_test.liste_des_livre = [['AA000', 'TITRE PAR DEFAULT', '100', '30'],
                                   ['BV378', 'LA VIE DEVANT SOI', '1640', '90']]
    assert biblio_test.trier("cote") == ['AA000', 'TITRE PAR DEFAULT', '100', '30']
    assert biblio_test.trier("titre") == ['BV378', 'LA VIE DEVANT SOI', '1640', '90']
    assert biblio_test.trier("nombre de pages") == ['AA000', 'TITRE PAR DEFAULT', '100', '30']
    assert biblio_test.trier("prix") == ['AA000', 'TITRE PAR DEFAULT', '100', '30']

    biblio_test.liste_des_livre = []
    assert biblio_test.trier("cote") == 0
    assert biblio_test.trier("titre") == 0
    assert biblio_test.trier("nombre de pages") == 0
    assert biblio_test.trier("prix") == 0

    # Tests unitaires sur la fonction qui permets la recherche par information passer
    biblio_test.liste_des_livre = [['AA000', 'TITRE PAR DEFAULT', '100', '30'],
                                   ['BV378', 'LA VIE DEVANT SOI', '1640', '90'],
                                   ['ZV234', 'LA LA LA LA', '43', '4']]
    mock_input.return_value = "la"
    assert biblio_test.rechercher("titre") == "BV378 LA VIE DEVANT SOI 1640 90\nZV234 LA LA LA LA 43 4\n"
    assert biblio_test.rechercher("cote") == "AA000 TITRE PAR DEFAULT 100 30\n"

    biblio_test.liste_des_livre = []
    assert biblio_test.rechercher("titre") == ""
    assert biblio_test.rechercher("cote") == ""

    pass


if __name__ == "__main__":
    # test_unitaire_sur_les_livres()
    # test_unitaire_sur_les_bibliotheques()
    test_unitaire_sur_interface_graphique()
