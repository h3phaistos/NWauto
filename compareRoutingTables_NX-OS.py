#!/usr/bin/python
import re
import sys

class routeEntry:

	def __init__(self, protocol, prefix, nexthop, nexthop2):
		self.protocol = protocol
		self.prefix = prefix
		self.nexthop = nexthop
		self.nexthop2 = nexthop2

class changedRouteEntry:

	def __init__(self, protocol, prefix, oldNexthop, newNexthop, oldNexthop2, newNexthop2):
		self.protocol = protocol
		self.prefix = prefix
		self.oldNexthop = oldNexthop
		self.newNexthop = newNexthop
		self.oldNexthop2 = oldNexthop2
		self.newNexthop2 = newNexthop2

# Creation des listes vide pour stocker les tables de routage pre et post check 
preRouteEntry_List = []
postRouteEntry_List = []

# Recup les path des fichiers en argument
preFilePath = sys.argv[1]
postFilePath = sys.argv[2]

# Ouvre les fichiers dont le path est en argument
preFile = open(preFilePath, "r")
postFile = open(postFilePath, "r")

#####################################
# Boucle pour peupler la list preOPE#
#####################################

routeType = None
prefix = None
nexthop = None
nexthop2 = None
multiPath = None
i = 0

for preLine in preFile:

	if re.search('subnetted', preLine):
		continue

	if re.search('Gateway of last resort is', preLine):
		continue	

#
# Si tous les infos protocol prefix nexthop1 sont sur la meme ligne -- elles sont matchees dans ce if
#

	if re.search (r'(?P<routeType>^(L|C|S|R|M|B|D|EX|O|IA|N1|N2|E1|E2|i|su|L1|L2|ia|\*|U|o|P|H|l|\+|\%)\*{0,1})\s*(?P<Prefix>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[\/|0-9]{0,3})', preLine):
		routeType = re.search(r'(?P<routeType>^(L|C|S|R|M|B|D|EX|O|IA|N1|N2|E1|E2|i|su|L1|L2|ia|\*|U|o|P|H|l|\+|\%)\*{0,1})\s*(?P<Prefix>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[\/|0-9]{0,3})', preLine).group('routeType')
		prefix = re.search(r'(?P<routeType>^(L|C|S|R|M|B|D|EX|O|IA|N1|N2|E1|E2|i|su|L1|L2|ia|\*|U|o|P|H|l|\+|\%)\*{0,1})\s*(?P<Prefix>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[\/|0-9]{0,3})', preLine).group('Prefix')
		nexthop = 'None'
		nexthop2 = 'None'
		multiPath = False

		if re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', preLine):
			nexthop = re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', preLine).group(0)
			multiPath = True
			preRouteEntry_List.append(routeEntry(routeType, prefix, nexthop, nexthop2))
			i = i + 1
		
		if re.search('is directly connected', preLine):
			nexthop = "Connected"
			nexthop2 = 'None'
			multiPath = False
			preRouteEntry_List.append(routeEntry(routeType, prefix, nexthop, nexthop2))
			i = i + 1

#
# Si le nexthop est sur la ligne suivante -- matches dans les elif
#

# si c'est un 2eme nexthop
	elif re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', preLine) and multiPath == True:
		nexthop2 = re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', preLine).group(0)
		multiPath = False
		preRouteEntry_List[i-1].nexthop2 = nexthop2

# Si c'est le premier nexthop
	elif re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', preLine) and multiPath == False:
		nexthop = re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', preLine).group(0)
		nexthop2= 'None'
		multiPath = False
		preRouteEntry_List.append(routeEntry(routeType, prefix, nexthop, nexthop2))
		i = i + 1

	elif re.search('is directly connected', preLine):
		nexthop = "Connected"
		nexthop2 = 'None'
		multiPath = False
		preRouteEntry_List.append(routeEntry(routeType, prefix, nexthop, nexthop2))
		i = i + 1

	else:
		continue


# for elt in preRouteEntry_List:
#  	print ('Type : ' + elt.protocol.ljust(11) + elt.prefix.ljust(25) + "Nexthop : " + elt.nexthop.ljust(34) + "Nexthop 2 : " + elt.nexthop2)

# print ("# Number of routes before operation: ".ljust(40) + str(len(preRouteEntry_List)) + " routes")


# #####################################
# #Boucle pour peupler la list postOPE#
# #####################################

routeType = None
prefix = None
nexthop = None
nexthop2 = None
multiPath = None
j = 0

for postLine in postFile:

	if re.search('subnetted', postLine):
		continue

	if re.search('Gateway of last resort is', postLine):
		continue	

#
# Si tous les infos protocol prefix nexthop1 sont sur la meme ligne -- elles sont matchees dans ce if
#

	if re.search (r'(?P<routeType>^(L|C|S|R|M|B|D|EX|O|IA|N1|N2|E1|E2|i|su|L1|L2|ia|\*|U|o|P|H|l|\+|\%)\*{0,1})\s*(?P<Prefix>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[\/|0-9]{0,3})', postLine):
		routeType = re.search(r'(?P<routeType>^(L|C|S|R|M|B|D|EX|O|IA|N1|N2|E1|E2|i|su|L1|L2|ia|\*|U|o|P|H|l|\+|\%)\*{0,1})\s*(?P<Prefix>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[\/|0-9]{0,3})', postLine).group('routeType')
		prefix = re.search(r'(?P<routeType>^(L|C|S|R|M|B|D|EX|O|IA|N1|N2|E1|E2|i|su|L1|L2|ia|\*|U|o|P|H|l|\+|\%)\*{0,1})\s*(?P<Prefix>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[\/|0-9]{0,3})', postLine).group('Prefix')
		nexthop = 'None'
		nexthop2 = 'None'
		multiPath = False

		if re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', postLine):
			nexthop = re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', postLine).group(0)
			multiPath = True
			postRouteEntry_List.append(routeEntry(routeType, prefix, nexthop, nexthop2))
			j = j + 1
		
		if re.search('is directly connected', postLine):
			nexthop = "Connected"
			nexthop2 = 'None'
			multiPath = False
			postRouteEntry_List.append(routeEntry(routeType, prefix, nexthop, nexthop2))
			j = j + 1

#
# Si le nexthop est sur la ligne suivante -- matches dans les elif
#

# si c'est un 2eme nexthop
	elif re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', postLine) and multiPath == True:
		nexthop2 = re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', postLine).group(0)
		multiPath = False
		postRouteEntry_List[j-1].nexthop2 = nexthop2

# Si c'est le premier nexthop
	elif re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', postLine) and multiPath == False:
		nexthop = re.search(r'(?<=via )[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', postLine).group(0)
		nexthop2= 'None'
		multiPath = False
		postRouteEntry_List.append(routeEntry(routeType, prefix, nexthop, nexthop2))
		j = j + 1

	elif re.search('is directly connected', postLine):
		nexthop = "Connected"
		nexthop2 = 'None'
		multiPath = False
		postRouteEntry_List.append(routeEntry(routeType, prefix, nexthop, nexthop2))
		j = j + 1

	else:
		continue


# for elt in postRouteEntry_List:
#  	print ('Type : ' + elt.protocol.ljust(11) + elt.prefix.ljust(25) + "Nexthop : " + elt.nexthop.ljust(34) + "Nexthop 2 : " + elt.nexthop2)

# print ("# Number of routes before operation: ".ljust(40) + str(len(postRouteEntry_List)) + " routes")


###############################
# Comparaison des deux listes #
###############################

missingRouteEntry_List = []
newRouteEntry_List = []
changedRouteEntry_List = []
for x, preElt in enumerate(preRouteEntry_List):
	exists = False

	for y, postElt in enumerate(postRouteEntry_List):
		# Si les subnets sont identiques - le subnet existe
		if postElt.prefix == preElt.prefix:

# Si le prefix existe dans pre et post list on regarde si les nexthops sont les memes. s il ne sont pas les memes on inscrit le prefix dans la liste
# de changed routes 
# Si on trouve le prefix dans les deux listes on set exists = true pour savoir a la fin d iteration de la seconde boucle si le prefix a ete trouve
# Si exists est toujours = False on inscrit le prefix dans la liste missing prefix
			
			# Si les nexthops sont differents 
			if preElt.nexthop != postElt.nexthop or preElt.nexthop2 != postElt.nexthop2:
				exists = True
				changedRouteEntry_List.append(changedRouteEntry(preElt.protocol, preElt.prefix, preElt.nexthop, postElt.nexthop, preElt.nexthop2, postElt.nexthop2))
#				print (x, y, preElt.prefix)

			# Si les nexthop sont identiques
			if preElt.nexthop == postElt.nexthop and preElt.nexthop2 == postElt.nexthop2:
				exists = True

	# Si le prefix n'a pas ete trouve dans la liste post on l ajoute a la liste missing 
	if exists == False:
		missingRouteEntry_List.append(preElt)

# Boucles imbriquee dans l autre sens pour trouver si des routes ont ete ajoutees
for postElt in postRouteEntry_List:
	exists = False
	for preElt in preRouteEntry_List:
		# Si les subnets sont identiques - le subnet existe
		if preElt.prefix == postElt.prefix:
			exists = True

	# Si le prefix n'a pas ete trouve dans la liste pre on l ajoute a la liste new route 
	if exists == False:
		newRouteEntry_List.append(postElt)


###########################
# Affichage des resultats #
###########################
print " "
print ("# Number of routes before operation: ".ljust(40) + str(len(preRouteEntry_List)) + " routes")
print ("# Number of routes after operation: ".ljust(40) + str(len(postRouteEntry_List)) + " routes")
print " "

# Regarde si les 3 listes sont vides - les fichiers sont identiques
if len(changedRouteEntry_List) == 0 and len(missingRouteEntry_List) == 0 and len(newRouteEntry_List) == 0:
	print " -o- No differences -o-"
print " "

# Affiche la liste de changed route s il y en a
if len(changedRouteEntry_List) != 0:
	print (" !!! These routes have changed: !!!")	
	print ("-----------------------------------")
	for changedRoute in changedRouteEntry_List:
		print ('** Type : ' + changedRoute.protocol.ljust(10) + changedRoute.prefix.ljust(25) + " Previous Nexthop : " + changedRoute.oldNexthop.ljust(25) + "Current Nexthop : " + changedRoute.newNexthop)

		if changedRoute.oldNexthop2 != 'None' or changedRoute.newNexthop2 != 'None':
			print ("".ljust(46) + "Previous Nexthop 2 : " + changedRoute.oldNexthop2.ljust(23) + "Current Nexthop 2 : " + changedRoute.newNexthop2)
		print " "

# Affiche la liste de missing route s il y en a
if len(missingRouteEntry_List) != 0:
	print (" !!!!!! These routes are missing: !!!!!!")	
	print ("----------------------------------------")
	for missingRoute in missingRouteEntry_List:
		print ('-- Type : ' + missingRoute.protocol.ljust(11) + missingRoute.prefix.ljust(25) + "Nexthop : " + missingRoute.nexthop.ljust(34) + "Nexthop 2 : " + missingRoute.nexthop2)
		print " "

# Affiche la liste de new route s il y en a
if len(newRouteEntry_List) != 0:
	print ("These routes have been added:")
	print ("----------------------------")

	for addedRoute in newRouteEntry_List:
		print ('++ Type : ' + addedRoute.protocol.ljust(11) + addedRoute.prefix.ljust(25) + "Nexthop : " + addedRoute.nexthop.ljust(34) + "Nexthop 2 : " + addedRoute.nexthop2)
		print " "



