#!/bin/bash



for run in {0..1000}
do
    for particle_amount in {60..100}
    do
        time python sa_particles.py $particle_amount
        echo "Simulated annealing $run on $particle_amount particles done"
    done
done

