# Un deuxième fichier graphique.py (qui importe la bibliothèque tkinter et le fichier book.py).
from operator import itemgetter
from tkinter import Tk, messagebox, NO, CENTER, ttk, Menu, Frame, filedialog
from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfile
from book import Livre, Bibliotheque


class InterfaceGraphique:
    """
La classe interface graphique est la fenêtre de l'interface graphique. Elle contient les méthodes en lien avec
l'affichage des données par le bias de Tkinter.
    """

    def __init__(self):
        """
        Constructeur de la classe Interface Graphique.
        """
        self.tableau_a_afficher = None
        self.bibliotheque_interface = Bibliotheque()
        self.fenetre = Tk()
        self.fenetre.geometry("820x900")
        self.fenetre.title("Gestion de livres")

        # Création des différents élément graphique
        self.creation_menu_barre()
        self.tableau_deja_affiche = False
        #self.affichage_liste_dans_tableau()  # Pour avoir un tableau vide en commencant

        self.fenetre.mainloop()

    def creation_menu_barre(self):
        """
        Cette fonction crée le menu en barre qui est affiché dans la barre d'outils.
        """
        # Début du menu
        menu_barre = Menu(self.fenetre)

        # Menu Fichier
        menu_fichier = Menu(menu_barre, tearoff=0)
        menu_fichier.add_command(label="Charger", command=self.charger)
        menu_fichier.add_command(label="Sauvegarder", command=self.sauvegarder)
        menu_fichier.add_command(label="Effacer", command=self.effacer)
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Quitter", command=self.fenetre.quit)
        menu_barre.add_cascade(label="Fichier", menu=menu_fichier)

        # Menu Trier
        menu_trier = Menu(menu_barre, tearoff=0)
        menu_trier.add_command(label="Cote", command=self.trier_cote)
        menu_trier.add_command(label="Titre", command=self.trier_titre)
        menu_trier.add_command(label="Page", command=self.trier_page)
        menu_trier.add_command(label="Prix", command=self.trier_prix)
        menu_barre.add_cascade(label="Trier", menu=menu_trier)

        # Menu Rechercher
        menu_rechercher = Menu(menu_barre, tearoff=0)
        menu_rechercher.add_command(label="Cote", command=self.rechercher_cote)
        menu_rechercher.add_command(label="Titre", command=self.rechercher_titre)
        menu_barre.add_cascade(label="Rechercher", menu=menu_rechercher)

        # Menu Aide
        menu_aide = Menu(menu_barre, tearoff=0)
        menu_aide.add_command(label="À propos", command=self.aide)
        menu_barre.add_cascade(label="Aide", menu=menu_aide)

        # Ajout du menu barre à l'interface
        self.fenetre.config(menu=menu_barre)

    def affichage_liste_dans_tableau(self):
        """
        Cette fonction prend une liste de livre et l'affiche dans le tableau de l'interface graphique

        :param liste_a_afficher: (list) Il s'agit d'une liste de 4 chaines de caractères représentant. Ces chaines 
        sont la cote, le titre, le nombre de pages et le prix.  
        """
        if self.tableau_deja_affiche:
            self.effacer()  # Afin d'enlever le tableau déjà afficher
        self.cadre = Frame(self.fenetre)  # Ça devrait être définit dans __init__ mais je ne sais pas comment faire sans
        # que ça bogue
        self.cadre.pack()
        self.tableau_a_afficher = ttk.Treeview(self.cadre, height=30)  # Ça aussi ça devrait être définit dans __init__
        self.tableau_a_afficher['columns'] = ("cote", "titre", "nombre de pages", "prix")
        self.tableau_a_afficher.pack()
        col_dict = {"cote": self.trier_cote, "titre": self.trier_titre, "nombre de pages": self.trier_page, "prix": self.trier_prix}
        self.tableau_a_afficher.column("#0", width=0, stretch=NO)  # Pour coller la colonne à droite
        self.tableau_a_afficher.heading("#0", text="", anchor=CENTER)
        for col in col_dict.keys():
            self.tableau_a_afficher.column(col, anchor=CENTER)
            self.tableau_a_afficher.heading(col, text=col, anchor=CENTER, command=col_dict[col])
        #self.tableau_a_afficher.column("cote", anchor=CENTER)
        #self.tableau_a_afficher.column("titre", anchor=CENTER)
        #self.tableau_a_afficher.column("nombre de pages", anchor=CENTER)
        #self.tableau_a_afficher.column("prix", anchor=CENTER)

        # Entête du tableau
        #self.tableau_a_afficher.heading("#0", text="", anchor=CENTER)
        #self.tableau_a_afficher.heading("cote", text="Cote", anchor=CENTER)
        #self.tableau_a_afficher.heading("titre", text="Titre", anchor=CENTER)
        #self.tableau_a_afficher.heading("nombre de pages", text="Nombre de pages", anchor=CENTER)
        #self.tableau_a_afficher.heading("prix", text="Prix ($)", anchor=CENTER)

        self.tableau_deja_affiche = True
        # Remplissage du tableau
        i = 0
        for livre in self.bibliotheque_interface.liste_des_livre:
            i += 1
            self.tableau_a_afficher.insert(parent='', index='end', iid=str(i), text='',
                                           values=livre)

    def charger(self):
        """Cette fonction sert à ouvrir un boite de dialogue pour aller selectionner un fichier à ouvrir. Le fichier
        selectionné et traiter et affiché sous forme de tableau dans l'interface graphique.
        """
        nom_fichier = filedialog.askopenfilename(title='Ouvrir le fichier',filetypes=[('txt', '*.txt')])
        try:
            self.bibliotheque_interface.creation_liste_a_partir_un_fichier(nom_fichier)
        except (IOError,Exception) as error:
            messagebox.showerror("Erreur", error)
        self.affichage_liste_dans_tableau()

    def sauvegarder(self):
        """Cette fonction sert à créer un fichier à partir de la liste dans la bibliotheque.
        :return:
        """
        fichier_sauvergarde = asksaveasfile(initialfile='texte.txt', defaultextension=".txt", filetypes=[("All Files", "*.*"),
                                                                                          ("Text Documents", "*.txt")])
        for line in self.bibliotheque_interface.liste_des_livre:
            fichier_sauvergarde.write("%s\n" % ",".join(line))
        fichier_sauvergarde.close()

        print('Sauvegarder')

    def effacer(self):
        """Cette fonction sert à effacer le tableau qui est affiché dans l'interface graphique.
        :return:
        """
        self.cadre.destroy()

        # TODO La liste doit être effacer de la bibliotheque mais la bibliotheque semble rester entière lorsqu'un
        #  fichier est chargé par la fonction charger(). Possiblement par la fonction création d'une liste à partir d'un
        #  fichier

    def aide(self):
        """Cette fonction affiche une section à propos contenant des informations sur le programme.
        :return:
        """
        info = """ Nom du programme: 
        Gestion de livre
        
        Version: 
        1.0
        
        Réalisé par : 
        Alexandre Dubeau et Gabriel Lecompte 
        """
        messagebox.showinfo(title="À propos", message=info)

    def trier(self, information_de_tri):
        """Cette fonction trie la liste de livre afficher selon le critère passé dans la fonction (ex. La cote du livre).
        :param information_de_tri: (string) La valeur selon laquel on veut trier. Il s'agit d'une chaine de caractère.
        Ses valeurs possibles sont 'cote', 'titre', 'page' et 'prix'.
        :return: À déterminer
        """
        try:
            liste_trie = sorted(self.bibliotheque_interface.liste_des_livre, key=itemgetter(self.tableau_a_afficher['columns'].index(information_de_tri)))
        except RuntimeError:
            messagebox.showerror("Erreur", "La liste fourni est invalide")

        # TODO: Il doit y avoir une gestion des erreurs pour la précondition suivante: Les valeurs doivent faire partie
        #  des valeurs possibles.
        self.bibliotheque_interface.liste_des_livre = liste_trie
        self.affichage_liste_dans_tableau()
        print(f'Trier par {information_de_tri}')

    def trier_cote(self):
        self.trier("cote")

    def trier_titre(self):
        self.trier("titre")

    def trier_page(self):
        self.trier("nombre de pages")

    def trier_prix(self):
        self.trier("prix")

    def rechercher(self, information_de_recherche):
        """ Cette fonction ouvrir un boite de dialogue pour que l'utilisateur entre l'information qu'il cherche.
        :param information_de_recherche: (str). Indique quel information sera utilisée pour la recherche. Les valeurs
        possibles sont "cote" et "titre".
        :return:
        """
        recherche = askstring(("Recherche par " + information_de_recherche), ("Veuillez entrer votre "
                                                                              + information_de_recherche))

        #  TODO Compléter cette fonction
        #  TODO S'assurer de la gestion des exceptions

    def rechercher_cote(self):
        self.rechercher("cote")

    def rechercher_titre(self):
        self.rechercher("titre")


if __name__ == '__main__':
    application = InterfaceGraphique()
