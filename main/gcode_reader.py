from inverse_kinematics import cinematique_inverse
from Global_Variables import POS_X, POS_Y, LEN_B, LEN_E
from plot_figure import plot
import math

# f = open("circle_new.gcode", 'w')

def read_file(file_name):
    """
    Lit un fichier G-code et retourne les instructions sous forme de liste.
    
    Args:
        file_name: Nom du fichier G-code à lire
        
    Returns:
        list: Liste des instructions, chaque instruction étant une liste de mots
    """
    with open(file_name, 'r') as f:
        file_instructions = (str(f.read()).split("\n"))
    
    for i in range(len(file_instructions)): 
        file_instructions[i] = file_instructions[i].split()

    return file_instructions


def circle_generator(Cx=50, Cy=140, rayon=10, step=1):
    """
    Génère les coordonnées et angles pour dessiner un cercle.
    
    Args:
        Cx: Coordonnée X du centre
        Cy: Coordonnée Y du centre
        rayon: Rayon du cercle
        step: Pas entre les points
        
    Returns:
        tuple: (liste_coordonnes, liste_angles) - Coordonnées et angles correspondants
    """
    liste_coordonnes = []
    liste_angles = []

    # Demi-cercle supérieur
    p = Cx-rayon
    while p <= Cx+rayon:
        q = math.sqrt(rayon**2 - (p-Cx)**2) + Cy
        liste_coordonnes.append((p, q))
        p += step

    # Demi-cercle inférieur
    p = Cx+rayon
    while p >= Cx-rayon:
        q = -math.sqrt(rayon**2 - (p-Cx)**2) + Cy
        liste_coordonnes.append((p,q))
        p -= step

    # Conversion des coordonnées en angles via cinématique inverse
    for element in liste_coordonnes:
        alpha, beta = cinematique_inverse(POS_X, POS_Y, element[0], element[1], LEN_B, LEN_E)
        liste_angles.append((alpha, beta))

    return liste_coordonnes, liste_angles


def circles(filename, out_rayon, out_step, in_rayon = 10, in_step = 1, cx_in = POS_X, cy_out = POS_Y):
    """
    Génère un fichier G-code avec des cercles concentriques.
    
    Args:
        filename: Nom du fichier G-code à créer
        out_rayon: Rayon des cercles extérieurs
        out_step: Pas pour les cercles extérieurs
        in_rayon: Rayon du cercle intérieur
        in_step: Pas pour le cercle intérieur
        cx_in: Coordonnée X du centre
        cy_out: Coordonnée Y du centre
    """
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
    """
    Génère les angles pour dessiner un carré avec rotation.
    
    Args:
        Cx: Coordonnée X du centre
        Cy: Coordonnée Y du centre
        r: Demi-côté du carré
        theta: Angle de rotation en degrés
        step: Pas entre les points
        
    Returns:
        list: Liste des angles (alpha, beta) pour chaque point du carré
    """
    def CoordoneesDeRotation(x, y, Cx, Cy, theta):
        """Applique une rotation autour du centre (Cx, Cy)."""
        x_prime = Cx + (x-Cx)*math.cos(math.radians(theta))  - (y - Cy)*math.sin(math.radians(theta))
        y_prime = Cy + (x-Cx)*math.sin(math.radians(theta))  + (y - Cy)*math.cos(math.radians(theta))
        return x_prime, y_prime
    
    liste_coordonees = []
    liste_angles = []

    # Coordonnées haut gauche
    x = Cx - r
    y = Cy + r

    # Ligne verticale gauche
    while y >= Cy - r:
        liste_coordonees.append(CoordoneesDeRotation(x, y, Cx, Cy, theta))
        y -= step

    # Ligne horizontale basse
    y = Cy - r
    while x <= Cx + r:
        liste_coordonees.append(CoordoneesDeRotation(x, y, Cx, Cy, theta))
        x += step

    # Ligne verticale droite
    x = Cx + r
    while y <= Cy + r: 
        liste_coordonees.append(CoordoneesDeRotation(x, y, Cx, Cy, theta))
        y += step

    # Ligne horizontale haute
    y = Cy + r
    while x >= Cx - r: 
        liste_coordonees.append(CoordoneesDeRotation(x, y, Cx, Cy, theta))
        x -= step
    
    # Conversion des coordonnées en angles via cinématique inverse
    for element in liste_coordonees: 
        alpha, beta = cinematique_inverse(POS_X, POS_Y, element[0], element[1], LEN_B, LEN_E)
        liste_angles.append((alpha, beta))

    return liste_angles

def squares(filename, Cx, Cy, r, step):
    """
    Génère un fichier G-code avec des carrés à différentes rotations.
    
    Args:
        filename: Nom du fichier G-code à créer
        Cx: Coordonnée X du centre
        Cy: Coordonnée Y du centre
        r: Demi-côté du carré
        step: Pas entre les points
    """
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
