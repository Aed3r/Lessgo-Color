import joueur

j = joueur.Joueur(123, 10, 10)


print("Le joueur", j.id, "est mort ?", j.isDead())
j.setDead(True)
print("Le joueur", j.id, "est mort ?", j.isDead())