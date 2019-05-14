from const import *
from tkinter import *

def association_trou_barre(canvas, y1_barre, y2_barre):
	liste_trous = canvas.find_withtag("TROU")

	# On cherche le trou correspondant a la barre dans la liste des trous du canvas
	for id_trou in liste_trous:
		(x1, y1, x2, y2) = canvas.coords(id_trou)
		if (y1 == y1_barre) and (y2 == y2_barre):
			return id_trou

	# Si on n'a pas trouvé de correspondance
	return None


def test_choc(canvas):
	liste_persos = canvas.find_withtag("PERSO")

	# Il n'y a qu'un seul perso à l'écran. On prend donc le premier de la liste
	id_perso = liste_persos[0]
	(x1_perso, y1_perso, x2_perso, y2_perso) = canvas.coords(id_perso)

	if x2_perso > LARGEUR_ECRAN or x1_perso < 0:
		print("GAME OVER: personnage hors du jeu")
        


	liste_barres = canvas.find_withtag("BARRE_HORIZ")

	for barre in liste_barres:
		(x1_barre, y1_barre, x2_barre, y2_barre) = canvas.coords(barre)

		# On cherche le trou correspondant a la barre
		id_trou = association_trou_barre(canvas, y1_barre, y2_barre)
		if id_trou == None:
			print("ERREUR: La barre n'a pas de trou !!!")
			sys.exit(1)
		else:
			(x1_trou, y1_trou, x2_trou, y2_trou) = canvas.coords(id_trou)

			if (y1_perso > y1_barre) and (y1_perso < y2_barre) or (y2_perso > y1_barre) and (y2_perso < y2_barre):
				if (x1_perso < x1_trou) or (x1_perso > x2_trou):
					# Le perso est en collision avec la barre
					#return CHOC
					continue

			elif (y1_perso < 0):
				# Le perso est arrivé en haut de l'écran
				return HAUT

			else:
				# Tout va bien pour cette barre
				continue

	return PAS_DE_CHOC
