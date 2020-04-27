#Ce programme vise à creer un puissance 4 avec une IA basée sur l'algorithme MinMax

#Implémentation des modules
import numpy as np
import math
import random

#Taille du jeu
nbRow=6
nbColums=12
nbCoupMax=42

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

def valid_col(tableau,col):
    return tableau[0][col] == 0

#Determine si c'est un winning move
def coup_gagnant(tableau,player):

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

###Module D'AI
#Charactere des joueurs
case_vide=0
PLAYER_PIECE=1
AI_PIECE=2

#Definit les cas d'arret du jeu
def is_finish(board,current_coup):
	return coup_gagnant(board, PLAYER_PIECE) or coup_gagnant(board, AI_PIECE) or current_coup==nbCoupMax

#Prend un rectangle de 4 jetons et evalue le score de chaque rectangle dans la grille
def heuristique(rectange, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if rectange.count(piece) == 4:
		score += 100
	elif rectange.count(piece) == 3 and rectange.count(case_vide) == 1:
		score += 5
	elif rectange.count(piece) == 2 and rectange.count(case_vide) == 2:
		score += 2

	if rectange.count(opp_piece) == 3 and rectange.count(case_vide) == 1:
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
			score += heuristique(rectange, piece)

	## Score Vertical
	for c in range(nbColums):
		col_array = [int(i) for i in list(board[:,c])]
		for l in range(nbRow-3):
			rectange = col_array[l:l+4]
			score += heuristique(rectange, piece)

	## Score sur les diagonales(/)et(\)
	for l in range(nbRow-3):
		for c in range(nbColums-3):
			rectange = [board[l+i][c+i] for i in range(4)]
			score += heuristique(rectange, piece)

	for l in range(3,nbRow):
		for c in range(nbColums-3):
			rectange = [board[l-i][c+i] for i in range(4)]
			score += heuristique(rectange, piece)

	return score

#Récupère l'ensemble des colonnes jouables
def all_col_jouable(board):
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
		row = ligne_jouable(board, col)
		temp_board = board.copy()
		ajouterPiece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

#Regarde sur quel ligne de la colonne on peut jouer
def ligne_jouable(board, col):
	for r in range(nbRow):
		if board[r][col] == 0:
			return r

#Algorithme MinMax AlphaBeta
# Voir le premier Pseudo-Code WIKIPEDIA : https://fr.wikipedia.org/wiki/%C3%89lagage_alpha-b%C3%AAta#Pseudocode
#Video qui explique sinon : https://www.youtube.com/watch?v=f30Ry1WOe_Q
def minimax(board, depth, alpha, beta, maximizingPlayer,current_coup):
	valid_locations = all_col_jouable(board)
	is_terminal = is_finish(board,current_coup)
	if depth == 0 or is_terminal:
		if is_terminal:
			if coup_gagnant(board, AI_PIECE):
				return (None, 100000000000000)
			elif coup_gagnant(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Plus de jetons pour jouer respect des contraintes
				return (None, 0)
		else: # si ce n'est pas fini
			return (None, score_position(board, AI_PIECE))
    # Minimizing player
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = ligne_jouable(board, col)
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
			row = ligne_jouable(board, col)
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
def puissance4():
    #Initialisation du jeu   
    tableau=cree_tableau()
    is_winner=False
    current_coup= 0
    player=handle()
    print(tableau)

    while current_coup<=nbCoupMax: 
        current_coup+=1
        if player==1 :
            col_choise=choixJeu(tableau)
            ajouterPiece(tableau,col_choise,player)
            
        else :
            col_choise=minimax(tableau,4,-math.inf,math.inf,True,current_coup)[0]
            print(f"L'IA a joué la colonne {col_choise}")
            ajouterPiece(tableau,col_choise,player)
            
        print(tableau)
        if coup_gagnant(tableau,player) : 
            print(tableau)
            is_winner=True
            break
        player=player%2 + 1 
    if is_winner :    
        print(f'Player {int(player)} a gagné en {current_coup} coups')
    else :
        print("Il n'y a pas de gagnant")
        

if __name__ == "__main__":
    puissance4()
    

    




    
        

    


 

    
    

