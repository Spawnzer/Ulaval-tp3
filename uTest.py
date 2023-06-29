# Un troisième fichier uTest.py qui contiendra les tests unitaires.

import graphique
from book import *


def test_unitaire_sur_les_bibliotheques():
    """
Cette fonction réalise les test unitaire en lien avec la classe bibliothèque.
    :return:
    """
    pass


def test_unitaire_sur_les_livres():
    """
Cette fonction réalise les test unitaire en lien avec la classe livre.
    :return:
    """
    pass


def test_unitaire_sur_interface_graphique():
    """
Cette fonction réalise les test unitaire en lien avec la classe interface_graphique.
    :return:
    """
    pass


if __name__ == "__main__":
    test_unitaire_sur_les_livres()
    test_unitaire_sur_les_bibliotheques()
    test_unitaire_sur_interface_graphique()


L = Bibliotheque()
L.creation_liste_a_partir_un_fichier("texte.txt")

