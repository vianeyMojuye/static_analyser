# static_analyser
Analyse Statique d'un langage defini permettant de representer le polyedre correspondant a chaque point defini dans un plan cartesien.

- La syntaxe et Semantique du langage disponible dans le fichier Language_syntax.txt:
   vous y trouverez :
     . Un exemple de programme correct
     . La Syntaxe
     . La sémantique

Pour Executer le projet il faut: 
     Avoir installer une version python sur votre machine (3.10 et plus)
     -soit  cloner le projet sur votre machine
     -ou bien de telecharger la version ziper, puis le dezipper en local.
   Ensuite, il faut se positionner a la racine du projet ie :
        entrez dans le folder STATIC_ANALYSER
             puis lancer la commande python permettant d'executer le fichier main.py
                   ex: python main.py (sur windows)
   vous pouvez ouvrir le projet avec un outil  tel que vsCode puis executer le fichier main.py

Il Y a trois differents exemples de programme dans le folder program :
       - progr1.txt
       - progr2.txt
       - progr3.txt (seul programme ayant une syntaxe correct)
    
pour tester ces differents programmes, il suffit de modifier la ligne 5 du ficher main.py avant de lancer l'execution.
   ligne 5 :    
                
            file_path = './program/progr2.txt' pour analyser le progr2.txt
               
            file_path = './program/progr1.txt' pour analyser le progr1.txt

            file_path = './program/progr3.txt' pour analyser le progr3.txt
