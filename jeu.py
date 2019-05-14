from tkinter import *
import random
import sys
import time

from const import *
import collision

""" Variables globales """
deplacements_en_cours = {}
perso = None
diminution = 0
largeur_trou = 50
acceleration = 0
vitesse_perso = 10


def close():
	print("fin")
	sys.exit(1)


def init_barre_horizontale(x1_trou, y, couleur="grey"):
	canvas.create_rectangle(0, y, LARGEUR_ECRAN, y + HAUTEUR_BARRE, fill=couleur, outline="", tags="BARRE_HORIZ")
	id_trou = canvas.create_rectangle(x1_trou, y, x1_trou + largeur_trou, y + HAUTEUR_BARRE, fill="black", outline="", tags="TROU")
	return id_trou


def init_jeu():
	global deplacements_en_cours
	global perso
	
	# On vide le dictionnaire des fonctions en cours d'execution
	deplacements_en_cours = {}

	# On supprime les anciennes barres et le perso s'ils existent
	for elem in canvas.find_all():
		canvas.delete(elem)

	# coordonnées et taille du perso
	perso = canvas.create_oval((LARGEUR_ECRAN)/2, 800, (LARGEUR_ECRAN)/2 + LARGEUR_PERSO,800 + HAUTEUR_PERSO, fill="yellow", outline="", tags="PERSO")
	
	positionX = 100
	positionY = 770
	

	for i in range (10):
		c = random.randint(0,8)
		sens = random.randint(0,1)
		couleur = ["green","yellow","red","blue","purple","brown","grey","white","orange"]
		id_trou = init_barre_horizontale(positionX, positionY, couleur[c])
		deplacement_trou(positionX, sens, id_trou)
		positionY -= 80
		positionX += 100

    # On place le perso au premier plan pour qu'il apparaisse au dessus des barres et des trous
	canvas.tag_raise("PERSO")


def perdu():
	print("game over\n")

	# Stoppe tous les déplacements en cours
	for id_fct in deplacements_en_cours.keys():
		id_fct_en_cours = deplacements_en_cours[id_fct]
		fenetre_principale.after_cancel(id_fct_en_cours)

	# Demande si on veut rejouer une partie
	codeRetour.set(0)
	rejouer(fenetre_principale)
	choix = codeRetour.get()
	if choix == REJOUER:
		init_jeu()
	elif choix == QUITTER:
		close()

def rejouer(fenetre_principale):

	fenetre_menu = Toplevel(bg = "blue", width = 200, height= 250, padx = 200, pady = 150)
	fenetre_menu.grab_set()
	fenetre_menu.focus_set()

	Bouton_Quitter = Button(fenetre_menu, text='QUITTER', command=quitter, bg='red')
	Bouton_Quitter.grid(row = 5, column = 4)

	Bouton_Rejouer = Button(fenetre_menu, text='JOUER', command=relancer, bg='green')
	Bouton_Rejouer.grid(row = 5, column = 7)
	
	Bouton_Rejouer = Button(fenetre_menu, text='JOUER', command=relancer, bg='green')

    # On se met en attente d'un changement de valeur de codeRetour
	fenetre_principale.wait_variable(codeRetour)

	choix = codeRetour.get()
	if choix == REJOUER:
		fenetre_menu.state('withdrawn')

def relancer():
	codeRetour.set(REJOUER)

def quitter():
	codeRetour.set(QUITTER)


def deplacement_trou(x1_trou, sens, id_trou):
	# Pour que la vitesse de déplacement soit un peu aleatoire

	x2_trou = x1_trou + largeur_trou

	if x2_trou + PADX + acceleration < LARGEUR_ECRAN and sens == 1:
		canvas.move(id_trou, PADX + acceleration, 0)
		x1_trou += PADX + acceleration

	elif x2_trou + PADX + acceleration >= LARGEUR_ECRAN and sens == 1:
		sens = 0

	elif x1_trou - PADX - acceleration > 0 and sens == 0:
		canvas.move(id_trou, -(PADX + acceleration), 0)
		x1_trou -= (PADX+acceleration)

	elif x1_trou - PADX - acceleration <= 0 and sens == 0:
		sens = 1

	# On arrete l'execution de la fonction en cours
	if id_trou in deplacements_en_cours:
		id_fct_en_cours = deplacements_en_cours[id_trou]
		fenetre_principale.after_cancel(id_fct_en_cours)

	# On rappelle une fonction de deplacement
	id_fct = fenetre_principale.after(10, deplacement_trou, x1_trou, sens, id_trou)

	# On met a jour le dictionnaire des deplacements avec cette nouvelle fonction pour pouvoir la stopper a la fin
	deplacements_en_cours[id_trou] = id_fct

	if collision.test_choc(canvas) == CHOC:
		perdu()

def droite(event):
	canvas.move(perso, PADX*vitesse_perso, 0)
	if collision.test_choc(canvas) == CHOC:
		perdu()

def gauche(event):
	canvas.move(perso, -PADX*vitesse_perso, 0)
	if collision.test_choc(canvas) == CHOC:
		perdu()

def haut(event):
	canvas.move(perso, 0, -PADY*vitesse_perso)
	result = collision.test_choc(canvas)
	if result == CHOC:
		perdu()
	elif result == HAUT:
		difficulte()
		init_jeu()

def bas(event):
	canvas.move(perso, 0, PADY*vitesse_perso)
	if collision.test_choc(canvas) == CHOC:
		perdu()

def difficulte():
	global acceleration
	global diminution
	global largeur_trou
	if acceleration < 4:
		acceleration += 0.25
		diminution += 2
	else :
		diminution += 10
		largeur_trou -= diminution




""" Programme principal """
fenetre_principale = Tk()
codeRetour = IntVar()

canvas = Canvas(fenetre_principale, width = LARGEUR_ECRAN, height = HAUTEUR_ECRAN, bd=0, bg="black")
canvas.pack(padx=PADX, pady=PADY)

init_jeu()

canvas.bind_all('<Right>', droite)
canvas.bind_all('<Left>', gauche)
canvas.bind_all('<Up>', haut)
canvas.bind_all('<Down>', bas)
canvas.bind_all('<Escape>', close)

fenetre_principale.mainloop()


