
# coding: utf-8

# In[1]:

"""
    N-body simulation.
"""
from itertools import combinations

def paris(BODIES_key):
    pairs=combinations(BODIES_key,2) 
    return list(pairs)
    
    
def advance(dt,iterations,BODIES_key,BODIES,BODIES_pairs):
    '''
        advance the system one timestep
    '''
    for _ in range(iterations):
        seenit = set()
   
        for (body1,body2) in BODIES_pairs: 
        
            if body2 not in seenit:
                ([x1, y1, z1], v1, m1) = BODIES[body1]
                ([x2, y2, z2], v2, m2) = BODIES[body2]
                (dx, dy, dz) = (x1-x2, y1-y2, z1-z2) #compute_delta
                
                core_compute_b = (dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5)))
                compute_b_m2=m2 * core_compute_b
                compute_b_m1=m1 * core_compute_b
                v1[0] -= dx * compute_b_m2
                v1[1] -= dy * compute_b_m2
                v1[2] -= dz * compute_b_m2
                v2[0] += dx * compute_b_m1
                v2[1] += dy * compute_b_m1
                v2[2] += dz * compute_b_m1
                seenit.add(body1)
        
   
        for body in BODIES_key:
            (r, [vx, vy, vz], m) = BODIES[body]
       
            r[0] += dt * vx
            r[1] += dt * vy
            r[2] += dt * vz

    
def report_energy(BODIES_key,BODIES,BODIES_pairs,e=0.0,):
    '''
        compute the energy and return it so that it can be printed
    '''
    
    seenit = set()

    for (body1,body2) in BODIES_pairs: 
       
        
        if body2 not in seenit:
            ((x1, y1, z1), v1, m1) = BODIES[body1]
            ((x2, y2, z2), v2, m2) = BODIES[body2]
            (dx, dy, dz) = (x1-x2, y1-y2, z1-z2) #compute_delta
            e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5) #compute_energy(m1, m2, dx, dy, dz)
               
            seenit.add(body1)
        
    #for body in BODIES.keys():
    for body in BODIES_key:
        (r, [vx, vy, vz], m) = BODIES[body]
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
        
    return e

def offset_momentum(ref, BODIES_key,BODIES,px=0.0, py=0.0, pz=0.0):
    '''
        ref is the body in the center of the system
        offset values from this reference
    '''
    
    for body in BODIES_key:
        (r, [vx, vy, vz], m) = BODIES[body]
        px -= vx * m
        py -= vy * m
        pz -= vz * m
        
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m


def nbody(loops, reference, iterations):
    '''
        nbody simulation
        loops - number of loops to run
        reference - body at center of system
        iterations - number of timesteps to advance
    '''
    
    offset_momentum(BODIES[reference],BODIES_key,BODIES)
    for _ in range(loops):
        report_energy(BODIES_key,BODIES,BODIES_pairs)
        advance(0.01,iterations,BODIES_key,BODIES,BODIES_pairs)
        print("report energy",report_energy(BODIES_key,BODIES,BODIES_pairs))

if __name__ == '__main__':
    PI = 3.14159265358979323
    SOLAR_MASS = 4 * PI * PI
    DAYS_PER_YEAR = 365.24

    BODIES = {
    'sun': ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], SOLAR_MASS),

    'jupiter': ([4.84143144246472090e+00,
                 -1.16032004402742839e+00,
                 -1.03622044471123109e-01],
                [1.66007664274403694e-03 * DAYS_PER_YEAR,
                 7.69901118419740425e-03 * DAYS_PER_YEAR,
                 -6.90460016972063023e-05 * DAYS_PER_YEAR],
                9.54791938424326609e-04 * SOLAR_MASS),

    'saturn': ([8.34336671824457987e+00,
                4.12479856412430479e+00,
                -4.03523417114321381e-01],
               [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR],
               2.85885980666130812e-04 * SOLAR_MASS),

    'uranus': ([1.28943695621391310e+01,
                -1.51111514016986312e+01,
                -2.23307578892655734e-01],
               [2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR],
               4.36624404335156298e-05 * SOLAR_MASS),

    'neptune': ([1.53796971148509165e+01,
                 -2.59193146099879641e+01,
                 1.79258772950371181e-01],
                [2.68067772490389322e-03 * DAYS_PER_YEAR,
                 1.62824170038242295e-03 * DAYS_PER_YEAR,
                 -9.51592254519715870e-05 * DAYS_PER_YEAR],
                5.15138902046611451e-05 * SOLAR_MASS)}

    BODIES_key=['sun','jupiter','saturn','uranus','neptune']
    BODIES_pairs=paris(BODIES_key)
    get_ipython().magic("timeit -n3 nbody(100, 'sun', 20000)")
    
    


# In[ ]:

get_ipython().magic("timeit -n3 nbody(10, 'sun', 20)")


# In[ ]:



