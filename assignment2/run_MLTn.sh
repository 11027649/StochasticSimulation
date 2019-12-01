#!/bin/bash


for server_amount in 1 2 4
do
    for rho in $(seq 0.70 0.05 0.90)
    do
        for run in {0..199}
        do
            echo "Simulating long tail joblength distribution with server_amount: $server_amount, workload: $rho for the $run time"
            python mltn_queue.py $server_amount $rho $run
            echo "Done"
        done
    done
done

