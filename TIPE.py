### TIPE : Compression par ondelette de Haar d'images colorées


## Bibliothèques & Image importées

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
from copy import deepcopy
import pywt

Image=img.imread("C:/Chartres.jpg")
Image=np.array(Image,dtype='int32')
#L'image avec laquelle on travaillera



## Fonctions utiles


def changer_couleur(Image : np.ndarray, rouge : bool, vert : bool, bleu : bool) -> None :
    """
    Description : cette fonction affiche seulement la composante rouge, verte, bleu ou une combinaison de ces trois couleurs de l'image en entrée

    Entrées : une image (np.ndarray) et trois boléens (un pour chaque couleur primaire)

    Sortie : affiche la composante choisie de l'image
    """

    I2=[[[0,0,0]for a in range (0,len(Image[0]))]for a in range (0,len(Image))]
    for i in range (0,len(Image)):
        for j in range (0,len(Image[0])):
            I2[i][j]=[Image[i][j][0],Image[i][j][1],Image[i][j][2]]
            if rouge==False:
                 I2[i][j][0]=0
            if vert==False:
                I2[i][j][1]=0
            if bleu==False:
                I2[i][j][2]=0
    plt.imshow(I2)
    plt.show()
    return None



def une_seule_couleur(Image : np.ndarray, rougevertbleu : int) -> np.ndarray :
    """
    Description : cette fonction représente une variation de la fonction changer_couleur en utilisant plt.imshow() à un seul coefficient de couleur (au lieu des 3 de la fonction précédente), on doit donc utiliser une colourmap pour afficher l'image

    Entrée : une image (np.ndarray) et un entier (0,1 ou 2 pour rouge, vert ou bleu)

    Sortie : l'image dont on ne gardera que la couleur choisie et que l'on pourra afficher à l'aide d'une colourmap si nécessaire
    """

    Image=np.array(Image)
    I=np.zeros((len(Image),len(Image[0])))
    for i in range(len(Image)):
        for j in range(len(Image[0])):
            I[i][j]=Image[i][j][rougevertbleu]
    I=np.array(I,dtype='int32')
    I2=np.array(255-I, dtype='int32')
    #on fait 255-I parce que les cmaps 'Reds', 'Greens' et 'Blues' vont du clair (0) au foncé (255) alors qu'en RGB, on va du noir (0,0,0) au blanc (255,255,255)
    #Colour_map=['Reds','Greens','Blues']
    #plt.imshow(I2,cmap=Colour_map[rougevertbleu])
    #plt.show()
    return I



def coef_pairs(Image : np.ndarray) -> np.ndarray :
    """
    Description : cette fonction renvoie la même image qu'en entrée, mais ayant un nombre pair de lignes et de colonnes

    Entrée : une image (np.ndarray)

    Sortie : la même image dont on supprime la dernière ligne et/ou colonne si son nombre de lignes/colonnes est impair
    """

    I=deepcopy(Image)
    if len(Image)%2!=0:
    #si le nombre de lignes de l'image est impaire
        I=I[:-1]
        #alors on supprime la dernière
    if len(Image[0])%2!=0:
    #si le nombre de colonnes de l'image est impaire
        I=np.delete(I, -1, axis = 1)
        #alors on supprime la dernière
    return I



def comparaison(I1 : np.ndarray, I2 : np.ndarray) -> str :
    """
    Description : cette fonction donne le nombre de coefficients différents entre deux images ainsi que le pourcentage que représente cette différence

    Entrées : deux images (np.ndarray) de même dimension

    Sorties : le nombre de coefficients différents ainsi que le pourcentage de différence entre les deux images en entrée
    """

    I1=np.array(I1,dtype='int32')
    I2=np.array(I2,dtype='int32')
    a=0
    L=I1.shape
    for i in range (0,len(I1)):
        for j in range (0,len(I1[0])):
            if type(I1[0][0])==type(I2[0][0])==np.ndarray:
                for k in range (0,len(I1[0][0])):
                    if I1[i][j][k]!=I2[i][j][k]:
                        a+=1
            else :
                if I1[i][j]!=I2[i][j]:
                    a+=1
    print(str(a) + ' coefficients différents')
    sum_coefs=1
    for i in range (0,len(L)):
        sum_coefs=sum_coefs*L[i]
    print(str(a/(sum_coefs)) + ' % de différence')
    return None



## Transformée en ondelette directe :


def passe_bas_x(Image : np.ndarray) -> np.ndarray :
    """
    Description : cette fonction calcule la moyenne des coefficients des pixels de chaque couleur de l'image (np.ndarray) selon l'axe horizontal

    Entrée : une image (np.ndarray)

    Sortie : la même image (np.ndarray) dont le nombre de colonnes a été divisé par 2
    """

    nombre_lignes=len(Image)
    nombre_colonnes=len(Image[0])
    I=[[[0,0,0]for _ in range (0,nombre_colonnes//2)]for _ in range (0,nombre_lignes)]
    for i in range (0,nombre_lignes):
        for j in range (0,nombre_colonnes//2):
            if type(Image[0][0])==np.ndarray:
                for k in range (0,len(Image[0][0])):
                    I[i][j][k]= (int(Image[i][2*j][k]) + int(Image[i][2*j+1][k]))
            else :
                I[i][j]=(int(Image[i][2*j]) + int(Image[i][2*j+1]))
    return np.array(I,dtype='int32')



def passe_bas_y(Image : np.ndarray) -> np.ndarray :
    """
    Description : cette fonction calcule la moyenne des coefficients des pixels de chaque couleur de l'image (np.ndarray) selon l'axe vertical

    Entrée : une image (np.ndarray)

    Sortie : la même image (np.ndarray) dont le nombre de lignes a été divisé par 2
    """

    nombre_lignes=len(Image)
    nombre_colonnes=len(Image[0])
    I=[[[0,0,0]for _ in range (0,nombre_colonnes)]for _ in range (0,nombre_lignes//2)]
    for i in range (0,nombre_lignes//2):
        for j in range (0,nombre_colonnes):
            if type(Image[0][0])==np.ndarray:
                for k in range (0,len(Image[0][0])):
                    I[i][j][k]= (int(Image[2*i][j][k]) + int(Image[2*i+1][j][k]))
            else :
                I[i][j]=(int(Image[2*i][j]) + int(Image[2*i+1][j]))
    return np.array(I,dtype='int32')



def passe_haut_x(Image : np.ndarray) -> np.ndarray :
    """
    Description : cette fonction calcule le "détail" des coefficients des pixels de chaque couleur de l'image selon l'axe horizontal

    Entrée : une image (np.ndarray)

    Sortie : une image contenant les coefficients de détails de l'entrée selon l'axe horizontal
    """

    nombre_lignes=len(Image)
    nombre_colonnes=len(Image[0])
    I=[[[0,0,0]for _ in range (0,nombre_colonnes//2)]for _ in range (0,nombre_lignes)]
    for i in range (0,nombre_lignes):
        for j in range (0,nombre_colonnes//2):
            if type(Image[0][0])==np.ndarray:
                for k in range (0,len(Image[0][0])):
                    I[i][j][k]= (int(Image[i][2*j][k]) - int(Image[i][2*j+1][k]))
            else :
                I[i][j]=(int(Image[i][2*j]) - int(Image[i][2*j+1]))
    return np.array(I,dtype='int32')



def passe_haut_y(Image : np.ndarray) -> np.ndarray :
    """
    Description : cette fonction calcule le "détail" des coefficients des pixels de chaque couleur de l'image selon l'axe vertical

    Entrée : une image (np.ndarray)

    Sortie : une image contenant les coefficients de détails de l'entrée selon l'axe vertical
    """

    nombre_lignes=len(Image)
    nombre_colonnes=len(Image[0])
    I=[[[0,0,0]for _ in range (0,nombre_colonnes)]for _ in range (0,nombre_lignes//2)]
    for i in range (0,nombre_lignes//2):
        for j in range (0,nombre_colonnes):
            if type(Image[0][0])==np.ndarray:
                for k in range (0,len(Image[0][0])):
                    I[i][j][k]= (int(Image[2*i][j][k]) - int(Image[2*i+1][j][k]))
            else :
                I[i][j]=(int(Image[2*i][j]) - int(Image[2*i+1][j]))
    return np.array(I,dtype='int32')



def TOD_Haar(Image : np.ndarray) -> list[np.ndarray] :
    """
    Description : cette fonction réalise la transformée en ondelette directe de Haar de l'image colorée en entrée

    Entrée : une image (np.ndarray)

    Sorties : quatre images : une contenant les coefficients d'approximation de l'image originale, et trois autres contenant les coefficients de détail selon l'axe horizontal, l'axe vertical et enfin selon la diagonale
    """

    Image=coef_pairs(Image)
    i1=passe_bas_x(Image)
    i2=passe_haut_x(Image)
    i3=passe_bas_y(i1)/2
    i4=passe_haut_y(i1)/2
    i5=passe_bas_y(i2)/2
    i6=passe_haut_y(i2)/2
    return [i3,i4,i5,i6]



##Affichage


def convert(L : list[np.ndarray])-> np.ndarray :
    """
    Description : cette fonction fait en sorte que ce que renvoie le fonction TOD_Haar puisse être affiché correctement à l'aide de la méthode plt.show()

    Entrées : la transformée en ondelette d'une image sous la forme [coefficients d'approximation, coefficients de détail selon l'axe vertical, coefficients de détail selon l'axe horizontal, coefficient de détail selon la diagonale]

    Sorties : la même forme qu'en entrée, mais avec chacun des coefficients sous la forme d'une image
    """

    L0=L[0]
    L0=L0//2
    L1,L2,L3=abs(L[1]),abs(L[2]),abs(L[3])
    L0=np.array(L0,dtype='int32')
    L1=np.array(L1,dtype='int32')
    L2=np.array(L2,dtype='int32')
    L3=np.array(L3,dtype='int32')
    return [L0,L1,L2,L3]



def affichage_usuel_1D(L : list[np.ndarray]) -> None :
    """
    Description : cette fonction affiche la transformée en ondelette directe de Haar de l'image sous la forme usuelle

    Entrées : les quatre images (np.ndarray) en sortie de la fonction TOD_Haar, c'est-à-dire les coefficients d'approximation (ca), les coefficients de détail selon l'axe vertical (cdv), les coefficients de detail selon l'axe horizontal (cdh) et les coefficients de détail selon la diagonale (cdd)

    Sorties : l'affichage de ces quatre images selon le format usuel (en utilisant plt.show()
    """

    ca,cdv,cdh,cdd=convert(L)
    I1=np.concatenate((ca,cdh),axis=1)
    I2=np.concatenate((cdv,cdd),axis=1)
    I=np.concatenate((I1,I2),axis=0)
    plt.imshow(I,cmap='Greys')
    plt.show()
    return None



def affichage_usuel_3D(L : list[np.ndarray]) -> None :
    """
    Description : cette fonction affiche la transformée en ondelette directe de Haar de l'image RGB sous la forme usuelle

    Entrées : les quatre images (np.ndarray) en sortie de la fonction TOD_Haar, c'est-à-dire les coefficients d'approximation (ca), les coefficients de détail selon l'axe vertical (cdv), les coefficients de detail selon l'axe horizontal (cdh), et les coefficients de détail selon la diagonale (cdd)

    Sorties : l'affichage de ces quatre images selon le format usuel (en utilisant plt.show())
    """

    ca,cdv,cdh,cdd=convert(L)
    I1=np.concatenate((ca,255-cdh),axis=1)
    I2=np.concatenate((255-cdv,255-cdd),axis=1)
    #Je fais 255-x pour afficher sur un fond blanc, ce que permet selon moi de mieux comprendre ce qu'il se passe
    I=np.concatenate((I1,I2),axis=0)
    plt.imshow(I)
    plt.show()
    return None


## Quantification


def quantification(L : list[np.ndarray], valeur : int) -> list[np.ndarray] :
    """
    Description : cette fonction réalise la perte de détail (afin de compresser l'image) sur les array cdh, cdv et cdd en remplaçant les coefficients inférieurs à l'entrée 'valeur' par 0

    Entrées : les quatre images (np.ndarray) en sortie de la fonction TOD_Haar, c'est-à-dire les coefficients d'approximation (ca), les coefficients de détail selon l'axe vertical (cdv), les coefficients de détail selon l'axe horizontal (cdh), et les coefficients de détail selon la diagonale (cdd) et une valeur de quantification

    Sorties : ca (inchangé), cdh, cdv et cdd dont les valeurs des coefficients inférieurs à la valeur demandée sont éliminées
    """

    L0,L1,L2,L3=deepcopy(L[0]),deepcopy(L[1]),deepcopy(L[2]),deepcopy(L[3])
    for i in range (0,len(L0)):
        for j in range (0,len(L0[0])):
            if type(L0[0][0])==np.ndarray:
                for k in range (0,len(L0[0][0])):
                    if abs(L1[i][j][k])<=valeur:
                        L1[i][j][k]=0
                    if abs(L2[i][j][k])<=valeur:
                        L2[i][j][k]=0
                    if abs(L3[i][j][k])<=valeur/2:
                        L3[i][j][k]=0
            else :
                if abs(L1[i][j])<=valeur:
                    L1[i][j]=0
                if abs(L2[i][j])<=valeur:
                    L2[i][j]=0
                if abs(L3[i][j])<=valeur/2:
                    L3[i][j]=0
    return [L0,L1,L2,L3]



## Transformée en ondelette inverse :


"""
On a directement l'ondelette inverse en faisant pywt.idwt2(TOD_Haar(Image),'haar')
"""



##Compression par ondelette de Haar


def CO_Haar(Image : np.ndarray, valeur : int) -> np.ndarray :
    """
    Description : cette fonction réalise la compression par ondelette de l'image entrée avec la valeur de quantification indiquée

    Entrées : une image (np.ndarray) et une valeur de quantification (int)

    Sortie : l'image compressée par la méthode de compression par ondelette
    """

    Image=coef_pairs(Image)
    I=deepcopy(Image)
    for k in range (0,len(Image[0][0])):
        Im=une_seule_couleur(Image,k)
        ca,cdv,cdh,cdd=TOD_Haar(Im)
        ca,cdv,cdh,cdd=quantification([ca,cdv,cdh,cdd],valeur)
        L=[ca,(cdv,cdh,cdd)]
        TOI_Haar=pywt.idwt2(L,'haar')
        TOI_Haar=np.array(TOI_Haar,dtype='int')
        for i in range (0,len(Image)):
            for j in range (0,len(Image[0])):
                I[i][j][k]=(TOI_Haar[i][j])
    I=np.array(I,dtype='int')
    return I


##Autres choses utilisées


#Pour enregistrer mes images, j'ai utilisé la méthode :
#plt.imsave('Chemin_de_l_image', nom_de_l_image)
#Il faut penser à changer le dtype de l'image pour que cette méthode fonctionne en faisant :
#Image=np.array(Image,dtype='uint8')


#Pour afficher les graphiques de comparaison de la taille de l'image en fonction de la valeur de quantification, j'ai utilisé le code suivant :
"""
ord1,ord2,ord3,ord4=[481,476,448,432,416],[416,415,405,402,394],[232,115,110,108,105],[541,539,523,494,466]
abs=[0,5,30,60,100]

plt.plot(abs,ord1,'-rs')
plt.plot(abs,ord2,'-gs')
plt.plot(abs,ord3,'-bs')
plt.plot(abs,ord4,'-ms')
plt.xlabel('valeur de quantification')
plt.ylabel('taille de l image (ko)')
plt.show()
"""

#Pour avoir le taux de compression d'une image (en pourcentage), on fait le calcul :
#T=100-(Taille_image_compressée/Taille_image_originelle)*100

#Pour comparer deux images, j'utilise la fonction :
#comparaison(Image,Image2)

