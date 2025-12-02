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


def cinematique_inverse2(Ax, Ay, Cx, Cy, La, Lb):
    # Vector from base A to target C
    dx = Cx - Ax
    dy = Cy - Ay
    r2 = dx**2 + dy**2
    r  = math.sqrt(r2)

    # Reachability check (don’t “lie” with clamp when outside workspace)
    if r > La + Lb or r < abs(La - Lb) or r == 0:
        print(r, La, Lb)
        raise ValueError("Target unreachable (or r==0).")

    # Elbow angle q2 (relative joint angle)
    cos_q2 = clamp((La*La + Lb*Lb - r2) / (2*La*Lb))
    sin_q2_mag = math.sqrt(max(0.0, 1.0 - cos_q2*cos_q2))
    sin_q2 = sin_q2_mag
    q2 = math.atan2(sin_q2, cos_q2)

    # Shoulder angle q1
    q1 = math.atan2(dy, dx) - math.atan2(Lb*sin_q2, La + Lb*cos_q2)

    # Convert to degrees
    alpha = math.degrees(q1)
    beta  = math.degrees(q2)

    # Your mechanical offsets
    S = alpha + 47
    E = beta  - 35
    return S, E

