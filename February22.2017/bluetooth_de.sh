#!/bin/bash


# Comment utiliser un bluetooth serial  avec rfcom
#
#  utiliser bluetoothctl pour faire un pair avec le bluetooth
#
#  sudo bluetoothctl
#  scan on            -> ceci va lister tout les bluetooths visibles
#                     -> chercher  le nom du bluetooth  et prener son MAC
#  agent on           -> ceci va permettre de d'entrer le mot de passe lors du pair
#  pair  MAC_ADRESS   -> Pour faire le pair  il faut cette commande  avec le MAC du bluetooth specifique
#                     -> Le mot de passe pour le bluetooth
# et voila!

#maintenant il sagit de creer un device  serie

/usr/bin/rfcomm bind /dev/rfcomm1 00:12:06:20:94:53 1

#Le /dev/rfcomm1 devrait exister pour le bluetooth 
#PS ne pas oublier d'utiliser le bon MAC address.
