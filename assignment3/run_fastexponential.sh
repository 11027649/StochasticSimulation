#!/bin/bash

for run in {0..100}
do
    for particle_amount in {2..50}
    do
        time python sa_particles.py $particle_amount "exponential_fast"
        echo "Simulated annealing fast exponential $run on $particle_amount particles done"
    done
done

