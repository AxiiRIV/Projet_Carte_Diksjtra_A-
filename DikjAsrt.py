######################################
# Récupération des données du graphe #
######################################
'''
Quatre fichiers tabulaires csv :

    - aretes.csv : les lignes correspondent aux arêtes. Une colonne distance a été ajoutée
      par rapport au fichier original.
    - sommets.csv : les lignes correspondent aux sommets du graphe.
    - matrice_poids.csv: matrice des poids-distances, telle que définie dans le cours pour 
      l'algorithme de Floyd-Warshall (0 dans la diagonale, inf pour les arcs absents)
      Les index et les noms de colonnes correspondent aux identifiants des sommets.
    - matrice_adjacence.csv : matrice d'adjacence. Les lignes et les colonnes correspondent aux identifiants des sommets.

Deux fichiers json, pour une importation directe dans des dictionnaires :

    - dicsucc.json : pour récupérer le dictionnaire des successeurs
    - dicsuccdist.json : pour récupérer les successeurs et les distances
'''
##########################################################
# Importation des bibliothèques et répertoire par défaut #
##########################################################
import pandas as pd
import numpy as np
import json
import os
from math import sin, cos, acos, pi, floor
import matplotlib.pyplot as plt
import time

os.chdir('F:\iut\BUT1\S2\S2.02_exploration-algo\Données et programme semaine 3-20260428')

############################################################
# Calcul de la  distance entre deux points A et B dont     #
# on connait la lattitude et la longitude                  #
# Cette fonction a été utilisé pour calculer les distances #
############################################################
# https://fr.wikipedia.org/wiki/Distance_du_grand_cercle
'''La distance du grand cercle, également appelée distance orthodromique, 
est la plus courte distance entre deux points sur une sphère. 
La surface de la Terre étant approximativement sphérique, 
la distance du grand cercle est généralement employée pour mesurer 
la distance entre deux points à sa surface, à partir de leur longitude et leur latitude.'''
def distanceGPS(latA,latB,longA,longB):
    # Conversions des latitudes en radians
    ltA=latA/180*pi
    ltB=latB/180*pi
    loA=longA/180*pi
    loB=longB/180*pi
    # Rayon de la terre en mètres (sphère IAG-GRS80)
    RT = 6378137
    # angle en radians entre les 2 points 
    S = acos(round(sin(ltA)*sin(ltB) + cos(ltA)*cos(ltB)*cos(abs(loB-loA)),14))
    # distance entre les 2 points, comptée sur un arc de grand cercle
    return S*RT


################################
#            IMPORT            #
################################

# Importation des csv
df_aretes = pd.read_csv("aretes.csv",index_col = 0, sep =';')
df_sommets = pd.read_csv("sommets.csv", index_col = 0, sep = ';')

df_matpoids = pd.read_csv("matrice_poids.csv", index_col = 0, sep = ';')
df_matpoids.columns = df_matpoids.index

df_matadj = pd.read_csv("matrice_adjacence.csv", index_col = 0, sep = ';')
df_matadj.columns = df_matadj.index


#Importation des json (par défaut les clés sont importées sous forme de chaînes de caractères, on corrige)

#############################
# Dictionnaire dicsucc.json #
#############################
with open("dicsucc.json", "r") as fichier:
    dicsucc = json.load(fichier)
# Convertir les clés en entiers
dicsucc = {int(k): v for k, v in dicsucc.items()}

#################################
# Dictionnaire dicsuccdist.json #
#################################
with open("dicsuccdist.json", "r") as fichier:
    dicsuccdist = json.load(fichier)
# Convertir les clés en entiers
dicsuccdist = {int(k): v for k, v in dicsuccdist.items()}


##############
# Complément #
##############

# transformation dataframe matrice des poids en tableau numpy   
tableau_poids = np.array(df_matpoids)
tableau_adj = np.array(df_matadj)


# transformation matrice des poids en liste de liste
n = len(tableau_adj)

liste_poids = [[tableau_poids[i, j] for j in range(n)] for i in range(n)]
liste_adj = [[tableau_adj[i, j] for j in range(n)] for i in range(n)]


# Correspondance indice <--> identifiant pour chaque sommet
# On peut éventuelleùent définir des fonctions ou des dictionnaires de corresponances
# Exemple : 
# les dictionnaires de correspondance
correspindsom = {}
correspsomind = {}
i = 0
for som in df_sommets.index : 
    correspindsom[i] = som
    correspsomind[som] = i
    i = i+1
    
def lst_succ(mat,point):
    lst = []
    for j in range(len(mat[point])):
        if mat[point][j] == 1:
            lst.append(j)
    return lst

lst_succ(liste_adj,464)

def parcours_profondeur(mat,NomPoint):
    indicePoint = correspsomind[NomPoint]
    pile = [indicePoint]
    Vu = [False for i in range(len(mat))]
    somVu = [indicePoint]
    somvunom = [NomPoint]
    Vu[indicePoint] = True
    while pile != []:
        Inds = pile.pop(-1)
        lst_Succ = lst_succ(mat,Inds)
        for succ in lst_Succ:
            if Vu[succ] == False:
                pile.append(succ)
                Vu[succ] = True
                somVu.append(succ)
                nomSucc = correspindsom[succ]
                somvunom.append(nomSucc)
    return (somvunom)  

l=parcours_profondeur(liste_adj, 11887639061)


def nettoyage_df(lst):
    new_df = df_matadj.loc[lst,lst]
    
    return new_df

df_mat_adj_nettoyage = nettoyage_df(l)

def nettoyage_df(lst):
    new_df = df_matpoids.loc[lst,lst]
    
    return new_df

df_mat_poids_nettoyage = nettoyage_df(l)

df_sommets_nettoye = df_sommets.loc[l,:]



correspindsom = {}
correspsomind = {}
i = 0
for som in df_sommets_nettoye.index : 
    correspindsom[i] = som
    correspsomind[som] = i
    i = i+1

tableau_adj_nettoye = np.array(df_mat_adj_nettoyage)
tableau_poids_nettoye = np.array(df_mat_poids_nettoyage)

m = len(tableau_adj_nettoye)

liste_adj_nettoyage = [[tableau_adj_nettoye[i, j] for j in range(m)] for i in range(m)]
liste_poids_nettoyage = [[tableau_poids_nettoye[i, j] for j in range(m)] for i in range(m)]
#Semaine 3

lstDist = [0,12,4,9,9,15,13]
pred = [None,2,0,0,2,4,4]
atraiterEx = [True, False, False, False, False, False, False]

def extract_min(dist):
    minimum = float('inf')
    minInd = 0
    for i in range(len(dist)):
        if dist[i] < minimum :
            minimum = dist[i]
            minInd = i
    return minimum, minInd

extract_min(lstDist)

def extract_min2(dist, atraiter):
    minInd = 0
    minimum = float('inf')
    for i in range(len(dist)):
        if dist[i] < minimum:
            if atraiter[i] == False:
                minimum = dist[i]
                minInd = i
    return minInd

extract_min2(lstDist,atraiterEx)

def extract_min_Df(dist, atraiter):
    minInd = 0
    minimum = float('inf')
    for i in range(len(dist)):
        if dist[i] < minimum:
            if atraiter[i] == False:
                minimum = dist[i]
                minInd = i
    return minInd


def reconstitution(pred, dep, arr):
    cheminMin = [dep]
    atraiter = [False]*len(pred)
    atraiter[dep] = True
    i = 0
    while (True):
        minInd = extract_min2(lstDist, atraiter)
        cheminMin.append(minInd)
        atraiter[minInd] = True
        if arr in cheminMin:
            break
        if i > len(pred):
            break
        i+=1
    return cheminMin

reconstitution(pred, 0, 6)
        

def relacher(u,v,dist,pred,poids):
    if dist[v] > dist[u] + poids[u][v] :
        dist[v] = dist[u] + poids[u][v]
        pred[v] = u
   # return dist,pred



poids=[[float('inf'),2,6,3],
       [2,float('inf'),8,5],
       [5,8,float('inf'),10],
       [5,5,10,float('inf')]]

def Dijkstra(mat,poids,dep):
    debTime = time.time()
    dist = [float('inf')]*len(poids)
    dist[dep] = 0 
    pred = [None]*len(poids)
    atraiter = [False]*len(poids)
    for i in range(len(poids)):
        minInd = extract_min2(dist, atraiter)
        lstSucc = lst_succ(mat, minInd)
        for succ in lstSucc :
            #dist,pred = 
            relacher(minInd,succ,dist,pred,poids)
        atraiter[minInd] = True
    finTime = time.time()
    return dist, pred, finTime - debTime

Dijkstra(liste_adj_nettoyage, liste_poids_nettoyage, 0)     
len(df_mat_poids_nettoyage)

for ind in df_sommets.index :
    if df_sommets.loc[ind,'nom'] == "La Rhune":
        idRhune = ind
        indRhune = correspsomind[ind]
    if df_sommets.loc[ind,'nom'] == "Place de Sare":
        idPSare = ind
        Place_de_sare = correspsomind[255240960]
        La_Rhune = correspsomind[11887639061]
        nomSommet = correspindsom[0]
        latA = df_sommets.loc[ind, 'lat']


def extract_minAStar(dist, atraiter,arrivee):
    nomSommetArrivee = correspindsom[arrivee]
    latB = df_sommets.loc[nomSommetArrivee,'lat']
    longB = df_sommets.loc[nomSommetArrivee,'lon']
    minInd = 0
    minimum = float('inf')
    for i in range(len(dist)):
        nomSommet = correspindsom[i]
        latA = df_sommets.loc[nomSommet,'lat']
        longA = df_sommets.loc[nomSommet,'lon']
        if dist[i] + distanceGPS(latA, latB, longA, longB)*3 < minimum:
            if atraiter[i] == False:
                minimum = dist[i]
                minInd = i
    return minInd

def AStar(mat,poids,dep,arrivee):
    debTime = time.time()
    dist = [float('inf')]*len(poids)
    dist[dep] = 0 
    pred = [None]*len(poids)
    atraiter = [False]*len(poids)
    for i in range(len(poids)):
        minInd = extract_minAStar(dist, atraiter,arrivee)
        lstSucc = lst_succ(mat, minInd)
        for succ in lstSucc :
            #dist,pred = 
            relacher(minInd,succ,dist,pred,poids)
        atraiter[minInd] = True
    finTime = time.time()
    return dist, finTime - debTime

AStar(liste_adj_nettoyage, liste_poids_nettoyage, 0,831)



def score(dist, i, latArriv, longArriv, a, b):
    if b == 0:
        return dist[i] * a
    else :
        # On récupère le nom du sommet 'i' de manière locale et sécurisée
        nomSommetCourant = correspindsom[i]
        latA = df_sommets.loc[nomSommetCourant, 'lat']
        longA = df_sommets.loc[nomSommetCourant, 'lon'] 
        return a * dist[i] + distanceGPS(latA, latArriv, longA, longArriv) * b
        
def extract_minDijAStar(dist, atraiter, arrivee, a, b):
    nomSommetArrivee = correspindsom[arrivee]
    latB = df_sommets.loc[nomSommetArrivee, 'lat']
    longB = df_sommets.loc[nomSommetArrivee, 'lon']
    minInd = 0
    minimum = float('inf')
    for i in range(len(dist)):
        if atraiter[i] == False:
            # On passe directement les bonnes coordonnées à score
            if score(dist, i, latB, longB, a, b) < minimum:
                minimum = dist[i]
                minInd = i
    return minInd


def DijAStar(mat,poids,dep,arrivee,a,b):
    debTime = time.time()
    dist = [float('inf')]*len(poids)
    dist[dep] = 0 
    pred = [None]*len(poids)
    atraiter = [False]*len(poids)
    for i in range(len(poids)):
        minInd = extract_minDijAStar(dist, atraiter,arrivee,a,b)
        lstSucc = lst_succ(mat, minInd)
        for succ in lstSucc :
            #dist,pred = 
            relacher(minInd,succ,dist,pred,poids)
        atraiter[minInd] = True
    cheminFinal = []
    #sommetArrivee = correspindsom[arrivee]
    courant = arrivee
        
        #tant que le sommet courant n'est pas le sommet de depart : 
    #sommetDep = correspindsom[dep]
    while courant != dep:
        cheminFinal.append(courant)
        courant = pred[courant]
        if courant is None:
            return [] # Le sommet d'arrivÃ©e n'est pas atteignable
                
    cheminFinal.append(dep)
    return cheminFinal


DijAStar(liste_adj_nettoyage, liste_poids_nettoyage, 0,831,1,0)


from graphics import *

def relacher2(u,v,dist,poids, pred, nomSommet, coordX, coordY, win):
    if dist[v] > dist[u] + poids[u][v] :
        dist[v] = dist[u] + poids[u][v]
        pred[v] = u
        nomSucc = correspindsom[v]
        affichLigne(win, df_sommets_nettoye, nomSommet, nomSucc, coordX, coordY)

def DijAStarCarte(mat,poids,dep,arrivee,a,b):
    debTime = time.time()
    win = GraphWin("Carte de la Rhune",1167,717, True)
    main(win)
    dist = [float('inf')]*len(poids)
    dist[dep] = 0 
    pred = [None]*len(poids)
    atraiter = [False]*len(poids)
    for i in range(len(poids)):
        minInd = extract_minDijAStar(dist, atraiter,arrivee,a,b)
        nomSommetATraiter = correspindsom[minInd]
        coorX, coorY = affichSommet3(win, df_sommets_nettoye, nomSommetATraiter)
        lstSucc = lst_succ(mat, minInd)
        for succ in lstSucc :
            relacher2(minInd,succ,dist,poids, pred, nomSommetATraiter, coorX, coorY, win)
        atraiter[minInd] = True
    sommetRhune = Circle(Point(pxXRhune, pxYRhune), 5)
    sommetRhune.setFill("red")
    sommetRhune.draw(win)
    finTime = time.time()
    win.getMouse()
    win.close()
    return dist, finTime - debTime

DijAStarCarte(liste_adj_nettoyage, liste_poids_nettoyage, 0,831,1,0)[0][831]
DijAStarCarte(liste_adj_nettoyage, liste_poids_nettoyage, 0,831,1,1)[0][831]

    

def DijAStarCarteReconstitution(mat,poids,dep,arrivee,a,b):
    debTime = time.time()
    win = GraphWin("Carte de la Rhune",1167,717, True)
    main(win)
    dist = [float('inf')]*len(poids)
    dist[dep] = 0 
    pred = [None]*len(poids)
    atraiter = [False]*len(poids)
    for i in range(len(poids)):
        minInd = extract_minDijAStar(dist, atraiter,arrivee,a,b)
        nomSommetATraiter = correspindsom[minInd]
        coorX, coorY = affichSommet3(win, df_sommets_nettoye, nomSommetATraiter)
        lstSucc = lst_succ(mat, minInd)
        for succ in lstSucc :
            relacher2(minInd,succ,dist,poids, pred, nomSommetATraiter, coorX, coorY, win)
        atraiter[minInd] = True
    sommetRhune = Circle(Point(pxXRhune, pxYRhune), 5)
    sommetRhune.setFill("red")
    sommetRhune.draw(win)
    cheminFinal = []
    #sommetArrivee = correspindsom[arrivee]
    courant = arrivee
        
        #tant que le sommet courant n'est pas le sommet de depart : 
    #sommetDep = correspindsom[dep]
    while courant != dep:
        cheminFinal.append(courant)
        courantTemp = courant
        courant = pred[courant]
        if courant is None:
            courant = [] # Le sommet d'arrivÃ©e n'est pas atteignable
                
    cheminFinal.append(dep)
    afficherReconstitution(win, cheminFinal)
    win.getMouse()
    win.close()


DijAStarCarteReconstitution(liste_adj_nettoyage, liste_poids_nettoyage, 0,831,1,0)

def afficherReconstitution(win,chemin):
    for i in range(len(chemin) - 1):
        sommet1 = correspindsom[chemin[i]]
        coorX = (df_sommets.loc[sommet1, "lon"] - lonLeft) * ratioX
        coorY = (latTop - df_sommets.loc[sommet1, "lat"]) * ratioY
        sommet = Circle(Point(coorX, coorY),3)
        sommet.setOutline("black")
        sommet.setFill("red")
        sommet.draw(win)
        
        sommet2 = correspindsom[chemin[i+1]]
        coorXSecond = (df_sommets.loc[sommet2, "lon"] - lonLeft) * ratioX
        coorYSecond = (latTop - df_sommets.loc[sommet2, "lat"]) * ratioY
        aLine = Line(Point(coorX, coorY), Point(coorXSecond, coorYSecond))
        aLine.setFill("red")
        aLine.setArrow("last")
        aLine.draw(win) 
        


Rhune = 11887639061

rhune = Image(Point(100,100),"")

rhuneWidth = rhune.getWidth()
rhuneHeight = rhune.getHeight()

# Coordonnées GPS de l'image
coordHautDroite = [43.35002, -1.572983]
coordBasGauche = [43.27846, -1.73344]

latTop = coordHautDroite[0]
lonRight = coordHautDroite[1]

latBottom = coordBasGauche[0]
lonLeft = coordBasGauche[1]

# Taille GPS couverte
gpsWidth = lonRight - lonLeft
gpsHeight = latTop - latBottom

# Ratios
ratioX = rhuneWidth / gpsWidth
ratioY = rhuneHeight / gpsHeight


# Conversion GPS -> pixels
pxXRhune = (df_sommets.loc[Rhune, "lon"] - lonLeft) * ratioX
pxYRhune = (latTop - df_sommets.loc[Rhune, "lat"]) * ratioY




def affichSommet(win,df_sommets):
    for key in df_matadj.index:  
        coorX = (df_sommets.loc[key, "lon"] - lonLeft) * ratioX
        coorY = (latTop - df_sommets.loc[key, "lat"]) * ratioY
        sommet = Circle(Point(coorX, coorY),3)
        sommet.setOutline("black")
        sommet.setFill("yellow")
        sommet.draw(win)
        # Fix: Use the newly calculated coorX and coorY, not the global pxX/pxY
        
        

def affichSommet3(win, df_sommets_nettoye, nomSommet):
    coorX = (df_sommets_nettoye.loc[nomSommet, "lon"] - lonLeft) * ratioX
    coorY = (latTop - df_sommets_nettoye.loc[nomSommet, "lat"]) * ratioY 
    sommet = Circle(Point(coorX, coorY),3)
    sommet.setOutline("black")
    sommet.setFill("blue")
    sommet.draw(win)
    return coorX, coorY

def affichSommet4(win, df_sommets_nettoye, nomSommet):
    coorX = (df_sommets_nettoye.loc[nomSommet, "lon"] - lonLeft) * ratioX
    coorY = (latTop - df_sommets_nettoye.loc[nomSommet, "lat"]) * ratioY 
    sommet = Circle(Point(coorX, coorY),3)
    sommet.setOutline("black")
    sommet.setFill("red")
    sommet.draw(win)
    return coorX, coorY

def affichLigne(win, df_sommets, nomSommet, succ, coorX, coorY):
    coorXSecond = (df_sommets.loc[succ, "lon"] - lonLeft) * ratioX
    coorYSecond = (latTop - df_sommets.loc[succ, "lat"]) * ratioY
    aLine = Line(Point(coorX, coorY), Point(coorXSecond, coorYSecond))
    aLine.setFill("black")
    aLine.draw(win)    
    

def affichLigne2(win, df_sommets, nomSommet, succ, coorX, coorY):
    coorXSecond = (df_sommets.loc[succ, "lon"] - lonLeft) * ratioX
    coorYSecond = (latTop - df_sommets.loc[succ, "lat"]) * ratioY
    aLine = Line(Point(coorX, coorY), Point(coorXSecond, coorYSecond))
    aLine.setFill("red")
    aLine.setArrow("last")
    aLine.setWidth(10)
    aLine.draw(win)   
    
    
def main(win):
    #win = GraphWin("My Circle", rhuneWidth, rhuneHeight)
    img = Image(Point(rhuneWidth / 2, rhuneHeight / 2), "F:\iut\BUT1\S2\S2.02_exploration-algo\laRhune.png")
    img.draw(win)
    
    affichSommet(win, df_sommets)
    
    


