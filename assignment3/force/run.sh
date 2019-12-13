#!/bin/bash

for run in {0..10}
do
    for particle_amount in {2..10}
    do
        time python force_sa_particles.py $particle_amount
        echo "Simulated annealing $run on $particle_amount particles done"
    done
done

