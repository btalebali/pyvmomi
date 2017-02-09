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
            data["resources_pools"].append(list_RessourcesPool_and_VM_in_cluster2(host, user, pwd, port, cluster_mor, rp_resource_pool))

        return json.dumps(data, sort_keys=True) if init else data
    except vmodl.MethodFault as e:
        result = "Caught vmodl fault : {}".format(e.msg)
        return result





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
        return result
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
        return result
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
        return result
    except vmodl.MethodFault as e:
        result="Caught vmodl fault : {}".format(e.msg)
        return result

