import syntax as s
import point as pt

if __name__ == "__main__":
    file_path = './program/progr1.txt'
    warnings =[]
    errors = []
    s.check_syntax(file_path,warnings, errors)
    
   ##########################################################################
    try:
        file = pt.read_file(file_path,warnings, errors)
    except ValueError as e :
        print(e)
    else:
        # Reading file and creation of points
        points = pt.create_points(file[0],file[1], file[2],warnings, errors )
    
    s.result(errors, warnings)

    if(len(errors) == 0 and len(warnings)==0):
        pt.draw_polyhedra(points)