#!/usr/bin/env python

import atexit
import ssl
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import json
import time
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

def get_vdc_info(host,user,pwd,port, vDCmor):
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
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.Datacenter], True)
        result={}
        for obj in object_view.view:
            if obj._moId == vDCmor:
                a=[]
                for datastore in obj.datastore:
                    a.append(datastore.name)
                result['datastore']=a
                net = []
                for network in obj.network:
                    net.append(network.name)
                result['network'] = net
                a = []
                for cluster in obj.hostFolder.childEntity:
                    for host in cluster.host:
                        a.append(host.name)
                result['hosts'] = a
        object_view.Destroy()

        return json.dumps(result,sort_keys=True)
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
                hosts = obj.host
                for host in hosts:
                    result[host.name]=host._moId
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result




def list_modele_in_vDC(host, user, pwd, port, vDCmor ):
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
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine], True)
        result={}
        for obj in object_view.view:
            vdcmor = get_vDCmor_by_vm(obj)
            if vdcmor == vDCmor:
                if "MarkAsTemplate" in obj.disabledMethod and not ("MarkAsVirtualMachine" in obj.disabledMethod):
                    result[obj.name]=obj._moId
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result
def get_vDCmor_by_vm(obj):
    parent=obj.parent
    while parent._wsdlName != "Datacenter":
        parent = parent.parent
    return parent._moId




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








def list_standard_vswitch_in_vDC(host, user, pwd, port, vDCmor):
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
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.Network], True)
        result={}
        for obj in object_view.view:
            if obj.parent.parent._moId == vDCmor and obj._wsdlName=='Network' :
                result[obj.name] = obj._moId
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result



def list_distributed_vswitch_in_vDC(host, user, pwd, port, vDCmor):
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
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.VmwareDistributedVirtualSwitch], True)
        result=[]
        for obj in object_view.view:
            if obj.parent.parent._moId == vDCmor:
                dvs={}
                dvs["name"]=obj.name
                dvs["uuid"] =obj.uuid
                dvs["moId"] = obj._moId
                result.append(dvs)
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result


def list_distributed_virtual_portgroups_in_vDC(host, user, pwd, port, dVSmor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param dVSmor:
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
        object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.DistributedVirtualPortgroup], True)
        result=[]
        for obj in object_view.view:
            if obj.config.distributedVirtualSwitch._moId==dVSmor:
                dpg={}
                dpg["name"]=obj.name
                dpg["moId"] = obj._moId
                result.append(dpg)
        object_view.Destroy()
        return json.dumps(result,sort_keys=True)
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result







def list_folders_and_vm_in_vdc(host, user, pwd, port, vDCmor, folder = None):
    try:
        init = (folder is None)

        if init:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.verify_mode = ssl.CERT_NONE
            service_instance = connect.SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
            if not service_instance:
                result = "Could not connect to the specified host using specified username and password"
                return result
            atexit.register(connect.Disconnect, service_instance)
            content = service_instance.RetrieveContent()
            object_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.Datacenter], True)
            datacenters = object_view.view
            object_view.Destroy()
            for d in datacenters:
                if d._moId == vDCmor:
                    folder = d.vmFolder
                    break

        data = {
            "id": str(folder._moId),
            "name": folder.name,
            "child_folders": [],
            "vms": get_VMS2(folder)
        }

        for child_entity in folder.childEntity:
            if child_entity._wsdlName=="Folder":
                data["child_folders"].append(list_folders_and_vm_in_vdc(host, user, pwd, port, vDCmor,  child_entity))

        return json.dumps(data, sort_keys=True) if init else data
    except vmodl.MethodFault as e:
        result = "Caught vmodl fault : {}".format(e.msg)
        return result


def get_VMS2(folder1):
    VMS = []
    for childentity in folder1.childEntity:
        vmdict = {}
        if childentity._wsdlName=="VirtualMachine":
            vmdict["id"] = str(childentity._moId)
            vmdict["name"] = str(childentity.name)
            vmdict["status"] = str(childentity.summary.runtime.powerState)
            VMS.append(vmdict)
    return VMS


def clone_object(host, user, pwd, port, vm_name, template_or_vm_mor, datastore_mor, resourcepool_mor ):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        datastore = get_obj(content, [vim.Datastore], datastore_mor)
        resourcepool = get_obj(content, [vim.ResourcePool], resourcepool_mor)
        template_vm = get_obj(content, [vim.VirtualMachine], template_or_vm_mor)

        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resourcepool


        clonespec = vim.vm.CloneSpec()
        clonespec.powerOn = False
        clonespec.template = False
        clonespec.location = relospec

        task = template_vm.Clone(folder = template_vm.parent, name = vm_name, spec = clonespec)
        result = WaitTask(task, 'VM clone task')
        return result

    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result



#Get the vsphere object associated with a given text name

def get_obj(content, vimtype, moId):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c._moId == moId:
            obj = c
            break
    return obj


"""
 Waits and provides updates on a vSphere task
"""


def WaitTask(task, actionName='job', hideResult=False):
    # print 'Waiting for %s to complete.' % actionName

    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(2)

    if task.info.state == vim.TaskInfo.State.success:
        if task.info.result is not None and not hideResult:
            out = '%s completed successfully, result: %s' % (actionName, task.info.result)
        else:
            out = '%s completed successfully.' % actionName
    else:
        out = '%s did not complete successfully: %s' % (actionName, task.info.error)
        print out
        raise task.info.error  # should be a Fault... check XXX

    # may not always be applicable, but can't hurt.
    return task.info.state





def update_cpu_ram(host, user, pwd, port,vm_mor,cpu,ramMB):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        vm_obj = get_obj(content, [vim.VirtualMachine], vm_mor)

        vmconf = vim.vm.ConfigSpec()
        vmconf.numCPUs = int(cpu)
        vmconf.memoryMB = int(ramMB)
        vmconf.cpuHotAddEnabled = True
        vmconf.memoryHotAddEnabled = True
        task=vm_obj.ReconfigVM_Task(spec=vmconf)
        result = WaitTask(task)
        return result

    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result





def update_capacity_virtualdisk(host, user, pwd, port, vm_mor, new_capacity_virtualdisk_in_gb, unit_number=1):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        vm_obj = get_obj(content, [vim.VirtualMachine], vm_mor)
        new_capacity_in_kb = 1024 * 1024 * new_capacity_virtualdisk_in_gb
        virtual_disk_device = None
        for dev in vm_obj.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualDisk) :
                    if dev.unitNumber == unit_number:
                        virtual_disk_device = dev
        disk_exist = True if virtual_disk_device else False
        if disk_exist:
            old_capacity_in_kb = virtual_disk_device.capacityInKB
            if new_capacity_in_kb > old_capacity_in_kb:
                disk_spec = vim.vm.device.VirtualDeviceSpec()
                disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                disk_spec.device = vim.vm.device.VirtualDisk()
                disk_spec.device.key = virtual_disk_device.key
                disk_spec.device.backing = virtual_disk_device.backing
                disk_spec.device.backing.fileName = virtual_disk_device.backing.fileName
                disk_spec.device.backing.diskMode = virtual_disk_device.backing.diskMode
                disk_spec.device.controllerKey = virtual_disk_device.controllerKey
                disk_spec.device.unitNumber = virtual_disk_device.unitNumber
                disk_spec.device.capacityInKB = long(new_capacity_in_kb)
            elif new_capacity_in_kb == old_capacity_in_kb:
                return 'Disk capacity is the same. No change need to be done.'
            else:
                return 'Reducing Virtual Hard Disk Size is not supported at this time.'
        else:
            return 'Disk Not Found'
        dev_changes = []
        dev_changes.append(disk_spec)
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = dev_changes
        task = vm_obj.ReconfigVM_Task(spec=spec)
        result = WaitTask(task)
        return result
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result




def delete_all_nic_in_vm(host, user, pwd, port, vm_mor):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        vm_obj = get_obj(content, [vim.VirtualMachine], vm_mor)
        r=[]
        spec1=vim.vm.ConfigSpec()
        spec1.deviceChange=[]
        for dev in vm_obj.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
                virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                dev.deviceInfo.label = ""
                virtual_nic_spec.device = dev
                spec1.deviceChange = [virtual_nic_spec]
                task = vm_obj.Reconfigure(spec=spec1)
                r = WaitTask(task)
        return r
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result


def delete_nic_in_vm(host, user, pwd, port, vm_mor, unitNumber):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        vm_obj = get_obj(content, [vim.VirtualMachine], vm_mor)
        r=[]
        spec1=vim.vm.ConfigSpec()
        spec1.deviceChange=[]
        for dev in vm_obj.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualEthernetCard) and dev.unitNumber== int(unitNumber):
                virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
                virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                dev.deviceInfo.label = ""
                virtual_nic_spec.device = dev
                spec1.deviceChange = [virtual_nic_spec]
                task = vm_obj.Reconfigure(spec=spec1)
                r = WaitTask(task)
                return r
        return "Network adapter not found"
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result











def add_nic_to_vm_and_connect_to_net(host, user, pwd, port, vm_mor, portgroup_or_vs_mor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param vm_mor:
    :param unitNumber:
    :param portgroup_or_dvs_mor:
    :param NET_TYPE:  vs or dvpg
    :return:
    """
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        vm_obj = get_obj(content, [vim.VirtualMachine], vm_mor)
        spec = vim.vm.ConfigSpec()
        nic_changes = []
        nic_spec = vim.vm.device.VirtualDeviceSpec()
        nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        nic_spec.device = vim.vm.device.VirtualE1000()
        nic_spec.device.deviceInfo = vim.Description()
        nic_spec.device.deviceInfo.summary = 'vCenter API test'
        content = service_instance.RetrieveContent()
        if 'network' in portgroup_or_vs_mor:
            nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
            nic_spec.device.backing.useAutoDetect = False
            net = get_obj(content, [vim.Network], portgroup_or_vs_mor)
            nic_spec.device.backing.network = net
            nic_spec.device.backing.deviceName = net.name
        if "portgroup" in portgroup_or_vs_mor:
            net = get_obj(content, [vim.DistributedVirtualPortgroup], portgroup_or_vs_mor)
            nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            port = vim.DistributedVirtualSwitchPortConnection()
            port.portgroupKey = portgroup_or_vs_mor
            port.switchUuid = net.config.distributedVirtualSwitch.uuid
            nic_spec.device.backing.port = port
        nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic_spec.device.connectable.startConnected = True
        nic_spec.device.connectable.allowGuestControl = True
        nic_spec.device.connectable.connected = False
        nic_spec.device.connectable.status = 'untried'
        nic_spec.device.wakeOnLanEnabled = True
        nic_spec.device.addressType = 'assigned'
        nic_changes.append(nic_spec)
        spec.deviceChange = nic_changes
        task = vm_obj.ReconfigVM_Task(spec=spec)
        r = WaitTask(task)
        return r
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result



def customize_nics_in_vm(host, user, pwd, port, vm_mor, NIC):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, sslContext=context)
        if not service_instance:
            result = "Could not connect to the specified host using specified username and password"
            return result
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        vm_obj = get_obj(content, [vim.VirtualMachine], vm_mor)
        ## Config ip for each nic adapter
        adaptermaps=[]
        for inputs in NIC:
            adaptermap = vim.vm.customization.AdapterMapping()
            adaptermap.adapter = vim.vm.customization.IPSettings()
            isDHDCP = inputs['isDHCP']
            if not isDHDCP:
                print "static"
                adaptermap.adapter.ip = vim.vm.customization.FixedIp()
                adaptermap.adapter.ip.ipAddress = inputs['vm_ip']
                adaptermap.adapter.subnetMask = inputs['subnet']
                adaptermap.adapter.gateway = inputs['gateway']
                adaptermap.adapter.dnsDomain = inputs['dnsdomain']
                adaptermap.adapter.dnsServerList = inputs['dns']
            else:
                print "dhcp"
                adaptermap.adapter.ip = vim.vm.customization.DhcpIpGenerator()
            adaptermaps.append(adaptermap)

        globalip = vim.vm.customization.GlobalIPSettings()
        if NIC[0]['dns']:
            globalip.dnsServerList = NIC[0]['dns']
        else:
            globalip.dnsServerList = ['8.8.8.8', '8.8.4.4']

        guestfullname = vm_obj.config.guestFullName.lower()
        if "linux" in guestfullname:
        # Identity for linux OS
            ident = vim.vm.customization.LinuxPrep(domain="doamin", hostName=vim.vm.customization.FixedName( name = "hostname"))
        if "windows" in  guestfullname:
            # Identity for Windows OS
            ident = vim.vm.customization.Sysprep()
            ident.guiUnattended = vim.vm.customization.GuiUnattended()
            ident.guiUnattended.autoLogon = False  # the machine does not auto-logon
            ident.guiUnattended.password = vim.vm.customization.Password()
            ident.guiUnattended.password.value = "Pr0l0gue:2014"
            ident.guiUnattended.password.plainText = True  # the password passed over is not encrypted
            ident.userData = vim.vm.customization.UserData()
            ident.userData.fullName = "useitcloud"
            ident.userData.orgName = "Prologue"
            ident.userData.computerName = vim.vm.customization.FixedName()
            ident.userData.computerName.name = "hostname"
            ident.identification = vim.vm.customization.Identification()


        customspec = vim.vm.customization.Specification()
        customspec.identity = ident
        customspec.nicSettingMap = adaptermaps
        customspec.globalIPSettings = globalip
        task = vm_obj.CustomizeVM_Task(spec = customspec)
        r = WaitTask(task)
        return r
    except vmodl.MethodFault as e:
            result="Caught vmodl fault : {}".format(e.msg)
            return result