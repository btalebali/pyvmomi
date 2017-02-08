#!/usr/bin/env python

import atexit
import ssl
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import json

#from samples.tools import cli
#from samples.tools import vm




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



def list_RessourcesPool_and_VM_in_cluster(host, user, pwd, port, Clustermor):
    """
    :param host:
    :param user:
    :param pwd:
    :param port:
    :param vDCmor:
    :param Clustermor:
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

        for resourcepool in object_view.view:
            if (resourcepool.parent._moId == Clustermor):

                rpdict={}
                rpdict["id"] = str(resourcepool._moId)
                rpdict["name"] = str(resourcepool.name)

                vms = resourcepool.vm
                # if VM exists => Add VM to dict
                if len(vms)>0:
                    rpdict["vms"] = get_VMS(vms)
                resourcepools = resourcepool.resourcePool
                if len(resourcepools) > 0:
                    rpdict["resources_pool"]=get_RPS_VMs(resourcepools)



        object_view.Destroy()
        result = json.dumps(rpdict)
        return result
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
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

def get_RPS_VMs(resourcepools):
    RPS = []
    for rp in resourcepools:
        childrp=rp.resourcePool
        if not childrp:
            RPS.append(get_rpdicts(rp))
        else:
            RPS.append(get_rpdicts(rp))
#            RPS2 = []
#            for chrp in childrp:
#                RPS2.append(get_rpdicts(chrp))
#            RPS.append(RPS2)
    return RPS


def get_rpdicts(rp):
    rpdict = {}
    rpdict["id"] = str(rp._moId)
    rpdict["name"] = str(rp.name)
    vms = rp.vm
    # if VM exists => Add VM to dict
    if len(vms) > 0:
        rpdict["vms"] = get_VMS(vms)
    return rpdict