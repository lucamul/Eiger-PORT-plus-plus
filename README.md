
# EIGER-PORT++ Prototype

This repository contains the prototype for the EIGER-PORT++ project. It is based on the repository from the SIGMOD 2014 paper titled [Scalable Atomic Visibility with RAMP Transactions](http://www.bailis.org/papers/ramp-sigmod2014.pdf) and includes enhancements to run experiments on EIGER-PORT, EIGER-PORT+, and EIGER-PORT++ along with the enhancements provided by the ORA repository.

## Setting up the CloudLab Cluster

1. Start an experiment with an OpenStack profile. 
2. Select a link speed of 1Gbps and the required number of nodes (clients + servers) using d710 from Emulab. Note that the results were calculated using eight servers and eight clients unless otherwise specified.
3. Once the CloudLab experiment is ready, access the OpenStack Dashboard as explained by CloudLab and create 16 nodes of size m1.large using the bionic-server image. Make sure to insert the following bash script in the configuration option:

```
#!bin/bash
sudo apt update
sudo apt install -y default-jdk
sudo apt install -y pssh
sudo apt install -y maven
```


4. Next, create one m1.medium instance, which we refer to as the Host and is the machine from which we will run our experiment. 
5. Assign a floating IP to the Host machine, copy the codebase to it, and SSH to it. The codebase should be copied so that in `/home/ubuntu` three folders appear:

- kaiju
- hosts
- results

6. Access the `all-clients.txt` file and write the IP addresses of all client machines, the same for `all-servers.txt`. Finally, in `all-hosts.txt`, write all clients and all servers.

7. Now, change to the `/home/ubuntu/experiment` folder and run `bash setup_cluster.sh`. (It will ask for a password to setup passwordless ssh among all the nodes, it's the same password that is used for the Openstack dahsboard)

## Running an Experiment

In `experiment.py`, you will find different experiments that you can run from the RAMP paper. You can expand and modify these experiments by altering the lists of parameters in the dictionary. For example, `tsize_test` is a test of varying transaction size. To run any experiment, change to the `/home/ubuntu/experiment` folder and run:

```
python setup_hosts.py --color -c us-west-2 -nc 5 -ns 5 --experiment EXP --tag example
```
Where `EXP` is the name of the experiment in `experiments.py`.

Alternatively, you can run one of the existing experiments by running `bash run_default.sh`, `bash run_number_clients.sh`, `bash run_number_servers.sh`, or `bash run_zipf_const.sh`.

The logs will be uploaded to the `output` folder.

You can process the latest results by calling `bash process_latest_results.sh` or process a specific result by calling `python3 process_results.py "folder_name" "experiment_name"` and adding `--freshness` if you want to process data freshness.

## Further Questions

For further information on the codebase, please refer to the RAMP GitHub repository.
