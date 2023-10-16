def P_cooling(N_tot_v):
    """
    Input total mol/s vapor flow in condenser.
    funcion:
    massflow, density and cp of H2O * dT(N) function
    """
    return 0.05 * 0.997 * 4186 * (157.65632810395147 * N_tot_v + 0.3091753045742593) 