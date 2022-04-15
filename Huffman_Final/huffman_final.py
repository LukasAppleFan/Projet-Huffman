# Projet Huffman

# Variables pour les fichiers textes
testpy = "testpy.txt"
texthuffman = "texthuffman.txt"
texte_retour_ligne = "texte_retour_ligne.txt"
texte_un_car = "texte_un_car.txt"
grostexte = "grostexte.txt"
demofile = "demofile.txt"

# Structure du dict :
dict_exemple = {'a': 21,
                'b': 15,
                'c': 30,
                'd': 9,
                'e': 5,
                'f': 7}


# Fonctions pour avoir les occurences des caractères sous forme de dictionnaire

def dictionnaire(fichier):
    """retourne un dictionnaire contenant toutes les lettres présentes
    dans un fichier (specifier en str avec '.txt' à la fin), et leur
    nombre d'occurences à chacune, pour fonctionner l'algorithme et le
    fichier doivent être dans le même dossier"""
    with open(fichier, "r", encoding='utf-8') as txt:
        global texte # Pour la décompression
        texte = txt.read()

    dictionnaire1 = {}
    for lettre in texte:
        if lettre not in dictionnaire1:
            dictionnaire1[lettre] = 0
        if lettre in dictionnaire1:
            dictionnaire1[lettre] += 1

    return dictionnaire1


assert dictionnaire(testpy) == {'T': 1, 'e': 2, 's': 1, 't': 2, ' ': 1, 'p': 1, 'r': 1, 'o': 1, 'j': 1}
assert dictionnaire(texte_retour_ligne) == {'L': 2, 'e': 29, ' ': 35, 'c': 8, 'o': 11, 'd': 10, 'a': 14, 'g': 4, 'H': 3, 'u': 13, 'f': 7, 'm': 7, 'n': 15, 's': 11, 't': 6, 'l': 7, 'r': 14, 'i': 7, 'h': 2, 'p': 6, 'é': 2, '.': 2, '\n': 3, 'à': 1, 'v': 1, 'b': 2, 'y': 1, '(': 1, 'x': 1, 'è': 1, ')': 1}
assert dictionnaire(texte_un_car) == {'A': 1}


def dictionnaire_car(car):
    """ str -> dict
    Retourne un dictionnaire contenant les occurences
    de chaque caractère de la chaîne de caractère.
    """
    dico = {}
    
    for lettre in car:
        if lettre not in dico:
            dico[lettre] = 0
        if lettre in dico:
            dico[lettre] += 1

    return dico

assert dictionnaire_car("CACHE") == {'C': 2, 'A': 1, 'H': 1, 'E': 1}
assert dictionnaire_car("huffman") == {'h': 1, 'u': 1, 'f': 2, 'm': 1, 'a': 1, 'n': 1}
assert dictionnaire_car("A") == {'A': 1}


class Noeud:
    """ un noeud d'un arbre binaire"""
    def __init__(self, g, v, o, d):
        self.gauche = g
        self.valeur = v
        self.occurence = o
        self.droit = d
        
    def modifier_fils_droit(self, d):
        self.droit = d

    def modifier_fils_gauche(self, g):
        self.gauche = g

    def fils_droit(self):
        return self.droit
        
    def fils_gauche(self):
        return self.gauche
    
    def valeur(self):
        return self.valeur
    
    def occurence(self):
        return self.occurence
        
        
    def donnee(self):
        """ Donne l'étiquette (la donnée)"""
        return self.valeur
    
    def __str__(self):
        return 'Valeur : ' + str(self.valeur) + \
            ' et Occurence : ' + str(self.occurence)
    
def est_feuille(a):
    return a.gauche is None and a.droit is None
    

def taille(a):
    if a is None:
        return 0
    else:
        return taille(a.fils_gauche()) + taille(a.fils_droit()) + 1


def creer_liste(dico):
    """ dict -> list
    Retourne la liste de noeud à partir du dictionnaire.
    """
    
    lst = []
    
    for key, value in dico.items():
        
        lst.append(Noeud(None, key, value, None))
        
    return lst


def minimum(lst):
    """ lst -> int
    Retourne l'indice du minimum de la liste de noeuds.
    """
    
    mini = 0
    
    for i in range(len(lst)):
        if lst[i].occurence < lst[mini].occurence:
            mini = i
            
    return mini


assert minimum(creer_liste(dict_exemple)) == 4
assert minimum(creer_liste(dictionnaire_car("A"))) == 0
assert minimum(creer_liste(dictionnaire(texte_un_car))) == 0


def creer_arbre(lst):
    """ lst -> Noeud()
    Retourne l'arbre à partir la liste de noeuds,
    En cherchant le minimum des occurences, puis les additionner.
    """

    while len(lst) > 1:
        a1 = lst.pop(minimum(lst))
        a2 = lst.pop(minimum(lst))
        
        a = Noeud(a1, None, a1.occurence + a2.occurence, a2)
        lst.append(a)
        
#         print(a)
#         print(a.fils_gauche())
#         print(a.fils_droit())
#         print()
#     print(lst[0])
    
    return lst[0]


# Si on a un fichier texte
def arbre_huffman(fichier):
    """ fichier texte -> Arbre
    Prend un fichier texte en argument en renvoie l'arbre d'Huffman.
    """
    
    return creer_arbre(creer_liste(dictionnaire(fichier)))


# Si on a une chaîne de caractères
def arbre_huffman_car(car):
    """ chaîne de caractère -> Arbre
    Prend une chaîne de caractère en argument en renvoie l'arbre d'Huffman.
    """
    
    return creer_arbre(creer_liste(dictionnaire_car(car)))


def parcours(arbre, chemin=""):
    """ Arbre -> dict
    Prend un abre en argument et créer le dictionnaire du codage Huffman
    en parcourant l'arbre récursivement.
    Ajoute 0 si à gauche et 1 si à droite.
    """
    
    codes = {}
    
    if arbre.gauche is None or arbre.droit is None:
        codes[arbre.valeur] = chemin
    else:
        codes.update(parcours(arbre.gauche, chemin+"0"))
        codes.update(parcours(arbre.droit, chemin+"1"))
    return codes
        
    
assert parcours(creer_arbre(creer_liste(dict_exemple))) == {'b': '00', 'a': '01', 'd': '100', 'e': '1010', 'f': '1011', 'c': '11'}
assert parcours(arbre_huffman(testpy)) == {' ': '000', 'p': '001', 'r': '010', 'o': '011', 'j': '100', 'e': '101', 't': '110', 'T': '1110', 's': '1111'}


# Si on a un fichier texte
def dico_huffman(fichier):
    """ fichier texte -> dict
    Prend un fichier texte en argument en renvoie le dictionnaire d'Huffman.
    """
    
    return parcours(creer_arbre(creer_liste(dictionnaire(fichier))))


# Si on a une chaîne de caractères
def dico_huffman_car(car):
    """ str -> dict
    Prend une chaîne de caractère en argument en renvoie le dictionnaire d'Huffman.
    """
    
    dicti = {}
    if car == len(car) * car[0]:
        dicti[car[0]] = '1'
        return dicti
    else:
        return parcours(creer_arbre(creer_liste(dictionnaire_car(car))))


assert dico_huffman(testpy) == {' ': '000', 'p': '001', 'r': '010', 'o': '011', 'j': '100', 'e': '101', 't': '110', 'T': '1110', 's': '1111'}
assert dico_huffman_car("CACHE") == {'A': '00', 'H': '01', 'E': '10', 'C': '11'}
# assert dico_huffman(texthuffman) == {'i': '0000', 'p': '0001', 'o': '0010', 'u': '0011', 'f': '0100', 'F': '01010', 'c': '01011', 'h': '01100', 'x': '01101', 'l': '01110', 'j': '01111', 'H': '10000', 'm': '10001', 'a': '10010', 'n': '10011', 'e': '101', ' ': '110', 'r': '1110', 't': '1111'}
assert dico_huffman_car("AA") == {'A': '1'}


# Fonction auxiliaire pour la compression
def compression_fichier(dico):
    """ fichier texte, dict -> str
    """
    global texte # Le texte de la fonction dictionnaire
    sortie = ""
    for caractere in texte:
        sortie += dico[caractere]
    
    return sortie
    
    
def compression_car(car, dico):
    """ str, dict -> str
    """
    
    sortie = ""
    for caractere in car:
        sortie += dico[caractere]
                        
    return sortie


assert compression_car("CACHE", dico_huffman_car("CACHE")) == '1100110110'
assert compression_fichier(dico_huffman(testpy)) == '11101011111110000001010011100101110'
# assert compression_fichier(dico_huffman(texthuffman)) == '010100000010110110000001011110110111110101101111110111000010010001111101100111010111000011110001001111101111111010000001101000100100011001010011'
assert compression_car("AA", dico_huffman_car("AA")) == '11'
assert compression_car("A", dico_huffman_car("A")) == '1'


# Compression finale
def compression_huffman(fichier):
    """ Fichier texte -> str
    Retourne le codage Huffman binaire d'un fichier texte.
    """
    
    return compression_fichier(dico_huffman(fichier))
    
        
def compression_huffman_car(car):
    """ str -> str
    Retourne le codage Huffman binaire d'une chaîne de caractères.
    """
    
    return compression_car(car, dico_huffman_car(car))


assert compression_huffman_car("A") == '1'
assert compression_huffman_car("EE") == '11'
assert compression_huffman_car("CACHE") == '1100110110'
assert compression_huffman_car("HUFFMAN") == '100101010111011100'
assert compression_huffman(testpy) == '11101011111110000001010011100101110'
# assert compression_huffman(texthuffman) == '010100000010110110000001011110110111110101101111110111000010010001111101100111010111000011110001001111101111111010000001101000100100011001010011'


# Décoder avec une une chaîne de caractères ou un fichier texte
def decompression_huffman(arbre, cha):
    """ arbre, str -> str
    Décompresse le code binaire à l'aide de l'abre du texte d'origine.
    """
    sortie = ""
    racine = arbre
    noeud_select = arbre
    
    chaine = ""
    if cha == len(cha) * cha[0]:
        chaine += arbre.valeur * arbre.occurence
        return chaine
    
    for bit in cha:
        if bit == '0':
            noeud_select = noeud_select.gauche
        else:
            noeud_select = noeud_select.droit
        if noeud_select.gauche is None and noeud_select.droit is None:
            sortie += noeud_select.valeur
            noeud_select = racine
    
    return sortie


assert decompression_huffman(arbre_huffman_car("A"), '1') == 'A'
assert decompression_huffman(arbre_huffman_car("AA"), '11') == 'AA'
assert decompression_huffman(arbre_huffman_car("CACHE"), '1100110110') == 'CACHE'
assert decompression_huffman(arbre_huffman_car("HUFFMAN"), '100101010111011100') == 'HUFFMAN'
assert decompression_huffman(arbre_huffman(testpy), '11101011111110000001010011100101110') == 'Test projet'
# assert decompression_huffman(arbre_huffman(texthuffman), '010100000010110110000001011110110111110101101111110111000010010001111101100111010111000011110001001111101111111010000001101000100100011001010011') == 'Fichier texte pour le projet Huffman'
assert decompression_huffman(arbre_huffman(texte_retour_ligne), '00111111001111100000001101101011100101001111101110011100100101000111001110011110101101111110000010010111101001011111010110100110010000001101010100101110011001111100111110111001111100000000111100110011010000010001101010000101111111011100111110110000101110111100111100000111100010101101100011110011010001100010110011010000011100011111100111110000000110110101110010100111110111001110010010100011100111001111010110111110100001011010110100101010001100111010010111111100000001101110011111010100111101000000101111001001001000100011011111010101010101101010101011101001101001001110011000000100011011101101000011001101100111000110010110010110001101110100101111100011101011001111110100100001010010011111011100111101000101111000100000100011011000100111110101110011001010110111100001000010001111001101010010011101001011111110000101011001011100000101001000101101001111101101011011000111101001011111011101010111000110011010101100011000111101101000001110001110001001010001110011100111101011011') \
                        == 'Le codage de Huffman est un algorithme de compression de données sans perte.\nLe codage de Huffman utilise un code à longueur variable pour représenter un symbole de la source (par exemple un caractère dans un fichier).\n\nHuffman'


def gain_fichier(dico):
    """ dict -> tuple
    Retourne la taille avant la compression puis la taille après la compression.
    """
    global texte
    global avant_compression
    global apres_compression
    avant_compression = len(texte) * 8
    apres_compression = 0
    lettres = dico.keys()
    
    for lettre in lettres:
        compte = texte.count(lettre)
        apres_compression += compte * len(dico[lettre])
    return avant_compression, apres_compression
    
    
def gain_car(cha, dico):
    """ str, dict -> tuple
    Retourne la taille avant la compression puis la taille après la compression.
    """
    avant_compression = len(cha) * 8
    apres_compression = 0
    lettres = dico.keys()
    
    for lettre in lettres:
        compte = cha.count(lettre)
        apres_compression += compte * len(dico[lettre])
    return avant_compression, apres_compression


assert gain_car("A", dico_huffman_car("A")) == (8, 1)
assert gain_car("AA", dico_huffman_car("AA")) == (16, 2)
assert gain_car("AAAAAAABCCCCCCDDEEEEE", dico_huffman_car("AAAAAAABCCCCCCDDEEEEE")) == (168, 45)
assert gain_car("CACHE", dico_huffman_car("CACHE")) == (40, 10)
assert gain_fichier(dico_huffman(testpy)) == (88, 35)
# assert gain_fichier(dico_huffman(texthuffman)) == (288, 144)
assert gain_car("Test projet", dico_huffman_car("Test projet")) == (88, 35)


def huffman(car, fichier=False):
    """ str -> Print
    Fonction finale qui prend une chaîne de caractère ou un fichier en argument.
    Pour un fichier il faudra spécifier True lors de l'appel de la fonction.
    Renvoie un affichage.
    """
    global texte
    
    if fichier:
        avant_codage = gain_fichier(dico_huffman(car))[0]
        apres_codage = gain_fichier(dico_huffman(car))[1]
        print("Fichier entré :", car)
        # print("Dictionnaire utilisé : ", dico_huffman(car))
        print("Texte compressé :", compression_huffman(car))
        print("Espace avant compression (en bits):", avant_codage)
        print("Espace après compression (en bits):", apres_codage)
        print("Soit une baisse de : ", int(abs(((apres_codage - avant_codage) / avant_codage) * 100)), "%")
        print("Texte décompressé :", decompression_huffman(arbre_huffman(car), compression_huffman(car)))
        
    else:
        avant_codage = gain_car(car, dico_huffman_car(car))[0]
        apres_codage = gain_car(car, dico_huffman_car(car))[1]
        print("Texte entré :", car)
        print("Dictionnaire utilisé : ", dico_huffman_car(car))
        print("Texte compressé :", compression_huffman_car(car))
        print("Espace avant compression (en bits):", avant_codage)
        print("Espace après compression (en bits):", apres_codage)
        print("Soit une baisse de : ", int(abs(((apres_codage - avant_codage) / avant_codage) * 100)), "%")
        print("Texte décompressé :", decompression_huffman(arbre_huffman_car(car), compression_huffman_car(car)))
        
    print()

        
#huffman('CACHE')
#huffman("Huffman")
#huffman("BADGE")
#huffman("NSI")
#huffman("Python")
#huffman('AA')
#huffman('AAAAAAABCCCCCCDDEEEEE')
#huffman(texthuffman, True)
#huffman(testpy, True)
#huffman(texte_retour_ligne, True)
#huffman(grostexte, True)
