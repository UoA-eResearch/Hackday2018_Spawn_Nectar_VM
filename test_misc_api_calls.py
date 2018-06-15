#!/usr/local/bin/python
from keystoneauth1.identity import v3
from keystoneauth1 import session
#from keystoneclient.v3 import client
from glanceclient import Client
import novaclient.v2.client
from neutronclient.v2_0 import client
import json

#Docs https://docs.openstack.org/python-openstackclient/pike/index.html

def list_keypairs():
  print "***********Keypairs****************"
  for k in novac.keypairs.list():
    print 'name =',k.name, ' id =',k.id
  
def list_flavors():
  print "************Flavors***************"
  for n in novac.flavors.list():
    print n.id, n.name

def list_servers():
  print "************Servers***************"
  for n in novac.servers.list(detailed=True):
    #print  n.__dict__['OS-EXT-STS:power_state']
    d = n.__dict__
    print n.id, n.name,n.hostId, d['OS-EXT-AZ:availability_zone'] #n.networks  #n.image #n.flavor #n.key_name, tenant_id, flavor, #n.user_id

def list_a_server(ip):
  print "************Servers with IP 130.216.216.98***************"
  for n in novac.servers.list(detailed=True, search_opts={'ip': ip}):
    d = n.__dict__
    print n.id, n.name,n.hostId, d['OS-EXT-AZ:availability_zone'], n.image['id'] #n.networks  #n.image #n.flavor #n.key_name, tenant_id, flavor, #n.user_id    
  
def list_security_groups():
  print "*********Security Groups**************"
  sg = neut.list_security_groups()
  for s in sg['security_groups']:
    print s
    print
  #for s in neut.list_security_groups(): #Deprecated !!!
  #  print s

def list_images():
  print "*************Images**************"
  for image in glance.images.list():
    print image
     
def image_by_name(name): #Horrible, but by name call, nova1.images.find(name=''), looks to have vanished. 
  for image in glance.images.list():
    if image.name == name:
      return image

def get_image(id):
  print "***********image by ID****************"
  d = glance.images.get(id)
  print d
  

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
novac = novaclient.client.Client(2, session=sess)
neut = client.Client(session=sess)
glance = Client('2', session=sess)

list_flavors()
list_servers()
list_a_server('130.216.216.98')
list_keypairs()
list_security_groups()
list_images()
get_image('f82012f7-5042-48aa-81c2-a59684840c23')
print "**********Get a image by name ***************"
image = image_by_name('NeCTAR Ubuntu 16.04 LTS (Xenial) amd64') #id 'f82012f7-5042-48aa-81c2-a59684840c23' 
print image
print "**********Get a flavor ID by name ***************"
flavor = novac.flavors.find(name='m2.medium')
print flavor



