"""
Network, VMware, and general settings for deploying a new Linux VM
"""

from netaddr import IPNetwork, IPAddress

"""
General settings
"""
deploy_settings = dict()
deploy_settings["dns_servers"]      = ['8.8.8.8','8.8.4.4']
deploy_settings["vserver"]          = "172.17.117.104"
deploy_settings["port"]             = 443
deploy_settings["username"]         = "administrateur"
deploy_settings["password"]         = "Pr0l0gue2014"
deploy_settings["mailfrom"]         = 'root@example.com'

"""
Networks
"""
# define settings for each of our networks
net = dict()

internal_omaha = IPNetwork("172.17.0.0/16")
net[internal_omaha] = dict()
net[internal_omaha]["datacenter_name"] = 'vDC prologue'
net[internal_omaha]["cluster_name"]    = 'cluster103'
net[internal_omaha]["datastore_name"]  = 'Disque2Tera'
net[internal_omaha]["network_name"]    = 'VM Network'
net[internal_omaha]["gateway"]         = '172.17.0.254'
net[internal_omaha]["subnet_mask"]     = str(internal_omaha.netmask)

routable_omaha = IPNetwork("123.56.78.90/25")
net[routable_omaha] = dict()
net[routable_omaha]["datacenter_name"] = 'vDC prologue'
net[routable_omaha]["cluster_name"]    = 'cluster103'
net[routable_omaha]["datastore_name"]  = 'Disque2Tera'
net[routable_omaha]["network_name"]    = 'VM Network'
net[routable_omaha]["gateway"]         = '172.17.0.254'
net[routable_omaha]["subnet_mask"]     = str(routable_omaha.netmask)

'''
Storage networks
'''
internal_storage = IPNetwork("172.12.120.1/24")
net[internal_storage] = dict()
net[internal_storage]["network_name"] = 'VM Network'#'172.12.120.x storage net'
net[internal_storage]["subnet_mask"]  = str(internal_storage.netmask)