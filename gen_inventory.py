#!/usr/bin/env python

import argparse
from distutils.spawn import find_executable
from jinja2 import Environment
import os
import yaml


def inventory(args):
    if find_executable('oc') is None:
        print("oc not found in path. Leaving!")
        os._exit(1)
    if 'KUBECONFIG' not in os.environ:
        print("KUBECONFIG environment variable unset. Leaving!")
        os._exit(1)
    physical = args.physical
    INVENTORY = """all:
  vars:
   performance_channel: 4.4
   mcps:
   - worker-cnf
   performance_crs:
   -    |
       apiVersion: performance.openshift.io/v1alpha1
       kind: PerformanceProfile
       metadata:
         name: worker-cnf
       spec:
         cpu:
           isolated: {{ "0-8" if physical else "1-3" }}
           reserved: {{ "9-15" if physical else "0" }}
         hugepages:
           defaultHugepagesSize: "1G"
           pages:
           - size: "1G"
             count: {{ 16 if physical else 1 }}
             node: 0
         realTimeKernel:
           enabled: true
         nodeSelector:
           node-role.kubernetes.io/worker-cnf: ""
  children:
      nodes:
        hosts:
{%- for node in nodes %}
          {{ node }}:
            labels:
              - node-role.kubernetes.io/worker-cnf
{%- endfor -%}"""

    nodes = []
    allnodes = os.popen("oc get node -o yaml").read()
    for node in yaml.load(allnodes)['items']:
        name = node['metadata']['name']
        labels = node['metadata']['labels']
        if 'node-role.kubernetes.io/worker' in labels:
            nodes.append(name)
    print(Environment().from_string(INVENTORY).render(nodes=nodes, physical=physical))


parser = argparse.ArgumentParser(description='Generate yaml inventory from your worker nodes to use with the playbook')
parser.add_argument('-p', '--physical', action='store_true', help='Treat workers as physical')
parser.set_defaults(func=inventory)
args = parser.parse_args()
args.func(args)