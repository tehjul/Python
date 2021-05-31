import render
from math import sqrt


def read(filename):
    file = open(filename)

    dim = int(file.readline())
    grid = []

    for i in range(dim ** 2):
        line = file.readline().split('\n')[0].split(' ')
        for j in range(dim ** 2):
            if int(line[j]) != 0:
                grid.append((i, j, int(line[j])))

    file.close()

    return dim, grid


###################################################################################
# Question 1
###################################################################################

##########################################################
# Créé une triple grille vide d'ordre n avec les valeurs #
# '?' en index 0 et 'green' en index 1                   #
# de la forme grille[ligne][colonne][valeur , couleur]  #
##########################################################

def init_grille(n):
    grille = []
    temp = []
    n = n ** 2

    for i in range(n):  # ligne
        for j in range(n):  # colonne
            temp.append(['?', "green"])
        grille.append(temp)
        temp = []

    return grille


###################################################################################
# Question 2                  
###################################################################################

####################################################
# Initialise une grille vide avec un               #
# fichier comme paramètre contenant l'ordre        #
# et les valeurs préfixées                         #
# Retourne l'ordre et la grille avec valeurs fixes #
####################################################

def creer_grille(fichier):
    n, valeurs = read(fichier)
    grille = init_grille(n)
    boucle = len(valeurs)
    for v in range(boucle):
        x = valeurs[v][0]
        y = valeurs[v][1]
        z = valeurs[v][2]
        grille[x][y][0] = z
        grille[x][y][1] = "red"

    return n, grille


###################################################################################
# Question 3        Représentation graphique d'une grille de sudoku
###################################################################################

########################################################
#  Ecrit les valeurs de la grille passée en paramètre  #
#  Dans le module render et affiche la grille          #
########################################################

def affiche_sudoku(grille):
    n = int(sqrt(len(grille)))
    boucle = n ** 2
    render.draw_sudoku_grid(n)
    for i in range(boucle):
        for j in range(boucle):
            z = grille[i][j][0]
            c = grille[i][j][1]
            render.write(i, j, z, c)


###################################################################################
# Question 4                     Jouer au Sudoku
###################################################################################

#########################
# Fonctions secondaires #
#########################

def lecture_cases_restantes(grille):
    boucle = len(grille)
    res = 0
    for i in range(boucle):
        for j in range(boucle):
            if grille[i][j][1] == 'green':
                res = res + 1
    return res


def est_chiffre(c):
    if c <= '9' and c >= '0':
        return True
    else:
        return False


def est_nombre(chaine):
    for c in chaine:
        if not est_chiffre(c):
            return False
    return True


def choix_ligne(grille, ligne):
    n = len(grille)
    temp = []
    for i in range(n):
        x = grille[ligne][i][0]
        if x != '?':
            temp.append(x)
    return temp


def choix_colonne(grille, colonne):
    n = len(grille)
    temp = []
    for i in range(n):
        y = grille[i][colonne][0]
        if y != '?':
            temp.append(y)
    return temp


def pos_ligne_carre(ligne, n):
    for i in range(n):
        if ligne >= n * i and ligne < n * (i + 1):
            return n * i


def pos_colonne_carre(colonne, n):
    for i in range(n):
        if colonne >= n * i and colonne < n * (i + 1):
            return n * i


def choix_carre(grille, ligne, colonne):
    n = int(sqrt(len(grille)))
    depart_ligne = pos_ligne_carre(ligne, n)
    depart_colonne = pos_colonne_carre(colonne, n)
    temp = []
    for i in range(depart_ligne, depart_ligne + n):
        for j in range(depart_colonne, depart_colonne + n):
            x = grille[i][j][0]
            if x != '?':
                temp.append(x)
    return temp


def liste_nombres_jouables(n):
    temp = []
    for i in range(n ** 2 + 1):
        temp.append(i)
    return temp


def est_dans_liste(liste, n):
    for i in liste:
        if i == n:
            return True
    return False


def liste_nombres_non_jouables(grille, ligne, colonne):
    n = int(sqrt(len(grille)))
    res = []
    lin = choix_ligne(grille, ligne)
    col = choix_colonne(grille, colonne)
    car = choix_carre(grille, ligne, colonne)
    for c in lin:
        res.append(c)
    for d in col:
        res.append(d)
    for e in car:
        if not est_dans_liste(res, e):
            res.append(e)
    return res


def affiche_nb_possibles(liste):
    print('les valeurs possibles sont :', end=' ')
    for c in liste:
        print(c, end=' ')
    print('')


###########################
##  Fonctions primaires  ##
###########################

# retourne un nom de fichier
def demande_fichier():
    fichier = 'sudoku_9_9_1.txt'
    temp = input('Entrez le nom du fichier (entrée pour prendre le fichier par défaut) : ')
    if temp == "":
        return fichier
    else:
        return temp


# Affiche les cases restantes à remplir
def afficher_cases_restantes(grille):
    res = lecture_cases_restantes(grille)
    print('Il reste', res, 'cases à remplir')


# Demande un numéro de ligne à l'utilisateur
def demande_ligne(n):
    y = n ** 2
    while True:
        ligne = input('Entrez un numéro de ligne ou entrée pour annuler : ')
        if ligne == '':
            return ligne
        elif est_nombre(ligne):
            ligne = int(ligne)
            if ligne >= 0 and ligne < y:
                return ligne
            else:
                print('Le numéro de ligne n’est pas correct. Il doit être entre 0 et', y - 1)
        else:
            print('Il faut entrer un nombre entier')


# Demande un numéro de colonne à l'utilisateur                
def demande_colonne(n):
    y = n ** 2
    while True:
        colonne = input('Entrez un numéro de colonne ou entrée pour annuler : ')
        if colonne == '':
            return colonne
        elif est_nombre(colonne):
            colonne = int(colonne)
            if colonne >= 0 and colonne < y:
                return colonne
            else:
                print('Le numéro de colonne n’est pas correct. Il doit être entre 0 et', y - 1)
        else:
            print('Il faut entrer un nombre entier')


# Teste si une case est modifiable à partir d'un numéro de ligne et colonne
def est_case_modifiable(grille, ligne, colonne):
    if grille[ligne][colonne][1] == 'red':
        return False
    return True


# Affiche les nombres possibles par comparaison entre la liste entière des nombres jouables et la liste des nombres joués
def nb_possibles(grille, ligne, colonne):
    n = int(sqrt(len(grille)))
    liste1 = liste_nombres_non_jouables(grille, ligne, colonne)
    liste2 = liste_nombres_jouables(n)
    temp = []
    for c in liste2:
        if not est_dans_liste(liste1, c):
            temp.append(c)
    return temp


# Demande un numéro à jouer à l'utilisateur, affiche les choix possibles
def demande_nb(liste):
    while True:
        affiche_nb_possibles(liste)
        res = input('Entrez une valeur possible ou appuyez sur entrée pour annuler le coup : ')
        if res == '':
            return res
        else:
            if est_nombre(res):
                res = int(res)
                if est_dans_liste(liste, res):
                    return res
                else:
                    print('Erreur! Veuillez entrez un nombre possible')

            else:
                print('Erreur! Veuillez entrez un entier')


def maj_grille(grille, ligne, colonne, res):
    if res == 0 or res == '?':
        render.write(ligne, colonne, '?', 'green')
        grille[ligne][colonne][0] = '?'
        grille[ligne][colonne][1] = 'green'
    else:
        render.write(ligne, colonne, res, 'blue')
        grille[ligne][colonne][0] = res
        grille[ligne][colonne][1] = 'blue'


#############################
#############################
###  Fonction principale  ###
#############################
#############################

def jouer_sudoku():
    historique = []
    fichier = demande_fichier()
    n, grille = creer_grille(fichier)
    affiche_sudoku(grille)
    j_ou_r = demande_jouer_resoude()
    if j_ou_r == 'R':
        cellules_vides = liste_cellules_vides(grille)
        resolveur_recursif(grille, cellules_vides)
        print("Félicitations, vous n'avez pas gagné, c'est l'ordinateur qui a tout fait ;-)")
        render.wait_quit()
        return 0
    else:
        while lecture_cases_restantes(grille) > 0:
            while len(historique) > 0 and not hist != 'O':
                ligne, colonne, ancien_coup = lecture_derniere_valeur_historique(historique)
                maj_grille(grille, ligne, colonne, ancien_coup)
                historique.pop()
                if len(historique) > 0:
                    afficher_cases_restantes(grille)
                    hist = demande_dernier_coup(historique)
            afficher_cases_restantes(grille)
            ligne = demande_ligne(n)
            if ligne != '':
                colonne = demande_colonne(n)
                if colonne != '':
                    if est_case_modifiable(grille, ligne, colonne):
                        nb_poss = nb_possibles(grille, ligne, colonne)
                        res = demande_nb(nb_poss)
                        if res != '':
                            if res == 0:
                                coup = [ligne, colonne, grille[ligne][colonne][0], '?']
                                maj_grille(grille, ligne, colonne, res)
                                historique.append(coup)
                            else:
                                coup = [ligne, colonne, grille[ligne][colonne][0], res]
                                maj_grille(grille, ligne, colonne, res)
                                historique.append(coup)
                            hist = demande_dernier_coup(historique)
                    else:
                        print('Il n\'est pas possible de modifier cette case')

        print('Félicitations, vous avez gagné !')
        render.wait_quit()
        return 0


###################################################################################
# Question 5                 Mise en place d'un historique
###################################################################################

#########################
# Fonctions secondaires #
#########################

def affiche_dernier_coup(historique):
    ligne = historique[-1][0]
    colonne = historique[-1][1]
    ancien_coup = historique[-1][2]
    nouveau_coup = historique[-1][3]
    print('Dernier coup joué = (', ligne, ',', colonne, ') :', ancien_coup, '-->', nouveau_coup)


def dernier_coup(historique):
    while True:
        res = input('Voulez-vous l\'annuler ? [O]ui / [N]on (ou entrée) : ')
        if res == 'O' or res == 'N' or res == '':
            return res
        else:
            print('Veuillez répondre \'O\' ou \'N\' (ou entrée)')


###########################
##  Fonctions primaires  ##
###########################

def demande_dernier_coup(historique):
    affiche_dernier_coup(historique)
    return dernier_coup(historique)


def lecture_derniere_valeur_historique(historique):
    ligne = historique[-1][0]
    colonne = historique[-1][1]
    ancien_coup = historique[-1][2]
    return ligne, colonne, ancien_coup


###################################################################################
# Question 6                     Résolution automatique
###################################################################################

def resolveur_recursif(grille, liste_cellules_vides):
    n = len(grille)
    if len(liste_cellules_vides) == 0:  # si longueur de la liste des cellules vides est 0 c'est qu'on est à la fin
        return True

    ligne = liste_cellules_vides[0][0]
    colonne = liste_cellules_vides[0][1]

    for choix in range(1, n + 1):  # on teste tous les choix possible pour une grille d'ordre n
        if est_choix_possible(grille, ligne, colonne,
                              choix):  # on protège des essais 'inutiles' avec cette fonction
            maj_grille(grille, ligne, colonne, choix)  # on met à jour la grille
            if resolveur_recursif(grille,
                                  liste_cellules_vides[1:]):  # si cette condition est vrai, c'est qu'on est à la fin
                return True  # Du coup, renvoie True en cascade jusqu'à la première occurence
            maj_grille(grille, ligne, colonne,
                       0)  # Si la condition précédente n'est pas remplie, on efface la case pour ne pas affecter les choix suivants
    # ici on retourne au début de la boucle 'for' pour tester le choix suivant

    # cette dernière ligne (#389) a été inspirée d'internet, ma fonction fonctionnait jusqu'à
    # un certain point mais je ne comprennais pas pourquoi ça n'allait pas plus loin.
    # je n'ai pas de source particulière à citer, mais c'est en voyant plusieurs fois
    # cette réassignation à 0 dans différentes solutions qui m'a permit de comprendre.
    # cet article m'a beaucoup aidé à comprendre comment le backtracking fonctionnait :
    # https://medium.com/@ekapope.v/learning-recursive-algorithm-with-sudoku-solver-in-python-345623de98ae

    return False  # dans le cas ou on ne peut pas résoudre la grille


def liste_cellules_vides(grille):
    boucle = len(grille)
    res = []
    for ligne in range(boucle):
        for colonne in range(boucle):
            if est_case_modifiable(grille, ligne, colonne):
                res.append([ligne, colonne])
    return res


def est_choix_possible(grille, ligne, colonne, choix):
    res = nb_possibles(grille, ligne, colonne)
    if est_dans_liste(res, choix):
        return True
    return False


def demande_jouer_resoude():
    while True:
        res = input('Voulez-vous [J]ouer ou [R]ésoudre ? ')
        if res == 'J' or res == 'R':
            return res
        else:
            print('Erreur! Veuillez saisir \'J\' ou \'R\'')


jouer_sudoku()
