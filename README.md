[![Build Status](https://travis-ci.org/karmab/ansible-cnf-install.svg?branch=master)](https://travis-ci.org/karmab/ansible-cnf-install)

## About

This repository provides ansible roles which can be used to deploy the following elements:
- cluster-setup (labels nodes and create machineconfigpools)
- performance add on operator
- sriov operator
- ptp operator
- sctp module
- dpdk s2i uild

For the operators, a set of crs can also be specified or let empty so that the user handles crs by himself

## Requirements

- a running openshift cluster
- ansible
- oc binary
- KUBECONFIG env variable properly set!

## Launch

Prepare a valid hosts or hosts.yml file in inventory directory with the information needed.

For instance, consider the following (yaml) inventory:

```
all:
  vars:
   performance_channel: 4.4
   mcps:
   - worker-cnf
   - master-cnf
   performance_crs:
   -    |
       apiVersion: performance.openshift.io/v1alpha1
       kind: PerformanceProfile
       metadata:
         name: worker-cnf
       spec:
         cpu:
           isolated: "1-3"
           reserved: "0"
         hugepages:
           defaultHugepagesSize: "1G"
           pages:
           - size: "1G"
             count: 1
         realTimeKernel:
           enabled: true
         nodeSelector:
           node-role.kubernetes.io/worker-cnf: ""
  children:
      nodes:
        hosts:
          node01:
            labels:
            - node-role.kubernetes.io/worker-cnf
          node02:
            labels:
            - node-role.kubernetes.io/worker-cnf
```

It will:

- create mcps worker-cnf and master-cnf
- labels all nodes in the *cluster_group* group (nodes by default) with their corresponding list of labels (node-role.kubernetes.io/worker-cnf in this case for both of them)
- when deploying performance operator, also create the `worker-cnf` performance profile

You could use this inventory along with the following playbook

```
---
- name: Deploy Cnf Operators
  hosts: localhost
  become: yes
  environment:
    PATH: "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
  roles:
  - cluster-setup
  - performance
  - ptp
  - sriov
  - dpdk
#  - sctp
#  - cnv
```

With inventory and playbook in place, you can launch the deployment the usual way:

```
ansible-playbook -i inventory playbook.yml
```

## Ansible variables

|Parameter                 |Default Value |
|--------------------------|--------------|
|cluster_group             |nodes         |
|mcps                      |[]            |
|performance_channel       |4.4           |
|performance_catalogsource |              |
|performance_crs           |              |
|performance_crs           |[]            |
|sriov_channel             |4.4           |
|sriov_catalogsource       |              |
|sriov_crs                 |[]            |
|ptp_channel               |4.4           |
|ptp_catalogsource         |              |
|ptp_crs                   |[]            |

## Generating ansible inventory

You can use the helper script *gen_inventory.py* for this purpose

```
python3 gen_inventory.py
```

