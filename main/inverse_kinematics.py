import math

def cinematique_inverse(Ax, Ay, Cx, Cy, La, Lb):

    # 1) Exprimer la position de C par rapport à A
    x = Cx - Ax
    y = Cy - Ay

    # 2) Calculer la distance AC au carré
    r = math.sqrt(x*x + y*y)

    # 3) Angle de l'articulation du coude beta
    cos_beta = (r - La*La - Lb*Lb) / (2.0 * La * Lb)
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

def clamp(x):
    return max(-1, min(1, x))

def cinematique_inverse_2(Ax, Ay, Cx, Cy, La, Lb):
    AC = math.sqrt((Cx-Ax)**2 + (Cy-Ay)**2)
    cos_theta = (La**2 + Lb**2 - AC**2)/(2*La*Lb)
    theta = math.acos(clamp(cos_theta))
    beta = math.degrees(theta)
    
    YC = math.sqrt((Ax-Cx)**2 + Cy**2)
    cos_theta2 = (abs(Ay)**2 + AC**2 - YC**2)/ (2*abs(Ay)*AC)
    theta2 = math.acos(clamp(cos_theta2))
    
    cos_theta3 = (La**2 + AC**2 - Lb**2)/(2*La*AC)
    theta3 = math.acos(clamp(cos_theta3))
    
    alpha = theta2 - theta3
    alpha = math.degrees(alpha)
    
    return alpha + 47, beta - 35