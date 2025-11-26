import math

def clamp(x):
    return max(-1, min(1, x))

def cinematique_inverse(Ax, Ay, Cx, Cy, La, Lb):
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