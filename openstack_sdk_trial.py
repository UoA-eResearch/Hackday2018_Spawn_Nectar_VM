#!/usr/local/bin/python
from keystoneauth1.identity import v3
from keystoneauth1 import session
import openstack.cloud
import json

def example_create_own_security_group
  #Check if security group exists
  services_group = conn.get_security_group(service_security_group)
  if services_group == None:
    services_group = conn.create_security_group(service_security_group, 'for DB and AMPQ services only')
    conn.create_security_group_rule(services_group.id, port_range_min=22,  port_range_max=22, protocol='tcp', direction='ingress', ethertype='IPv4')
    conn.create_security_group_rule(services_group.id, port_range_min=3306,  port_range_max=3306, protocol='tcp', direction='ingress', ethertype='IPv4')
    conn.create_security_group_rule(services_group.id, port_range_min=5672,  port_range_max=5672, protocol='tcp', direction='ingress', ethertype='IPv4')
  return security_group
  
with open('conf.json') as f:
    conf = json.load(f)

# Initialize and turn on debug logging
#openstack.enable_logging(debug=True)
print "*********Open Connection**************"

auth = v3.Password(auth_url=conf['auth_url'],
                   username=conf['username'],
                   password=conf['password'],
                   project_name=conf['project_name'],
                   project_domain_name=conf['project_domain_name'],
                   user_domain_name=conf['user_domain_name']
                   )
sess = session.Session(auth=auth)

# Initialize connection
# Cloud configs are read with openstack.config
conn = openstack.connect(session=sess)

# Upload an image to the cloud
#image = conn.create_image( 'ubuntu-trusty', filename='ubuntu-trusty.qcow2', wait=True)
#image = conn.get_image('NeCTAR Ubuntu 16.04 LTS (Xenial) amd64') #Gets multiple images
image = conf['image']

# Find a flavor with at least 512M of RAM
#flavor = conn.get_flavor_by_ram(512)
flavor = conf['flavor']

print "********Create Server Instance***************"

USE_USERDATA_STR=True
userdata_as_str = '''#!/bin/bash
/bin/echo "Hello World" > /tmp/hello.txt
'''
user_data_as_file = file('/Users/rbur004/startup.sh', 'r')
startup_script =  userdata_as_str if USE_USERDATA_STR else user_data_as_file

# Boot a server, wait for it to boot, and then do whatever is needed
# to get a public ip for it.
# Use existing security groups and SSH keys
server = conn.create_server( 'rbur-test10', image=image, flavor=flavor, key_name=conf['keypair'], wait=True, auto_ip=True, security_groups=['http and https','ssh'], userdata=startup_script, timeout=300)

print "*******Server Instance created****************"
print server.name "at", server.public_v4

print "********Server Details***************"
conn.pprint(server)

print "********Security Groups***************"
for s in conn.list_server_security_groups(server):
  print s.name
  
print "**********Deleting server instance*************"
conn.delete_server(server, wait=True, delete_ips=True)

