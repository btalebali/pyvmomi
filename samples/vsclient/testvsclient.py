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



# clustermor="domain-c532"
# ressourcepools = list_RessourcesPool_and_VM_in_cluster(host, user, pwd, port, clustermor)
# print ressourcepools




# clustermor="domain-c532"
# hosts = list_hosts_in_cluster(host, user, pwd, port, clustermor)
# print hosts




###### DATASTORE

# vDCmor="datacenter-527"
# datastorecluster = list_datastorecluster_in_vDC(host, user, pwd, port, vDCmor)
# print datastorecluster



# datastoreclustermor="group-p5809"
# datastores = list_datastore_in_datastorecluster(host, user, pwd, port, datastoreclustermor)
# print datastores



