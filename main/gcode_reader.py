from math import sqrt
from inverse_kinematics import cinematique_inverse2
from Global_Variables import POS_X, POS_Y, LEN_B, LEN_E
from plot_figure import plot

# f = open("circle_new.gcode", 'w')

def read_file(file_name):
    with open(file_name, 'r') as f:
        file_instructions = (str(f.read()).split("\n"))
    
    for i in range(len(file_instructions)): 
        file_instructions[i] = file_instructions[i].split()

    return file_instructions


def circle_gcode_generator(Cx=50, Cy=140, rayon=10, step=1):
    """equation du cercle avec centre (p,q) (x-p)^2 + (y-q)^2 = r^2
    centre qui suit un mouvement circulaire 
    
    si le centre suit un mouvement circlaire, c'est une equation de la forme (p - a)^2 + (q - b)^2 = c^2
    p =  coordonnees horizontal du cercle directeur (l'axe circulaire), coordonne x du centre de chaque cercle sur l'axe circulaire
    q = coordonnees vertical du cercle directeur (l'axe circulaire), coordonne y du centre de chaque cercle sur l'axe circulaire
    Cx = coordonnee x du centre du cercle (l'axe circulaire)
    Cy = coordonnee y du centre du cercle (l'axe circulaire)
    rayon = rayon du cercle"""


    liste_coordonnes = []
    liste_angles = []

    p = Cx-rayon
    while p <= Cx+rayon:
        q = sqrt(rayon**2 - (p-Cx)**2) + Cy
        liste_coordonnes.append((p, q))
        p += step

    p = Cx+rayon
    while p >= Cx-rayon:
        q = -sqrt(rayon**2 - (p-Cx)**2) + Cy
        liste_coordonnes.append((p,q))
        p -= step

    for element in liste_coordonnes:
        alpha, beta = cinematique_inverse2(POS_X, POS_Y, element[0], element[1], LEN_B, LEN_E)
        liste_angles.append((alpha, beta))

    return liste_coordonnes, liste_angles


def beauty(out_rayon, out_step, in_rayon = 10, in_step = 1, cx_in = POS_X, cy_out = POS_Y):
    liste_coordonnes = circle_gcode_generator(Cx=cx_in, Cy=cy_out, rayon=in_rayon, step=in_step)[0]
    f = open("circle_new.gcode", 'w')
    for i in liste_coordonnes:
        angles = circle_gcode_generator(i[0], i[1], out_rayon, out_step)[1]
        f.write(f"M3\n")
        f.write(f"G1 S{angles[0][0]} E{angles[0][1]} \n")
        f.write(f"M5\n")

        for element in angles:
            f.write(f"G1 S{element[0]} E{element[1]} \n")
        f.write(f"M3\n")
    f.close()


        
if __name__ == "__main__":
    beauty(50, 0.1, 50, 10, 150, 140)
    plot()

