import math

def cinematique_inverse(Ax, Ay, Cx, Cy, La, Lb):

    # 1) Exprimer la position de C par rapport à A
    x = Cx - Ax
    y = Cy - Ay

    # 2) Calculer la distance AC au carré
    r2 = x*x + y*y

    # 3) Angle de l'articulation du coude beta
    cos_beta = (r2 - La*La - Lb*Lb) / (2.0 * La * Lb)
    cos_beta = max(-1.0, min(1.0, cos_beta))
    beta = math.acos(cos_beta)   

    # 4) Angle de l'articulation de l'épaule alpha
    k1 = La + Lb * math.cos(beta)
    k2 = Lb * math.sin(beta)
    alpha = math.atan2(y, x) - math.atan2(k2, k1)

    # 5) Convertion en degrees
    alpha_deg = math.degrees(alpha)
    beta_deg  = math.degrees(beta)

    return alpha_deg, beta_deg