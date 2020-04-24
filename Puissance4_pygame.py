#Ce programme vise à creer un puissance 4 avec une IA basée sur l'algorithme MinMax

#Implémentation des modules
import numpy as np
import math
import pygame
import random
import math


#Taille du jeu
nbRow=6
nbColums=12
nbCoupMax=30

#Couleur
Bleu=(0,0,254)
Noir=(0,0,0)
Rouge=(255,0,0)
Jaune=(244,244,0)
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

def valid_col(tableau,col):
    return tableau[0][col] == 0
#Choix de la colonne à jouer(Pour le joueur la première colonne aura pour index=1)
def choixJeu(tableau) : 
    possible=False
    while possible!=True :
        colum_jouer=int(input("Entrez la colonne que vous voulez jouer : "))-1
        if (colum_jouer<nbColums) and (colum_jouer>=0) and valid_col(tableau,colum_jouer):
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
        for l in range(nbRow-3):
            if tableau[l][c]==tableau[l+1][c+1]==tableau[l+2][c+2]==tableau[l+3][c+3]==player : 
                return True
    
    #Verifie si 4 pieces sont alignées en diagonal (/)
    
    for c in range(nbColums-3):
        for l in range(3,nbRow):
            if (tableau[l][c]==tableau[l-1][c+1]==tableau[l-2][c+2]==tableau[l-3][c+3]==player) : 
                return True

###Creation des graphiques avec pygame :
#Taille de la grille/ et Autres Constante
element_grille=100
width_grille=100*(nbColums)
height_grille=100*(nbRow)
size=(width_grille,height_grille)
moitie_element=int(element_grille/2)
rayon=moitie_element-6

#Retourne la colonne choisie par le joueur quand il click   
def event():
    position_col=0
    click=False
    while click==False:
        
        for event in pygame.event.get() : 
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN :
                position_col=int(event.pos[0]//100)
                click=True
    return position_col
            
#Mets à jour la grille    
def update_grille(screen,tableau):
    for c in range(nbColums):
            for l in range(nbRow):
                pygame.draw.rect(screen,Bleu,(c*element_grille,l*element_grille,
                                element_grille,element_grille) )
                pygame.draw.circle(screen,Noir,(int(c*element_grille+moitie_element),int(l*element_grille+moitie_element)),rayon)
                if tableau[l][c]==1:
                    pygame.draw.circle(screen,Rouge,(int(c*element_grille+moitie_element),int(l*element_grille+moitie_element)),rayon)
                if tableau[l][c]==2:
                    pygame.draw.circle(screen,Jaune,(int(c*element_grille+moitie_element),int(l*element_grille+moitie_element)),rayon)

                pygame.display.update()

###Module D'AI
#Charactere des joueurs
EMPTY=0
PLAYER_PIECE=1
AI_PIECE=2

#Definit les cas d'arret du jeu
def is_finish(board,current_coup):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or current_coup>nbCoupMax

#Prend un rectangle de 4 jetons et evalue le score de chaque rectangle dans la grille
def evaluateRectangle(rectange, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if rectange.count(piece) == 4:
		score += 100
	elif rectange.count(piece) == 3 and rectange.count(EMPTY) == 1:
		score += 5
	elif rectange.count(piece) == 2 and rectange.count(EMPTY) == 2:
		score += 2

	if rectange.count(opp_piece) == 3 and rectange.count(EMPTY) == 1:
		score -= 4

	return score

#On simule l'ajout d'un jeton dans la grille pour tester le score de celui-ci
def score_position(board, piece):
	score = 0
	## Score sur la colonne centrale
	center_array = [int(i) for i in list(board[:, nbColums//2])]
	center_count = center_array.count(piece)
    #Ici on previlégie de jouer au centre pour avoir plus d'opportunité par la suite
	score += center_count * 3

	## Score Horizontal
	for l in range(nbRow):
		row_array = [int(i) for i in list(board[l,:])]
		for c in range(nbColums-3):
			rectange = row_array[c:c+4]
			score += evaluateRectangle(rectange, piece)

	## Score Vertical
	for c in range(nbColums):
		col_array = [int(i) for i in list(board[:,c])]
		for l in range(nbRow-3):
			rectange = col_array[l:l+4]
			score += evaluateRectangle(rectange, piece)

	## Score sur les diagonales(/)et(\)
	for l in range(nbRow-3):
		for c in range(nbColums-3):
			rectange = [board[l+i][c+i] for i in range(4)]
			score += evaluateRectangle(rectange, piece)

	for l in range(3,nbRow):
		for c in range(nbColums-3):
			rectange = [board[l-i][c+i] for i in range(4)]
			score += evaluateRectangle(rectange, piece)

	return score

#Récupère l'ensemble des colonnes jouables
def get_valid_move(board):
	valid_locations = []
	for col in range(nbColums):
		if valid_col(board, col):
			valid_locations.append(col)
	return valid_locations

#On recupère la meilleur colonne apres la simulation 
def best_move(board, piece):
	valid_locations = (board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_row(board, col)
		temp_board = board.copy()
		ajouterPiece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

#Regarde sur quel ligne de la colonne on peut jouer
def get_row(board, col):
	for r in range(nbRow):
		if board[r][col] == 0:
			return r

#Algorithme MinMax AlphaBeta
def minimax(board, depth, alpha, beta, maximizingPlayer,current_coup):
	valid_locations = get_valid_move(board)
	is_terminal = is_finish(board,current_coup)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Plus de jetons pour jouer respect des contraintes
				return (None, 0)
		else: # si ce n'est pas fini
			return (None, score_position(board, AI_PIECE))

    # Voir le premier Pseudo-Code WIKIPEDIA : https://fr.wikipedia.org/wiki/%C3%89lagage_alpha-b%C3%AAta#Pseudocode
    #Video qui explique sinon : https://www.youtube.com/watch?v=f30Ry1WOe_Q

    # Minimizing player
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_row(board, col)
			b_copy = board.copy()
			ajouterPiece(b_copy, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False,current_coup)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column,value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_row(board, col)
			b_copy = board.copy()
			ajouterPiece(b_copy, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True,current_coup)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column,value

def puissance4 ():                   

    #Initialisation du jeu 
    is_winner = False
    tableau=cree_tableau()
    current_coup= 0
    player=handle()
    print(tableau)

    #Initialise et Affiche la fenetre
    pygame.init() 
    screen= pygame.display.set_mode(size)
    update_grille(screen,tableau)       
    
    #Prend en compte la contrainte du nombre de jetons
    while current_coup<=nbCoupMax  : 
        #Ajoute un jeton au compteur
        current_coup+=1
        
        #Choix du joueur 
        if player==1 :
            
            col_choise=event() 
            ajouterPiece(tableau,col_choise,player)
            update_grille(screen,tableau)   
        # Choix de l'IA
        else :
            col_choise=minimax(tableau,4,-math.inf,math.inf,True,current_coup)[0]
            ajouterPiece(tableau,col_choise,player)
            update_grille(screen,tableau)
        print(tableau)
        update_grille(screen,tableau)  
        if winning_move(tableau,player) :
            update_grille(screen,tableau)
            break   
        #Change la main IA <-> Joueur
        player=player%2 + 1 
        
    #Affiche le Vainqueur   
    myfont = pygame.font.SysFont("monospace", 42)

    # render text
    label = myfont.render(f'Player {int(player)} a gagné en {current_coup} coups', 1, (0,255,0))
    screen.blit(label, (200, height_grille//2))
    pygame.display.update()
    
    
    print(f'Player {int(player)} a gagné en {current_coup} coups')


 
        
        

if __name__ == "__main__":
    puissance4()

