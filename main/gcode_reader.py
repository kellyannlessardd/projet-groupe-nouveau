from inverse_kinematics import cinematique_inverse
from Global_Variables import POS_X, POS_Y, LEN_B, LEN_E
from plot_figure import plot
import math

# f = open("circle_new.gcode", 'w')

def read_file(file_name):
    with open(file_name, 'r') as f:
        file_instructions = (str(f.read()).split("\n"))
    
    for i in range(len(file_instructions)): 
        file_instructions[i] = file_instructions[i].split()

    return file_instructions


def circle_generator(Cx=50, Cy=140, rayon=10, step=1):
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
        q = math.sqrt(rayon**2 - (p-Cx)**2) + Cy
        liste_coordonnes.append((p, q))
        p += step

    p = Cx+rayon
    while p >= Cx-rayon:
        q = -math.sqrt(rayon**2 - (p-Cx)**2) + Cy
        liste_coordonnes.append((p,q))
        p -= step

    for element in liste_coordonnes:
        alpha, beta = cinematique_inverse(POS_X, POS_Y, element[0], element[1], LEN_B, LEN_E)
        liste_angles.append((alpha, beta))

    return liste_coordonnes, liste_angles


def circles(filename, out_rayon, out_step, in_rayon = 10, in_step = 1, cx_in = POS_X, cy_out = POS_Y):
    liste_coordonnes = circle_generator(Cx=cx_in, Cy=cy_out, rayon=in_rayon, step=in_step)[0]
    f = open(filename, 'w')
    for i in liste_coordonnes:
        angles = circle_generator(i[0], i[1], out_rayon, out_step)[1]
        f.write(f"M3\n")
        f.write(f"G1 S{angles[0][0]} E{angles[0][1]} \n")
        f.write(f"M5\n")

        for element in angles:
            f.write(f"G1 S{element[0]} E{element[1]} \n")
        f.write(f"M3\n")
    f.close()


def square_generator(Cx, Cy, r, theta, step):
    def prime(x, y, Cx, Cy, theta):
        x_prime = Cx + (x-Cx)*math.cos(math.radians(theta))  - (y - Cy)*math.sin(math.radians(theta))
        y_prime = Cy + (x-Cx)*math.sin(math.radians(theta))  + (y - Cy)*math.cos(math.radians(theta))
        return x_prime, y_prime
    
    liste_coordonees = []
    liste_angles = []

    # coordonees haut gauche
    x = Cx - r
    y = Cy + r

    # Ligne vertical gauche
    while y >= Cy - r:
        liste_coordonees.append(prime(x, y, Cx, Cy, theta))
        y -= step

    # Ligne horizontal basse
    y = Cy - r
    while x <= Cx + r:
        liste_coordonees.append(prime(x, y, Cx, Cy, theta))
        x += step

    # Ligne vertical droite
    x = Cx + r
    while y <= Cy + r: 
        liste_coordonees.append(prime(x, y, Cx, Cy, theta))
        y += step

    # Ligne horizontal haute
    y = Cy + r
    while x >= Cx - r: 
        liste_coordonees.append(prime(x, y, Cx, Cy, theta))
        x -= step
    
    for element in liste_coordonees: 
        alpha, beta = cinematique_inverse(POS_X, POS_Y, element[0], element[1], LEN_B, LEN_E)
        liste_angles.append((alpha, beta))

    return liste_angles

def squares(filename, Cx, Cy, r, step):
    f = open(filename, 'w')
    for theta in range(0, 90, 5):
        angles = square_generator(Cx, Cy, r, theta, step)
        f.write(f"M3\n")
        f.write(f"G1 S{angles[0][0]} E{angles[0][1]} \n")
        f.write(f"M5\n")
        for i in angles:
            f.write(f"G1 S{i[0]} E{i[1]} \n")
        f.write(f"M5\n")
    f.close()
        
if __name__ == "__main__":
    # circles("self_plot.gcode", 50, 1, 50, 10, 125, 150)
    # plot("self_plot.gcode")
    squares("self_plot.gcode", 50, 100, 10, 2)
    plot("self_plot.gcode")

