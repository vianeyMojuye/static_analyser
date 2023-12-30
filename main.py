import syntax as s

if __name__ == "__main__":
    file_path = './program/progr1.txt'
    warnings =[]
    errors = []
    s.check_syntax(file_path,warnings, errors)
    
    s.result(errors, warnings)

   ##########################################################################
#    try:
#      file = read_file(file_path,warnings, errors)
#    except ValueError as e :
#      print(e)
#    else:
#     # Reading file and creation of points
#     points = p.create_points(file[0],file[1], file[2],warnings, errors )

#     for w in warnings:
#         print(w)
#     for e in errors:
#         print(e)
#     # draw_polyhedra(points)