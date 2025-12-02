import math

def clamp(x):
    return max(-1, min(1, x))

def cinematique_inverse(Ax, Ay, Cx, Cy, La, Lb):
    dx = Cx - Ax
    dy = Cy - Ay
    r2 = dx*dx + dy*dy
    r  = math.sqrt(r2)

    cos_beta = clamp((La**2 + Lb**2 - r2)/(2*La*Lb))
    sin_beta = math.sqrt(max(0,1-cos_beta**2))
    beta = math.degrees(math.atan2(sin_beta, cos_beta))

    sin_theta1 = (Lb*sin_beta)/r
    cos_theta1 = (r2 + La**2 - Lb**2)/(2*r*La)
    theta1 = math.atan2(sin_theta1, cos_theta1)

    AY  = abs(Ay)
    YC2 = (Cx-Ax)**2 + (Cy)**2
    cos_theta2 = clamp((AY*AY + r2 - YC2) / (2*AY*r))
    theta2 = math.acos(cos_theta2)

    theta = theta2 - theta1
    alpha = math.degrees(theta)

    return alpha + 47, beta -35  # ajustements mécaniques
