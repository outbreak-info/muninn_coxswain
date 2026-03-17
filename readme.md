# Muninn Coxswain

**Deployment management for Muninn using Ansible.**


## Setup

### Execution environment

Ansible commands are run within a container called an execution environment.
To build the execution environment image:

```
ansible-builder build --tag test_ee
```
You may replace the image name `test_ee` with a more descriptive string.

### Secrets

Secrets are expected to be stored in a directory called `secrets/`.
The following are expected to be present:

- gcp service account file
- ssh keys for the user to be used by ansible
- a yaml file setting mirroring muninn's .env settings.

The names of these files are hardcoded for now, as this project only has one user for now. (me.)

I have provided a script to convert `.env` files to yaml files for use here. 
```
python3 env_to_yaml.py foo.env > foo.env.yml
```


## Usage

### Tips

To restrict the set of hosts on which a playbook is run, change the value of `target_hosts`.

- `target_hosts=muninn-h5n1-19-nov` will only run against this one instance
- `target-hosts=muninn-h5n1*` will target all instance with names matching the pattern

The playbook `uptime.yml` just prints the uptime of all running instances in GCP.
This is a way to test that your environment is set up correctly.

### Create a new instance in GCP

Instance names start with the prefix `muninn-`. 
Provide a `suffix` value to name the instance.

```
podman run --rm -v $PWD:/muninn test_ee:latest \
ansible-playbook /muninn/playbooks/create_instance.yml \
-i /muninn/inventory.gcp.yml \
-u james_coxswain \
--private-key /muninn/secrets/james_coxswain \
-e "suffix=hello-world"
```


### Update muninn on existing instances

This will update instances to the latest version of master and reload the nginx config.
The database will **not** be wiped, and its schema will not be updated.
```
podman run --rm -v $PWD:/muninn test_ee:latest \
ansible-playbook /muninn/playbooks/update_instances.yml \
-i /muninn/inventory.gcp.yml \
-u james_coxswain \
--private-key /muninn/secrets/james_coxswain \
-e "target_hosts=all"
```

This playbook needs access to a yaml file that gives the muninn .env values.
By default, this file is `secrets/coxswain.env.yml`.
You can override the values in this file by supplying another file as `extra_vars`.
Add the following to the end of the command:
```
-e '@/muninn/secrets/override.env.yml'
```

### Update the H5N1 frontend on existing instances

This updates js-outbreak and outbreak-info-h5n1 to latest versions.
```
podman run --rm -v $PWD:/muninn test_ee:latest \
ansible-playbook /muninn/playbooks/update_frontend.yml \
-i /muninn/inventory.gcp.yml \
-u james_coxswain \
--private-key /muninn/secrets/james_coxswain \
-e "target_hosts=all"
```

### Stop running containers and wipe database

```
podman run --rm -v $PWD:/muninn test_ee:latest \
ansible-playbook /muninn/playbooks/hard_shutdown.yml \
-i /muninn/inventory.gcp.yml \
-u james_coxswain \
--private-key /muninn/secrets/james_coxswain \
-e "target_hosts=all"
```

### What doesn't this do?

**Data ingestion:**
No part of the muninn data ingestion is handled by these playbooks. 
For now, ingestion is a very manual process. 


**Adding instances to load balancers:**
New instances need to be added to an instance group to associate them with a LB and make them accessible at a domain name. 
This is done manually through the google cloud console.