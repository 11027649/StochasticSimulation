#!/bin/bash

for run in {0..100}
do
    for particle_amount in 90 92
    do
        time python sa_particles.py $particle_amount "exponential_fast" 20000
        echo "Simulated annealing fast exponential $run on $particle_amount particles done"
    done
done

