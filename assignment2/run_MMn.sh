#!/bin/bash


for server_amount in 1 2 4
do
    for rho in $(seq 0.05 0.05 0.95)
    do
        for run in {0..9}
        do
            echo "Simulating server_amount: $server_amount, workload: $rho for the $run time"
            python mmn_queue.py $server_amount $rho $run
            echo "Done"
        done
    done
done
