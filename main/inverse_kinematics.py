import math

def clamp(x):
    """
    Limite une valeur entre -1 et 1.
    
    Args:
        x: Valeur à limiter
        
    Returns:
        float: Valeur limitée entre -1 et 1
    """
    return max(-1, min(1, x))

def cinematique_inverse(Ax, Ay, Cx, Cy, La, Lb):
    """
    Calcule les angles alpha (épaule) et beta (coude) pour atteindre un point (Cx, Cy).
    
    Args:
        Ax: Coordonnée X du pivot
        Ay: Coordonnée Y du pivot
        Cx: Coordonnée X du point cible
        Cy: Coordonnée Y du point cible
        La: Longueur du bras arrière
        Lb: Longueur du bras avant
        
    Returns:
        tuple: (alpha, beta) - Angles en degrés pour l'épaule et le coude
    """
    dx = Cx - Ax
    dy = Cy - Ay
    r2 = dx*dx + dy*dy
    r  = math.sqrt(r2)

    # Calcul de l'angle beta (coude) via loi des cosinus
    cos_beta = clamp((La**2 + Lb**2 - r2)/(2*La*Lb))
    sin_beta = math.sqrt(max(0,1-cos_beta**2))
    beta = math.degrees(math.atan2(sin_beta, cos_beta))

    # Calcul de l'angle theta1
    sin_theta1 = (Lb*sin_beta)/r
    cos_theta1 = (r2 + La**2 - Lb**2)/(2*r*La)
    theta1 = math.atan2(sin_theta1, cos_theta1)

    # Calcul de l'angle theta2
    AY  = abs(Ay)
    YC2 = (Cx-Ax)**2 + (Cy)**2
    cos_theta2 = clamp((AY*AY + r2 - YC2) / (2*AY*r))
    theta2 = math.acos(cos_theta2)

    # Calcul de l'angle alpha (épaule)
    theta = theta2 - theta1
    alpha = math.degrees(theta)

    return alpha + 50, beta  # Ajustements mécaniques
