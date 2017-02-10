#!/usr/bin/env python




from samples.vsclient.vsclient import *

host= "172.17.117.104"
user= "administrateur"
pwd="Pr0l0gue2014"
port=443

######################################################
######### Unit tests #################################
#################################### #################


##### COMPUTE

# server_infos = get_vcenterserver_infos(host,user,pwd,port)
# print server_infos

#vDCs = list_vDC(host,user,pwd,port)
#print vDCs


# vDCmor="datacenter-527"
# clusters = list_Clusters_in_vDC(host,user,pwd,port, vDCmor)
# print clusters


#
# clustermor="domain-c532"
# ressourcepools = list_RessourcesPool_and_VM_in_cluster(host, user, pwd, port, clustermor)
# print ressourcepools




# clustermor="domain-c532"
# hosts = list_hosts_in_cluster(host, user, pwd, port, clustermor)
# print hosts





####### resourcepool

# resourcepool_mor ="resgroup-2851"
# resourcepool_infos = get_resourcepool_infos(host, user, pwd, port, resourcepool_mor)
# print resourcepool_infos





###### DATASTORE

# vDCmor="datacenter-527"
# datastorecluster = list_datastorecluster_in_vDC(host, user, pwd, port, vDCmor)
# print datastorecluster




# datastoreclustermor="group-p5809"
# datastores = list_datastore_in_datastorecluster(host, user, pwd, port, datastoreclustermor)
# print datastores


# datastore_mor = "datastore-2925"#"datastore-543"
# datastore_infos = get_datastore_infos(host, user, pwd, port, datastore_mor)
# print datastore_infos




###### VirtualMachine

# virtualmachine_mor = "vm-5641" #"vm-5796" #"vm-5736"#"vm-5520"#"vm-5781" #
# virtualmachine_infos = get_virtualmachine_infos(host, user, pwd, port, virtualmachine_mor)
# print virtualmachine_infos
