import numpy as np
import matplotlib.pyplot as plt
import re


"""
   Class Point: Use to represent the coordinates and constraints of each point
"""
class Point:
    def __init__(self, name, coordinates, constraints):
        """
         Initialize an object point with coordinates and constraints
         Args:
           name (str) : Represent the name of the point
           coordinates (int,int) : coordinates (x,y) of the point ex: (1,0)
           constraints [string] : Contrainst applied on a point ex: ['X >=0 ', 'Y <5']

        """
        self.name = name
        self.coordinates = coordinates
        self.constraints = constraints

    def move(self, new_coordinates):
        """
         Move the point to another location : correspoding to new_coordinates
         or Updates the coordinates of each point
         Args:
           new_coordinates (int, int) :  new coordinate to be  assigned to the point ex : (2,2)

        """
        self.coordinates = new_coordinates

    def __str__(self):
        """
         Return a string representation of a point  with all the contrainsts related to it
           ex: Point A :  (1, 2) , constraint A : ['Y >= xdx1', 'Y <= 4', 'X >= 1', 'X <= 4', '2 * Y - X <= 6', '2 * Y - X >= 0', '2 * X + Y >= 4']

         Returns:
            str : Representation of a point with all the contrainsts related to it

        """
        return f"Point : '{self.name}', coordonates : {self.coordinates}, constraints : {self.constraints}"


def read_file(file_path, warnings, errors):
    """
        Reads the content of the file submitted to this program then extract informations
        present in the following blocs : points , move, and canstraint
        Args:
           file_path (str) : path of the file to be read
        Returns:
           dict, dict, dict :  points, moves, constraints

    """
    points = {}
    moves = {}
    constraints = {}
    reading_block = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("points{"):
                reading_block = "points"
            elif line.startswith("move{"):
                reading_block = "move"
            elif line.startswith("constraints{"):
                reading_block = "constraints"
            elif line.startswith("}"):
                reading_block = None
            elif reading_block:
                parts = line.split('=', maxsplit=1)
                #print(parts)
                if len(parts) == 2:
                    key, value = map(str.strip, parts)
                    # print( key,  value, '  ok')
                    value = value.rstrip(',')  # Remove trailing comma if present

                    if reading_block == "points":
                        # Remove parentheses and spaces, then split into coordinates
                        coordinates = tuple(map(int, value[1:-1].replace(' ', '').split(',')))
                        #verify if a point the name= key already exist
                        # print(points.keys() )
                        if key in points.keys() :
                            errors.append(f" ****** Warning !!! *****\nPoints: Duplication of variable name  '{key}' ")
                        points[key] = coordinates
                    elif reading_block == "move":
                        # Remove parentheses and spaces, then split into coordinates
                        new_coordinates = tuple(map(int, value[1:-1].replace(' ', '').split(',')))
                        moves[key] = new_coordinates
                    elif reading_block == "constraints":
                        # Remove square brackets and spaces, then split into expressions
                        expressions = [expr.strip() for expr in value[1:-1].replace(' ', '').split(',')]
                        if  key in constraints.keys():
                             
                             constraints[key]= constraints[key]+ expressions
                             
                        else :
                            constraints[key] = expressions
                #verify if the points present in the move block have already been declared in points block
                for m in moves.keys():
                     if not(m in points.keys()):
                        warnings.append(f" ****** Warning !!! *****\nMove: Variable name  '{m}'  is not declared in points block")
                #verify if the points present in the move block have already been declared in points block
                for c in constraints.keys():
                     if not(c in points.keys()):
                        warnings.append(f" ****** Warning !!! *****\nConstraints: Variable name  '{c}'  is not declared in points block")


    return points, moves, constraints

def has_duplicates(seq):
    seen = []
    unique_list = [x for x in seq if x not in seen and not seen.append(x)]
    return len(seq) != len(unique_list)



def eval_constraints(point,warnings, errors, old_constr):
    """
        evalue la liste de contraintes d'un, verifie si il n y a aucune incoherence: inegalité fausse 
                                                        contrainte contradictoire
        point (Point) : point à verifier 
        old_constr ([String]): liste des contraintes initiale(representation faite avant la substitution)
    
    """
    constraints = point.constraints
    c = []
    # Remplace les occurrences de X, Y, etc. par les valeurs correspondantes
    for expression in constraints :
        expression = expression.replace('X', str(point.coordinates[0]))
        expression = expression.replace('Y', str(point.coordinates[1]))
        c.append(expression)
    constraints = c
    for i in range(0, len(constraints)):
        try:
            resultat = eval(constraints[i])
            
            if not resultat:
                errors.append(f"Point: {point.name} - Erreur constraint: {old_constr[i]}.")
        except Exception as e:
            # En cas d'erreur d'évaluation (par exemple, division par zéro), considérez l'expression comme fausse.
            
            errors.append(f"Point: {point.name} - Error constraint: {old_constr[i]}")

    

def update_constraints(points,warnings, errors):
    """Updates the constraint expression of all the points defined in the program
       Args:
        points ([Point]) : list of all the points

    """
    for point in points:
        #recuperons la liste des contraintes avant la mise à jour
        old_constr = point.constraints
        # Met à jour chaque expression de contrainte pour le point
        point.constraints = [substitute_coordinates(expr, point, points,warnings, errors) for expr in point.constraints]
        # evaluons si la liste de contraintes est coherente: existe-t-il de contraintes contradictoires? ou de contraintes fausses?
        eval_constraints(point,warnings, errors, old_constr)
            
    

      
def create_points(points, moves, constraints,warnings, errors):
    """ Read a file , extract all the relavant information then creates points according to the class Point
        Args:
           points (dict) : list of points ex: ['A', '(1,2)']
           move (dict) : list ofe moves  ex: ['A', '(3,2)']
           constraints (dict) : list of constraints  ex: ['A', '[A.x > 5]']
        Returns:
            [Point] : list of points extracted
    """
    # print(points)
    # Créer des objets Point pour chaque point défini
    point_objects = []
    for point_name, coordinates in points.items():
        constraints_for_point = constraints.get(point_name, [])
        point_object = Point(point_name, coordinates, constraints_for_point)
        point_objects.append(point_object)


     #Appliquer les mouvements
    for point_name, new_coordinates in moves.items():
        for point_object in point_objects:
            if point_name == point_object.name:
                point_object.move(new_coordinates)


    # Afficher les informations pour chaque point
    # for point_object in point_objects:
    #     print(point_object)

    #Update the representation of each constraint's expression
    update_constraints( point_objects,warnings,errors)
    # Afficher les informations pour chaque point
    # print("############## After Updation \n")
    # for point_object in point_objects:
    #     print(point_object)


    return point_objects


def substitute_coordinates(expression, point, points,warnings, errors):
    """Updates the expression of each contrainst related to one point in the way that for the point A, A.x would be X A.y would be Y
          this is helpfull for the fonction that drows the polyhedra
       Args:
          expression (str) :  expression to be updated
          point (Point) : the concerned  point
          points ([Point]) : liste de tous les points
      Returns:
         (str) : updated expression

    """
    # Dictionnaire pour stocker les coordonnées de tous les points
    all_coordinates = {p.name: p.coordinates for p in points}

    # Remplace les occurrences de A.x, A.y, etc. par les valeurs correspondantes
    expression = expression.replace(f"{point.name}.x", 'X')
    expression = expression.replace(f"{point.name}.y", 'Y')

    # Remplace les occurrences de B.x, B.y, etc. par les valeurs correspondantes du point B
    for other_point in points:
        expression = expression.replace(f"{other_point.name}.x", str(other_point.coordinates[0]))
        expression = expression.replace(f"{other_point.name}.y", str(other_point.coordinates[1]))

    # Vérifie si des coordonnées inconnues (ex: C.x, C.y) existent dans l'expression
    unknown_coordinates = re.findall(r'[A-Za-z]+\.[xy]', expression)
    for unknown_coord in unknown_coordinates:
        if unknown_coord not in all_coordinates:
             errors.append(f"Erreur : La coordonnée {unknown_coord} n'est pas définie pour un point existant.")

     # Vérifie si des coordonnées autres que x et y sont présentes dans l'expression
    invalid_coords = re.findall(r'[A-Za-z]+\.[^xy]', expression)
    if invalid_coords:
        errors.append(f"Erreur : Les coordonnées {', '.join(invalid_coords)} ne peuvent pas être substituées.")



    return expression



def draw_polyhedra(point_objects):
    """Draws the polyhedra related to evrery point
       Args:
        point_objects ([Point]) : list of points to represent

    """

    points = []
    constraints = []
    # Afficher les informations pour chaque point
    for point_object in point_objects:
        print(point_object)
    for point_object in point_objects:
          points.append(point_object.coordinates)
          constraints.append(point_object.constraints)
          #  points = [(2, 3), (1, 6), (6,6)]
          #  constraints = [
          #       ["Y >= 1", "Y <= 4", "X >= 1", "X <= 4", "2 * Y - X <= 6", "2 * Y - X >= 0", "2 * X + Y >= 4"],  # Contraintes pour le point A
          #       ["X < 2", "X >= 1 ", "Y > 4", "Y <= 8 ", "2 * X - Y <= 6" ],  # Contraintes pour le point B
          #       ["X >= 5", "X <= 10 ", "Y >= 6", "Y <= 10 "],  # Contraintes pour le point c

          #   ]

    x_min, x_max, y_min, y_max = 0, 10, 0, 10  # Définir les limites du graphique
    x = np.linspace(x_min, x_max, 400)
    y = np.linspace(y_min, y_max, 400)
    X, Y = np.meshgrid(x, y)

    plt.figure(figsize=(8, 6))

    for point, constraint in zip(points, constraints):
        # Appliquer les contraintes pour chaque point
        region = np.ones_like(X, dtype=bool)
        for cond in constraint:
            region &= eval(cond)

        # Dessiner le polyèdre pour chaque point
        plt.imshow(region, extent=(x_min, x_max, y_min, y_max), origin='lower', alpha=0.3)
        plt.plot(*point, marker='o', markersize=10, label=f'Point {point}')

    plt.title('Polyèdres avec Contraintes')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.legend()
    plt.grid(True)
    plt.show()

