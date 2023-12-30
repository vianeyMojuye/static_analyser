import re


def check_block(bloc, pattern, program, warnings, errors):
    '''
      This Function is used to verify if the structure of a bloc is valid or not
      Args:
        bloc (str): represents the bloc to be tested. ex: 'points'
        pattern (str): represents the pattern or a struture that should be respected by the bloc
        program (str) :  entry program to be tested

      returns {True} if the bloc's representation follows the pattern
      else {False}
    '''
  # Vérification si il existe une seule instance de points dans le programme
    if len(re.findall(bloc + r'\s*\{', program)) > 1 :
      # print(len(re.findall(bloc + r'\s*\{', program)))
      errors.append(f"Erreur de structure: il existe plus d une '{bloc}' section : ")
      # return False
     # Vérification si il existe au moins une section move ou points
    if re.search(bloc +r'\s*\{', program) is None :
        errors.append("Erreur de structure: section '"+ bloc +"' manquante")
        # return False
    # Vérification si il existe une erreur dans la section
    if re.search(pattern, program) is None:
        errors.append("Erreur de syntaxe dans la section '"+bloc+"'")
        # return False

    return True

# Fonction pour vérifier la validité de la syntaxe du programme
def check_syntax(file_path, warnings, errors):
    '''
      This Function is used to check if the program is written aacording to the syntax of our language
      Args:
        program (str) :  entry program to be tested

      returns {str} : Message to specify if the syntax is correct or not

    '''

    print("\n*******  Verification de la syntaxe de votre programme manipulant des points du plan cartésien *******\n")
    with open(file_path) as file:
      program = file.read()

    # Définition des expressions régulières pour les déclarations de points et les instructions de déplacement
    points_pattern = r'points\s*\{\s*([A-Za-z]+\s*=\s*\(\s*-?\d+\s*,\s*-?\d+\s*\)\s*,?\s*)*}'
    move_pattern = r'move\s*\{\s*([A-Za-z]+\s*=\s*\(\s*-?\d+\s*,\s*-?\d+\s*\)\s*,?\s*)*}'
    constraints_pattern = r'constraints\s*\{\s*([A-Za-z]+\s*=\s*\[\s*(?:\s*(?:[\dA-Za-z\.]+\s*(?:[+\-*/]\s*[\dA-Za-z\.]+\s*)*)(?:<=?|>=?|==?)\s*(?:[\dA-Za-z\.]+\s*(?:[+\-*/]\s*[\dA-Za-z\.]+\s*)*)\s*,?\s*)+\s*\]\s*,?\s*)*}'


    # Expression régulière pour la structure points puis move puis constraints
    pointsthenmove = r'points\s*{.*?},\s*.*?\s*move\s*{.*?},\s*.*?\s*constraints\s*{.*?}'


     # Expression régulière pour vérifier s'il y a du texte a l exterieur des blocs points et move
    pattern = r'\s*start:\s*points\s*{.*?},\s*move\s*{.*?},\s*constraints\s*{.*?}\s*end;'

    # Recherche de la structure dans le programme
    if  re.search(pattern, program, re.DOTALL) is None :
          errors.append("Erreur Syntaxe: syntaxe incorrecte ou Texte supplémentaire trouvé en dehors des blocs points, move et constraints.")
    # Recherche de la structure dans le programme
    if  re.search(pattern, program, re.DOTALL) is None :
      # Recherche de la structure dans le programme
      if re.search(pointsthenmove, program, re.DOTALL) is None:
        errors.append("Erreur Syntaxe ou structure invalide.\nIl se peut que l'ordre de denition des blocs soit ne soit pas  respecte.\nLes blocs doivent etre defini de la facon suivante: Points{...}, move{...}, constraints{...} ")
       # Vérification des expressions régulières pour le programme complet
      if not (re.match(r'^\s*start:', program) and re.search(r'end;$', program)):
        errors.append("Erreur de structure: 'start:' ou 'end;' manquants")
      #Bloc's verification
      check_block("points", points_pattern, program,warnings, errors)
      check_block("move", move_pattern, program,warnings, errors)
      check_block("constraints", constraints_pattern, program,warnings, errors)

    else:
       #Bloc's verification
      if not((check_block("points", points_pattern, program,warnings, errors) and check_block("move", move_pattern, program,warnings, errors) and check_block("constraints", constraints_pattern, program,warnings, errors))):
          # return "Syntaxe du programme invalide."
          pass
    # return "Syntaxe du programme valide."

# Fonction pour retourner le resultat de la verification
def result(errors, warnings):
      
      if(len(errors) == 0 and len(warnings)==0):
         print("\n\n Syntaxe du code correct \n")
      else :
          for w in warnings:
            print("Warnings ", w)
          for e in errors:
            print("Errors ", e)





