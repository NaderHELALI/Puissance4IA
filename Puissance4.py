#Ce programme vise à creer un puissance 4 avec une IA basée sur l'algorithme MinMax

#Implémentation des modules
import numpy as np
import math
import pygame
import sys

#Taille du jeu
nbRow=6
nbColums=7
nbCoupMax=30

#Couleur
Bleu=(0,0,255)
Noir=(0,0,0)
###Gestion du jeu : 

#Choix de la main Joueur/ AI
def handle():
    hand=0
    while hand!=1 and hand!=2 :
        hand=float(input('Entrer 1 si vous jouez en premier, 2 sinon : '))
    return hand

#Creation du tableau de jeu initial
def cree_tableau():
    tableau = np.zeros((nbRow,nbColums))
    return (tableau)

#Choix de la colonne à jouer(Pour le joueur la première colonne aura pour index=1)
def choixJeu(tableau) : 
    possible=False
    while possible!=True :
        colum_jouer=int(input("Entrez la colonne que vous voulez jouer : "))-1
        if (colum_jouer<nbColums) and (colum_jouer>=0) and tableau[0][colum_jouer]==0.0:
            possible=True
        else : 
            print("La colonne est pleine jouer une autre colonne."+"\n")
    return colum_jouer
def choixJeuAleatoire(tableau) : 
    possible=False
    while possible!=True :
        colum_jouer=np.random.randint(0,nbColums)
        if (colum_jouer<nbColums) and (colum_jouer>=0) and tableau[0][colum_jouer]==0.0:
            possible=True
        else : 
            print("La colonne est pleine jouer une autre colonne."+"\n")
    return colum_jouer

#Ajoute un i jeton au tableau
def ajouterPiece(tableau,col,piece):
    i=nbRow-1
    while tableau[i][col]!=0 :
        i-=1
    tableau[i][col]=piece

#Determine si c'est un winning move
def winning_move(tableau,player):

    #Verifie si 4 pieces sont alignées en ligne
    
    for l in range(nbRow-3):
        for c in range(nbColums):
            if(tableau[l][c]==tableau[l+1][c]==tableau[l+2][c]==tableau[l+3][c]==player) : 
                return True

    #Verifie si 4 pieces sont alignées en colonne
    
    for c in range(nbColums-3):
        for l in range(nbRow):
            if (tableau[l][c]==tableau[l][c+1]==tableau[l][c+2]==tableau[l][c+3]==player) : 
                return True

    #Verifie si 4 pieces sont alignées en diagonal inverse(\)
    
    for c in range(nbColums-3):
        for l in range(3,nbRow-3):
            if tableau[l][c]==tableau[l+1][c+1]==tableau[l+2][c+2]==tableau[l+3][c+3]==player : 
                return True
    
    #Verifie si 4 pieces sont alignées en diagonal (/)
    
    for c in range(nbColums-3):
        for l in range(3,nbRow):
            if (tableau[l][c]==tableau[l-1][c+1]==tableau[l-2][c+2]==tableau[l-3][c+3]==player) : 
                return True

###Creation des graphiques avec pygame :

###Creation des graphiques avec pygame :

def event():
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT :
            pygame.quit()
        if event.type==pygame.MOUSEBUTTONDOWN :
            position=int(event.pos[0]//100)
            print(position)
            
current_coup= 0 

def grille ():                   
    #Taille de la grille 
    element_grille=100
    width_grille=100*(nbColums)
    height_grille=100*(nbRow+1)
    size=(width_grille,height_grille)
    moitie_element=int(element_grille/2)
    rayon=moitie_element-6

    #Initialise et Affiche la fenetre
    pygame.init() 
    screen= pygame.display.set_mode(size)
    for c in range(nbColums):
        for l in range(1,nbRow+1):
            pygame.draw.rect(screen,Bleu,(c*element_grille,l*element_grille,
                             element_grille,element_grille) )
            pygame.draw.circle(screen,Noir,(int(c*element_grille+moitie_element),int(l*element_grille+moitie_element)),rayon)
            pygame.display.update()
    while current_coup<=nbCoupMax : 
        event()  



def puissance4():
    
    grille()
    #Initialisation du jeu 
    is_winner = False
    tableau=cree_tableau()
    current_coup= 0
    player=handle()
    print(tableau)

    while current_coup<=nbCoupMax: 
        current_coup+=1
        if player==1 :
            col_choise=choixJeu(tableau)
            ajouterPiece(tableau,col_choise,player)
            
        else :
            col_choise=choixJeuAleatoire(tableau)
            ajouterPiece(tableau,col_choise,player)
            
        print(tableau)
        if winning_move(tableau,player) : 
            break
        player=player%2 + 1 
        
    print(f'Player {int(player)} a gagné en {current_coup} coups')
        

if __name__ == "__main__":
    puissance4()
    

    




    
        

    


 

    
    

