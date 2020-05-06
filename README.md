[![Build Status](https://travis-ci.org/karmab/ansible-cnf-install.svg?branch=master)](https://travis-ci.org/karmab/ansible-cnf-install)

## About

This repository provides an ansible role which can be used to deploy the following elements:
- performance add on operator
- sriov operator
- ptp operator
- sctp module
- dpdk s2i uild

## Requirements

- a running openshift cluster
- ansible
- oc binary

## Launch

Prepare a valid parameter file with the information needed. At least, you need to specify the following elements:

```
ansible-playbook -i $YOUR_HOST, playbook.yml
```

## Parameters

### Performance

|Parameter                |Default Value                 |
|-------------------------|------------------------------|
|namespace                |openshift-performance-addon   |
|channel                  |4.4                           |
|mcp                      |worker-cnf                    |
