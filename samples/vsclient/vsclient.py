#!/usr/bin/env python

import atexit
import ssl
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import json

#from samples.tools import cli
#from samples.tools import vm


def get_vcenterserver_infos(host,user,pwd,port):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :return:
    """
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        vim_aboutinfos = service_instance.content.about
        result={}
        result["version"]=vim_aboutinfos.version
        result["vendor"] = vim_aboutinfos.vendor
        result["productLineId"] = vim_aboutinfos.productLineId
        result["osType"] = vim_aboutinfos.osType
        result["name"] = vim_aboutinfos.name
        result["localeVersion"] = vim_aboutinfos.localeVersion
        result["localeBuild"] = vim_aboutinfos.localeBuild
        result["licenseProductVersion"] = vim_aboutinfos.licenseProductVersion
        result["licenseProductName"] = vim_aboutinfos.licenseProductName
        result["instanceUuid"] = vim_aboutinfos.instanceUuid
        result["fullName"] = vim_aboutinfos.fullName
        result["build"] = vim_aboutinfos.build
        result["apiVersion"] = vim_aboutinfos.apiVersion
        result["apiType"] = vim_aboutinfos.apiType
        result = json.dumps(result)
        return result
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result



def list_vDC(host, user, pwd, port):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :return:
    """
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.Datacenter], True)
        result={}
        for obj in object_view.view:
            result[obj.name]=obj._moId
        object_view.Destroy()
        return result
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result





def list_Clusters_in_vDC(host, user, pwd, port, vDCmor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param vDCmor:  id of the virtual datacenter
    :return:
    """
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.Datacenter], True)
        result={}
        for obj in object_view.view:
            if obj._moId==vDCmor:
                #print obj
                clusters = obj.hostFolder.childEntity
                for obj in clusters:
                    result[obj.name] = obj._moId
        object_view.Destroy()
        return result
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result


def list_RessourcesPool_and_VM_in_cluster(host, user, pwd, port, cluster_mor, rp = None):
    try:
        init = (rp is None)

        if init:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.verify_mode = ssl.CERT_NONE
            service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
            if not service_instance:
                result = "Could not connect to the specified host using specified username and password"
                return result
            atexit.register(connect.Disconnect, service_instance)
            content = service_instance.RetrieveContent()
            object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.ClusterComputeResource], True)

            clusters = object_view.view
            object_view.Destroy()
            # todo gerer le fait de ne pas trouver le cluster
            for c in clusters:
                if c._moId == cluster_mor:
                    rp = c.resourcePool
                    break

        data = {
            "id": str(rp._moId),
            "name": str(rp.name),
            "resources_pools": [],
            "vms": get_VMS(rp.vm)
        }

        for rp_resource_pool in rp.resourcePool:
            data["resources_pools"].append(list_RessourcesPool_and_VM_in_cluster(host, user, pwd, port, cluster_mor, rp_resource_pool))

        return json.dumps(data, sort_keys=True) if init else data
    except vmodl.MethodFault as e:
        result = "Caught vmodl fault : {}".format(e.msg)
        return result

def get_VMS(vms):
    VMS = []
    for vm in vms:
        vmdict = {}
        vmdict["id"] = str(vm._moId)
        vmdict["name"] = str(vm.name)
        vmdict["status"] = str(vm.summary.runtime.powerState)
        VMS.append(vmdict)
    return VMS



def list_hosts_in_cluster(host, user, pwd, port, Clustermor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param Clustermor:  id of the Clustermor
    :return:
    """
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.ClusterComputeResource], True)
        result={}
        for obj in object_view.view:
            if obj._moId==Clustermor:
#                print obj
                hosts = obj.host
                for host in hosts:
                    result[host.name]=host._moId
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result




def list_datastorecluster_in_vDC(host, user, pwd, port, vDCmor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param vDCmor:
    :return:
    """
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.StoragePod], True)
        result={}
        for obj in object_view.view:
            if obj.parent.parent._moId == vDCmor:
                result[obj.name] = obj._moId
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result


def list_datastore_in_datastorecluster(host, user, pwd, port, datastoreclustermor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param datastoreclustermor:
    :return:
    """
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.StoragePod], True)
        result={}
        for obj in object_view.view:
            if obj._moId == datastoreclustermor:
                datastores = obj.childEntity
                for datastore in datastores:
                    result[datastore.name] = datastore._moId
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result

def get_datastore_infos(host, user, pwd, port, datastore_mor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param datastore_mor:
    :return:
    """
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.Datastore], True)
        result={}
        for obj in object_view.view:
            if obj._moId == datastore_mor:
                result["name"]=obj.name
                result["moId"] = str(obj._moId)
                result["overallStatus"] = str(obj.overallStatus)
                result["capacity"]=str(obj.summary.capacity)
                result["freeSpace"] = str(obj.summary.freeSpace)
                result["type"] = obj.summary.type
                result["vms"]=get_VMS(obj.vm)
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result



def get_resourcepool_infos(host, user, pwd, port, resourcepool_mor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param resourcepool_mor:
    :return:
    """

    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.ResourcePool], True)
        result={}
        for obj in object_view.view:
            if obj._moId == resourcepool_mor:
                result["name"]=obj.name
                result["moId"] = str(obj._moId)
                result["overallStatus"] = str(obj.overallStatus)
                cpu = {
                    "overallCpuUsage": int(obj.summary.quickStats.overallCpuUsage),
                    "overallCpuDemand": int(obj.summary.quickStats.overallCpuDemand),
                    "maxUsage": int(obj.summary.runtime.cpu.maxUsage)
                }
                ram = {
                    "hostMemoryUsage": int(obj.summary.quickStats.hostMemoryUsage),
                    "consumedOverheadMemory": int(obj.summary.quickStats.consumedOverheadMemory),
                    "maxUsage": sum_memory_vms(obj.vm)
                }
                result["cpu"] = cpu
                result["ram"] = ram
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result


def sum_memory_vms(vms):
    if len(vms) == 0:
        return None
    else:
        result=0
        for vm in vms:
            result+= int(vm.config.hardware.memoryMB)
        return result




def get_virtualmachine_infos(host, user, pwd, port, virtualmachine_mor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param virtualmachine_mor:
    :return:
    """


    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine], True)
        result={}
        for vm in object_view.view:
            if vm._moId == virtualmachine_mor:
                tools = {
                    "toolsVersion": vm.config.tools.toolsVersion,
                    "toolsStatus": str(vm.summary.guest.toolsStatus),
                    "toolsRunningStatus": str(vm.summary.guest.toolsRunningStatus)
                }
                result["name"]=vm.name
                result["moId"] = str(vm._moId)
                result["powerState"]=str(vm.runtime.powerState)
                result["resourcePool"]=vm.resourcePool._moId
                result["annotation"]=(vm.summary.config.annotation)
                result["memorySizeMB"]=vm.summary.config.memorySizeMB
                result["numCPU"] = int(vm.config.hardware.numCPU)
                result["numCoresPerSocket"]=int(vm.config.hardware.numCoresPerSocket)
                result["vmPathName"]=vm.summary.config.vmPathName
                result["VirtualDisks"]= get_vm_virtualDisk_infos(vm)
                result["VirtualNetworkAdapter"] = get_vm_VirtualNetworkAdapter_infos(vm)
                result["GuestNicInfos"] = get_vm_GuestNicInfos_infos(vm)
                result["hostName"]=vm.summary.guest.hostName
                result["ipAddress"]=vm.summary.guest.ipAddress
                result["tools"] = tools

        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result


def get_vm_virtualDisk_infos(vm):
    devices=[]
    for device in vm.config.hardware.device:
        if device._wsdlName == "VirtualDisk" :
            dev={}
            dev["capacityInKB"] = device.capacityInKB
            dev["label"] = device.deviceInfo.label
            devices.append(dev)
    return devices

def get_vm_VirtualNetworkAdapter_infos(vm):
    adaptaters = []
    for device in vm.config.hardware.device:
        if device._wsdlName in ["VirtualE1000", "VirtualE1000e", "VirtualPCNet32", "VirtualVmxnet", "VirtualNmxnet2", "VirtualVmxnet3"]:
            adap = {}
            adap["DeviceType"] = device._wsdlName
            adap["macAddress"] = device.macAddress
            adap["label"] = device.deviceInfo.label
            adaptaters.append(adap)
    return adaptaters

def get_vm_GuestNicInfos_infos(vm):
    devices=[]
    for guestnicinfos in vm.guest.net:
        dev={}
        dev["Network"]=guestnicinfos.network
        dev["ipAddress"]=guestnicinfos.ipAddress
        dev["macAddress"]=guestnicinfos.macAddress
        dev["connected"] =guestnicinfos.connected
        # TODO  if guestnicinfos.dnsConfig incluse a NetDnsConfigInfos
        dev["dnsConfig"]=None
        aux = guestnicinfos.dnsConfig
        if aux:
            dnsConfig={}
            dnsConfig["dhcp"]=aux.dhcp
            dnsConfig["domainName"] =aux.domainName
            dnsConfig["hostName"] =aux.hostName
            dnsConfig["ipAddress"] =aux.ipAddress
            dev["dnsConfig"] = dnsConfig
        devices.append(dev)
    return devices
