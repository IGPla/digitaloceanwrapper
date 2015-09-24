# digitaloceanwrapper
Most used API calls on Digital Ocean, implemented in a single python script, to be able to use it as a base manager on your cloud infrastructure

## Install
 - git clone https://github.com/IGPla/digitaloceanwrapper.git
 
## Usage
```sh
usage: digitaloceanwrapper.py [-h] -t TOKEN -c
                              {get_image_list,get_region_list,get_size_list,get_instance_list,get_instance_info,create_instance,create_ssh_key,reboot_instance,shutdown_instance,poweron_instance,resize_instance,rename_instance}
                              [--dropletid DROPLETID] [--name NAME]
                              [--region REGION] [--size SIZE] [--image IMAGE]
                              [--sshkey SSHKEY]

This script is a wrapper around main functions from Digital Ocean cloud
provider API. Required parameters for every command < get_image_list(token),
get_region_list(token), get_size_list(token), get_instance_list(token),
get_instance_info(token, dropletid), create_instance(token, name, region,
size, image, sshkey), create_ssh_key(token, sshkey), reboot_instance(token,
dropletid), shutdown_instance(token, dropletid), poweron_instance(token,
dropletid), resize_instance(token, dropletid), rename_instance(token,
dropletid) >

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Account token
  -c {get_image_list,get_region_list,get_size_list,get_instance_list,get_instance_info,create_instance,create_ssh_key,reboot_instance,shutdown_instance,poweron_instance,resize_instance,rename_instance}, --command {get_image_list,get_region_list,get_size_list,get_instance_list,get_instance_info,create_instance,create_ssh_key,reboot_instance,shutdown_instance,poweron_instance,resize_instance,rename_instance}
                        Command to be performed
  --dropletid DROPLETID
                        Droplet identifier
  --name NAME           Droplet name (must be a slug)
  --region REGION       Region where you want to perform your action
  --size SIZE           Size identifier
  --image IMAGE         Image identifier
  --sshkey SSHKEY       SSH key to be passed as initial user credential

```
