#!/usr/bin/env python




from samples.vsclient.vsclient import *

host= "172.17.117.104"
user= "administrateur"
pwd="Pr0l0gue2014"
port=443

######################################################
######### Unit tests #################################
#################################### #################

# server_infos = get_vcenterserver_infos(host,user,pwd,port)
# print server_infos
#
#
# ##### COMPUTE
#
# vDCs = list_vDC(host,user,pwd,port)
# print vDCs
#
# vDCmor="datacenter-527"
# clusters = list_Clusters_in_vDC(host,user,pwd,port, vDCmor)
# print clusters
#
#
# clustermor="domain-c532"
# ressourcepools = list_RessourcesPool_and_VM_in_cluster(host, user, pwd, port, clustermor)
# print ressourcepools
#
#
#
# clustermor="domain-c532"
# hosts = list_hosts_in_cluster(host, user, pwd, port, clustermor)
# print hosts
#
#

# vDCmor="datacenter-527"
# modeles = list_modele_in_vDC(host, user, pwd, port,vDCmor)
# print modeles
#
#
#
# ####### resourcepool
#
# resourcepool_mor ="resgroup-2851"
# resourcepool_infos = get_resourcepool_infos(host, user, pwd, port, resourcepool_mor)
# print resourcepool_infos
#
#
#
# ###### DATASTORE
#
# vDCmor="datacenter-527"
# datastorecluster = list_datastorecluster_in_vDC(host, user, pwd, port, vDCmor)
# print datastorecluster
#
#
#
# datastoreclustermor="group-p5809"
# datastores = list_datastore_in_datastorecluster(host, user, pwd, port, datastoreclustermor)
# print datastores
#
#
# datastore_mor = "datastore-2925"#"datastore-543"
# datastore_infos = get_datastore_infos(host, user, pwd, port, datastore_mor)
# print datastore_infos
#
#
#
# ###### VirtualMachine
#
# virtualmachine_mor = "vm-5641" #"vm-5796" #"vm-5736"#"vm-5520"#"vm-5781" #
# virtualmachine_infos = get_virtualmachine_infos(host, user, pwd, port, virtualmachine_mor)
# print virtualmachine_infos
#
#
# ######## NETWORK
#
# vDCmor="datacenter-527"
# standard_switchs = list_standard_vswitch_in_vDC(host, user, pwd, port, vDCmor)
# print standard_switchs
# {"VM Network": "network-540", "none": "network-2939"}
#
#
# vDCmor="datacenter-527"
# distributed_switchs = list_distributed_vswitch_in_vDC(host, user, pwd, port, vDCmor)
# print distributed_switchs
#
#
#
# dVSmor="dvs-3083"
# distributed_virtual_portgroups = list_distributed_virtual_portgroups_in_vDC(host, user, pwd, port, dVSmor)
# print distributed_virtual_portgroups
#
#
# ######### Folders
#
# vDCmor="datacenter-527"
# folders = list_folders_and_vm_in_vdc(host, user, pwd, port, vDCmor)
# print folders




######### Clonage virtualMachine or Modele

# resourcepool_mor = "resgroup-2852"
# datastore_mor = "datastore-543"
# vm_name="testclonetemplate1"
# template_or_vm_mor="vm-5781"
#
# result = clone_object(host, user, pwd, port,vm_name, template_or_vm_mor, datastore_mor, resourcepool_mor )
# print result
#


# vm_mor = "vm-5843"
# cpu = 3
# ramMB = 2048
#
# result = update_cpu_ram(host, user, pwd, port,vm_mor,cpu,ramMB)
# print result


new_capacity_virtualdisk_in_gb = 40  # unit = GB
vm_mor = "vm-5843"
disk_number=0
vm_new_vm = update_capacity_virtualdisk(host, user, pwd, port, vm_mor, new_capacity_virtualdisk_in_gb, disk_number)
print vm_new_vm