#!/usr/bin/env python




from samples.vsclient.vsclient import *
import time,json

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

# vDCmor="datacenter-527"
# vdc_info = get_vdc_info(host,user,pwd,port, vDCmor)
# print vdc_info

# clustermor="domain-c532"
# cluster_info = get_cluster_info(host,user,pwd,port, clustermor)
# print cluster_info



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
#{"UBUNTU1204-AMD-64BIT-VMware-tools-cloudinit": "vm-5146", "UBUNTU1204-AMD-64BIT-VMware-tools-cloudinit.old": "vm-5133", "Ubuntu12.04-VMware-Tool-64bits": "vm-1341",
#  "Ubuntu14.04 LTS-VMwaretools-64bits": "vm-1485", "Ubuntu16.04 64bits": "vm-5621", "Windows 2008 Server R2": "vm-1348", "Windows 2012 R2 x86_64": "vm-1573", "ubunt14.04-LTS-x64": "vm-3719",
# "ubuntu-server-12.4-64lts": "vm-3699", "ubuntu12.04 64 bits 2nic dhcp": "vm-5737", "ubuntu12.04-VMware-tools-64bits-eth0static": "vm-1674"}


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
# virtualmachine_infos = get_virtualmachine_info(host, user, pwd, port, virtualmachine_mor)
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

# dVSmor="dvs-3083"
# dv_port_name="vlan20"
# vlan_id = 20
# result = create_distributed_virtual_portgroup_in_distributed_vswitch(host, user, pwd, port,dVSmor,dv_port_name,vlan_id)
# print result




# dVSmor="dvs-3083"
# dv_port_name="vlan20"
# result = delete_distributed_virtual_portgroup_in_distributed_vswitch(host, user, pwd, port,dVSmor,dv_port_name)
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
# vm_name="testclonetemplate0"
# template_or_vm_mor="vm-5621" # win2012 R2 vm-1573

#result = clone_object2(host, user, pwd, port,vm_name, template_or_vm_mor, datastore_mor, resourcepool_mor )
# print result

# result = clone_object2(host, user, pwd, port,vm_name, template_or_vm_mor, datastore_mor, resourcepool_mor )
# print result


# vm_mor = "vm-5843"
# cpu = 3
# ramMB = 2048
#
# result = update_cpu_ram(host, user, pwd, port,vm_mor,cpu,ramMB)
# print result


# new_capacity_virtualdisk_in_gb = 40  # unit = GB
# vm_mor = "vm-5843"
# disk_number=0
# vm_new_vm = update_capacity_virtualdisk(host, user, pwd, port, vm_mor, new_capacity_virtualdisk_in_gb, disk_number)
# print vm_new_vm
# vm_mor = "vm-5930"
#  list disk in vm
# disks = get_vm_disks(host, user, pwd, port, vm_mor)
# print disks

# create disk in vm_mor
# vm_mor = "vm-5930"
# disk_size_in_gb = 1
# result = add_disk_in_vm(host, user, pwd, port, vm_mor, disk_size_in_gb)
# print result

# delete disque in vm_mor
# vm_mor = "vm-5930"
# unit_number=2
# result = delete_disk_in_vm(host, user, pwd, port, vm_mor, unit_number)
# print result

"""

vm_mor = "vm-5930" #win 2012 "vm-5850"  # ubuntu 12.04 "vm-5781"   win 2016  vm-5796
result = delete_all_nic_in_vm(host, user, pwd, port, vm_mor)
print result



# vm_mor = "vm-5857"
# result = delete_nic_in_vm(host, user, pwd, port, vm_mor, unitNumber)
# print result


# vm_mor = "vm-5857"
portgroup_or_vs_mor1 = "dvportgroup-5733"           #vlan1 dhcp
portgroup_or_vs_mor2 = "dvportgroup-5746"           #"network-540" #
portgroup_or_vs_mor3= "network-540"


result = add_nic_to_vm_and_connect_to_net(host, user, pwd, port, vm_mor, portgroup_or_vs_mor1)
print result
# result = add_nic_to_vm_and_connect_to_net(host, user, pwd, port, vm_mor, portgroup_or_vs_mor2)
# print result
# result = add_nic_to_vm_and_connect_to_net(host, user, pwd, port, vm_mor, portgroup_or_vs_mor3)
# print result

# vm_mor = "vm-5850"

#nic config in order
nic_config=[
            {'isDHCP': False,
             'vm_ip': '10.10.10.3',
             'subnet': '255.255.255.0',
             'gateway': '10.10.10.1',
             'dns': ['8.8.8.8', '8.8.4.4'],
             }
            ]
hostname = "vm1"
domaine = "prologue.prl"
adminpassword= "" # Only for windows


result = customize_nics_in_vm(host, user, pwd, port, vm_mor, nic_config, hostname, domaine, adminpassword)
print result



##Actions on VM
result = poweron_vm(host, user, pwd, port, vm_mor)
print result




timeout_in_mn=15   # 15 for windows os
result = wait_for_tools(host, user, pwd, port, vm_mor, timeout_in_mn)
print result



virtualmachine_infos = get_virtualmachine_info(host, user, pwd, port, vm_mor)
print virtualmachine_infos
"""

vm_mor = "vm-5641"
link = generate_html5_console(host, user, pwd, port, vm_mor)
print link


### Snapshot
# vm_mor="vm-5906"
# result = get_snapshots_in_vm(host, user, pwd, port, vm_mor)
# print result

# create snapshot

# vm_mor="vm-5906"
# snapshot_name="1000"
# result = create_snapshot_in_vm(host, user ,pwd , port ,vm_mor ,snapshot_name)
# print result
#
#
# vm_mor="vm-5906"
# snapshot_name="1000"
# result = create_snapshot_in_vm(host, user ,pwd , port ,vm_mor ,snapshot_name)


#
# vm_mor="vm-5906"
# snapshot_name="1645"
# result = revert_to_snapshot_in_vm(host, user ,pwd , port ,vm_mor ,snapshot_name)


# vm_mor="vm-5906"
# snapshot_name="1641"
# result = delete_snapshot_in_vm(host, user ,pwd , port ,vm_mor ,snapshot_name)


