# -*- coding: utf-8 -*-
"""
This script is a wrapper around main functions from Digital Ocean cloud provider API
"""
import urllib
import urllib2
import json
import argparse
import sys

def get_resource_list(url, path, token):
    """
    Basic call to get authenticated resource list
    """
    retset = []

    next_url = u"%s%s" % (url, path)
    while next_url:
        req = urllib2.Request(next_url)
        req.add_header(u"Authorization", u"Bearer %s" % token)
        res = urllib2.urlopen(req)
        result = json.loads(res.read())

        next_url = None
        if result.get("links") and result.get("links").get("pages") and result.get("links").get("pages").get("next"):
            next_url = result.get("links").get("pages").get("next")
        retset.append(result)
    return retset

def get_image_list(*args, **kwargs):
    """
    Return all snapshots
    """
    path = u"/v2/images"
    retset = get_resource_list(kwargs.get("url"), path, kwargs.get("token"))
    return filter(lambda a: a.get("public") == False, reduce(lambda a, b: a+b, [a.get("images") for a in retset]))

def get_region_list(*args, **kwargs):
    """
    Return all regions
    """
    path = u"/v2/regions"
    retset = get_resource_list(kwargs.get("url"), path, kwargs.get("token"))
    return filter(lambda a: a.get("available") == True, reduce(lambda a, b: a+b, [a.get("regions") for a in retset]))

def get_size_list(*args, **kwargs):
    path = u"/v2/sizes"
    retset = get_resource_list(kwargs.get("url"), path, kwargs.get("token"))
    return reduce(lambda a, b: a+b, [a.get("sizes") for a in retset])


def get_instance_list(*args, **kwargs):
    """
    Return all droplets
    """
    path = u"/v2/droplets"
    retset = get_resource_list(kwargs.get("url"), path, kwargs.get("token"))
    return filter(lambda a: True, reduce(lambda a, b: a+b, [a.get("droplets") for a in retset]))

def post_request(url, path, token, data):
    req = urllib2.Request(u"%s%s" % (url, path), json.dumps(data))
    req.add_header(u"Authorization", u"Bearer %s" % token)
    req.add_header(u"Content-Type", u"application/json")
    req.get_method = lambda: "POST"
    resp = urllib2.urlopen(req)
    result = json.loads(resp.read())
    return result

def get_instance_info(*args, **kwargs):
    """
    Get droplet information
    """
    path = u"/v2/droplets/%i/" % kwargs.get("dropletid")
    url = u"%s%s" % (kwargs.get("url"), path)
    
    req = urllib2.Request(url)
    req.add_header(u"Authorization", u"Bearer %s" % kwargs.get("token"))
    res = urllib2.urlopen(req)
    result = json.loads(res.read())

    return result.get("droplet")


def create_instance(*args, **kwargs):
    """
    Create a new droplet
    * Note: name must be a slug
    """
    path = u"/v2/droplets"
    data = {'name': kwargs.get("name"),
            'region': kwargs.get("region"),
            'size': kwargs.get("size"),
            'image': kwargs.get("image")
        }
    if kwargs.get("key"):
        data["ssh_keys"] = [kwargs.get("sshkey")]
    result = post_request(url = kwargs.get("url"), path = path, token = kwargs.get("token"), data = data)
    return result.get("droplet")

def create_ssh_key(*args, **kwargs):
    """
    Create ssh key
    """
    path = "/v2/account/keys"
    data = {'name': kwargs.get("name"),
            'public_key': kwargs.get("sshkey")}
    return post_request(url = kwargs.get("url"), path = path, token = kwargs.get("token"), data = data)
    
def reboot_instance(*args, **kwargs):
    """
    Reboot a given droplet
    """
    path = "/v2/droplets/%i/actions"
    data = {'type': 'reboot'}
    return post_request(url = kwargs.get("url"), path = path % kwargs.get("dropletid"), token = kwargs.get("token"), data = data)

def shutdown_instance(*args, **kwargs):
    """
    Shutdown a given droplet
    """
    path = "/v2/droplets/%i/actions"
    data = {'type': 'shutdown'}
    return post_request(url = kwargs.get("url"), path = path % kwargs.get("dropletid"), token = kwargs.get("token"), data = data)

def poweron_instance(*args, **kwargs):
    """
    Power on a given droplet
    """
    path = "/v2/droplets/%i/actions"
    data = {'type': 'power_on'}
    return post_request(url = kwargs.get("url"), path = path % kwargs.get("dropletid"), token = kwargs.get("token"), data = data)


def resize_instance(*args, **kwargs):
    """
    Resize a given droplet
    """
    path = "/v2/droplets/%i/actions"
    data = {'type': 'resize',
            'size': kwargs.get("size")}
    return post_request(url = kwargs.get("url"), path = path % kwargs.get("dropletid"), token = kwargs.get("token"), data = data)


def rename_instance(*args, **kwargs):
    """
    Rename a given droplet
    """
    path = "/v2/droplets/%i/actions"
    data = {'type': 'rename',
            'name': kwargs.get("name")}
    return post_request(url = kwargs.get("url"), path = path % kwargs.get("dropletid"), token = kwargs.get("token"), data = data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""This script is a wrapper around main functions from Digital Ocean cloud provider API. Required parameters for every command <
get_image_list(token), 
get_region_list(token), 
get_size_list(token), 
get_instance_list(token), 
get_instance_info(token, dropletid), 
create_instance(token, name, region, size, image, sshkey), 
create_ssh_key(token, sshkey), 
reboot_instance(token, dropletid), 
shutdown_instance(token, dropletid), 
poweron_instance(token, dropletid), 
resize_instance(token, dropletid), 
rename_instance(token, dropletid) 
>""")
    parser.add_argument('-t', '--token', help="Account token", required = True)
    parser.add_argument('-c', '--command', help="Command to be performed", choices=["get_image_list", "get_region_list", "get_size_list", "get_instance_list", "get_instance_info", "create_instance", "create_ssh_key", "reboot_instance", "shutdown_instance", "poweron_instance", "resize_instance", "rename_instance"], required = True)
    parser.add_argument('--dropletid', help="Droplet identifier")
    parser.add_argument('--name', help="Droplet name (must be a slug)")
    parser.add_argument('--region', help="Region where you want to perform your action")
    parser.add_argument('--size', help="Size identifier")
    parser.add_argument('--image', help="Image identifier")
    parser.add_argument('--sshkey', help="SSH key to be passed as initial user credential")
    
    userargs = parser.parse_args()
    
    params = userargs.__dict__
    params['url'] = u"https://api.digitalocean.com"
    function = getattr(sys.modules[__name__], userargs.command)
    print function(**params)
