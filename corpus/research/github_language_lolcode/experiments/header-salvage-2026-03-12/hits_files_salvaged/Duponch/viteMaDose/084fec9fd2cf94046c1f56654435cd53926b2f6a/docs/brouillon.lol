Check - finir lampadaires (cones, orientation)
Check - ajouter fog
Check - découper CityManager
- color batiments pour séléction
- détails : allumer qu'une partie des fenetres
- afficher stats de debug : nombres de citoyens par statut
- mode debug par calques
- ajouter jours / semaines / mois / années
- gameplay basé beaucoup sur énènements à base d'info / choix au joueur via UI
- ajouter point rouge émissif sur antenne gratte ciel



- multijoueur comme clash of clan : on peut faire en sorte que des citoyens de ma ville aillent chez la ville d'un autre joueur (exemple voyage avion)
	- ressources (ou map) en commun partagées par plusieurs jouers / villes qui fait que si j'infecte un lac / réserve etc ça peut le niquer



- métro sous la ville


- bonheur, diminue auto (de 100 à 0)
	- le bonheur est fonction de la santé (bonheur = (santé + salaire) / 2)
- santé max diminue auto (de 100 à 0) 
- santé augmente auto jusqu'à santé max
- 4 statuts sanitaire (par rapport à santé max) : très bonne 75 à 100, bonne 50 à 75, mauvais 25 à 50, très mauvaise 0 à 25
- Ajouter notion économie : afficher ressource argent du maire + argent des golems (moyenne)
- Chaque golem a un compte de 100 dollars initial
- Le maire (joueur) a aussi un compte
- A midi les citoyens prennent un cacheton : +1 santé et -1 santé max et -1 dollar en compte du golem et +1 dans le compte du maire
- Tous les midi, tout le monde gagne 10 dollar (salaire du travail)



Utilisation de lengthSq() au lieu de distanceToSquared() pour réduire les allocations