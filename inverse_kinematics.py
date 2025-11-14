import math

def calculate_angles(x, y):
    """
    Calcule les angles d’articulation à partir des coordonnées X et Y.
    Retourne : (alpha, beta)
    alpha = angle à l’épaule, beta = angle au coude
    """
    # [À compléter plus tard avec les équations trigonométriques]
    alpha = 0.0
    beta = 0.0
    return alpha, beta


def cinematique_inverse(Ax, Ay, Cx, Cy, La, Lb):

    # (1) AC
    AC = math.sqrt((Ax - Cx)**2 + (Ay - Cy)**2)

    # (2) A_baseC : distance entre la projection de A sur l'axe des x et C
    A_baseC = math.sqrt((Ax - Cx)**2 + (Cy)**2)

    # (3) ∠BAC
    num = La**2 + AC**2 - Lb**2
    den = 2 * La * AC
    cos_BAC = num / den
    BAC = math.acos(cos_BAC)

    # (4) ∠ACB
    sin_ACB = (La * math.sin(BAC)) / Lb
    ACB = math.asin(sin_ACB)

    # (5) ∠YAC
    num = Ay**2 + AC**2 - A_baseC**2
    den = 2 * Ay * AC
    cos_YAC = num / den
    cos_YAC = max(-1.0, min(1.0, cos_YAC))
    YAC = math.acos(cos_YAC)

    # (6) α = ∠BAC + ∠YAC
    alpha = BAC + YAC

    # (7) β = ∠BAC + ∠ACB
    beta = BAC + ACB

    # Conversion en degrés
    alpha_deg = math.degrees(alpha)
    beta_deg = math.degrees(beta)

    return alpha_deg - 75, 150 - beta_deg