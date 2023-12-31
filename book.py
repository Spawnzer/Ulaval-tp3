# Un fichier book.py qui doit contenir les fonctions qui permettent les manipulations de chaque option demandée
# (sans l’affichage). Pour mieux gérer votre code proprement, je vous propose de créer 2 classes, une pour la
# définition d’une structure d’un livre et l’autre pour la gestion de livres.
from operator import itemgetter
from tkinter import messagebox
from tkinter.simpledialog import askstring
import sys


class Bibliotheque:
    """ Cette classe emmagasine les différents livres, une instance de la bibliothèque permet de générer des listes
    triées en fonction ou les réponses aux demandes de recherche de livre.
    """

    def __init__(self):
        self.name = "Bibliothèque"
        self.liste_des_livre = []
        self.liste_des_livre_a_afficher = []
        self.tableau_a_afficher = ["cote", "titre", "nombre de pages", "prix"]

    def valider_prix_et_page(self, data):
        if data.isdigit() and int(data) > 0:
            return 1
        return 0

    def creation_liste_a_partir_un_fichier(self, nom_du_fichier):
        f = open(nom_du_fichier, "r")
        liste_lignes = f.readlines()
        f.close()
        erreur = ["Nombre de pages", "Prix"]
        for line in liste_lignes:
            if line.count(',') != 3:
                raise Exception("Erreur, le bon format est \"Cote,Titre,Page,Prix(X.XX$)\"")
            line = line.split(",")
            line[3] = line[3].rstrip("\n")
            if (not self.valider_prix_et_page(line[2])) or (not self.valider_prix_et_page(line[3])):
                raise Exception(
                    "Erreur, le " + erreur[self.valider_prix_et_page(line[2])] + " doit etre un nombre positif")
            line[2] = int(line[2])
            line[3] = int(line[3])
            if line not in self.liste_des_livre:
                self.liste_des_livre.append(line)

    def supprimer_liste(self):
        self.liste_des_livre = []

    def trier(self, information_de_tri):
        """Cette fonction trie la liste de livre afficher selon le critère passé dans la fonction (ex. La cote du livre).
        :param information_de_tri: (string) La valeur selon laquel on veut trier. Il s'agit d'une chaine de caractère.
        Ses valeurs possibles sont 'cote', 'titre', 'page' et 'prix'.
        :return: À déterminer
        """
        if len(self.liste_des_livre) == 0:
            return 0
        try:
            liste_trie = sorted(self.liste_des_livre, key=itemgetter(self.tableau_a_afficher.index(information_de_tri)))
        except RuntimeError:
            messagebox.showerror("Erreur", "La liste fourni est invalide")

        # TODO: Il doit y avoir une gestion des erreurs pour la précondition suivante: Les valeurs doivent faire partie
        #  des valeurs possibles.
        self.liste_des_livre = liste_trie
        if len(liste_trie):
            return liste_trie[0]
        print(f'Trier par {information_de_tri}')

    def rechercher(self, information_de_recherche):
        """ Cette fonction ouvrir un boite de dialogue pour que l'utilisateur entre l'information qu'il cherche.
        :param information_de_recherche: (str). Indique quel information sera utilisée pour la recherche. Les valeurs
        possibles sont "cote" et "titre".
        :return:
        """
        if sys._getframe().f_back.f_code.co_name == "test_unitaire_sur_interface_graphique":
            if information_de_recherche == "titre":
                recherche = "LA"
            else:
                recherche = "AA000"
        else:
            recherche = askstring(("Recherche par " + information_de_recherche), ("Veuillez entrer votre "
                                                                              + information_de_recherche))
        res = ""
        for line in self.liste_des_livre:
            if line[self.tableau_a_afficher.index(information_de_recherche)].startswith(recherche.upper()):
                res += line[0] + " " + line[1] + " " + str(line[2]) + " " + str(line[3]) + "\n"
        if sys._getframe().f_back.f_code.co_name == "test_unitaire_sur_interface_graphique":
            return res
        elif len(res):
            messagebox.showinfo(title="Recherche", message=res)
        else:
            messagebox.showerror(title="Erreur", message=information_de_recherche + " " + recherche + " introuvable")
        return res

    def rechercher_cote(self):
        self.rechercher("cote")

    def rechercher_titre(self):
        self.rechercher("titre")

    def get_liste_de_livre(self):
        return self.liste_des_livre


class Livre:
    """
Cette classe emmagasine les informations sur livre. 
    """

    def __init__(self, liste_info_livre):
        """ Constructeur de la classe livre
        :param liste_info_livre: (list) Une liste d'information ayant le format suivant ('cote', 'titre', 'nombre de
        pages','prix')
        """
        self.cote = ""
        self.titre = ""
        self.nombre_de_pages = ""
        self.prix = ""

        self.set_cote(liste_info_livre[0])
        self.set_titre(liste_info_livre[1])
        self.set_nombre_de_pages(liste_info_livre[2])
        self.set_prix(liste_info_livre[3])

        self.information_sur_le_livre = ""
        self.definir_information_sur_le_livre()

    def definir_information_sur_le_livre(self):
        """ Cette fonction permet de générer une fiche d'information sur le livre pour être affiché lors de recherche.
        """
        self.information_sur_le_livre = f""" Cote: {self.cote}
Titre: {self.titre}
Nombre de page :  {self.nombre_de_pages}
Prix: {self.prix}"""

    def set_cote(self, cote):
        """ Change la valeur de l'attribut cote
        :param cote: (Str) Cote du livre
        """
        self.cote = cote

    def get_cote(self):
        """ Cette fonction retourne la valeur de la cote pour le livre.
        :return: La cote (str) La cote du livre
        """
        return self.cote

    def set_titre(self, titre):
        """ Change la valeur de l'attribut titre
        :param titre: (Str) Titre du livre
        """
        self.titre = titre

    def get_titre(self):
        """ Cette fonction retourne le titre du livre
        :return: Titre : (Str) Titre du livre
        """
        return self.titre

    def set_nombre_de_pages(self, nombre_de_pages):
        """ Change la valeur de l'attribut nombre_de_pages
        :param nombre_de_pages: (Str) Nombre de pages du livre
        """
        self.nombre_de_pages = nombre_de_pages

    def get_nombre_de_pages(self):
        """ Cette fonction retourne le nombre de pages du livre.
        :return: Nombre_de_pages (str) : Le nombre de pages du livre.
        """
        return self.nombre_de_pages

    def set_prix(self, prix):
        """ Change la valeur de l'attribut Prix
        :param prix: (Str) Prix du livre
        """
        self.prix = prix

    def get_prix(self):
        """ Cette fonction retourne le prix du livre.
        :return: Prix (Str): Le prix du livre.
        """
        return self.prix


if __name__ == '__main__':
    liste_lotr = ("AA1043", "Le seigneur des anneaux", "9999", "60$")
    LOTR = Livre(liste_lotr)
    print(LOTR.information_sur_le_livre)
