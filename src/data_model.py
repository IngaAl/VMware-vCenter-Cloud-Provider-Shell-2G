from cloudshell.shell.core.driver_context import ResourceCommandContext, AutoLoadDetails, AutoLoadAttribute, \
    AutoLoadResource
from collections import defaultdict


class LegacyUtils(object):
    def __init__(self):
        self._datamodel_clss_dict = self.__generate_datamodel_classes_dict()

    def migrate_autoload_details(self, autoload_details, context):
        model_name = context.resource.model
        root_name = context.resource.name
        root = self.__create_resource_from_datamodel(model_name, root_name)
        attributes = self.__create_attributes_dict(autoload_details.attributes)
        self.__attach_attributes_to_resource(attributes, '', root)
        self.__build_sub_resoruces_hierarchy(root, autoload_details.resources, attributes)
        return root

    def __create_resource_from_datamodel(self, model_name, res_name):
        return self._datamodel_clss_dict[model_name](res_name)

    def __create_attributes_dict(self, attributes_lst):
        d = defaultdict(list)
        for attribute in attributes_lst:
            d[attribute.relative_address].append(attribute)
        return d

    def __build_sub_resoruces_hierarchy(self, root, sub_resources, attributes):
        d = defaultdict(list)
        for resource in sub_resources:
            splitted = resource.relative_address.split('/')
            parent = '' if len(splitted) == 1 else resource.relative_address.rsplit('/', 1)[0]
            rank = len(splitted)
            d[rank].append((parent, resource))

        self.__set_models_hierarchy_recursively(d, 1, root, '', attributes)

    def __set_models_hierarchy_recursively(self, dict, rank, manipulated_resource, resource_relative_addr, attributes):
        if rank not in dict: # validate if key exists
            pass

        for (parent, resource) in dict[rank]:
            if parent == resource_relative_addr:
                sub_resource = self.__create_resource_from_datamodel(
                    resource.model.replace(' ', ''),
                    resource.name)
                self.__attach_attributes_to_resource(attributes, resource.relative_address, sub_resource)
                manipulated_resource.add_sub_resource(
                    self.__slice_parent_from_relative_path(parent, resource.relative_address), sub_resource)
                self.__set_models_hierarchy_recursively(
                    dict,
                    rank + 1,
                    sub_resource,
                    resource.relative_address,
                    attributes)

    def __attach_attributes_to_resource(self, attributes, curr_relative_addr, resource):
        for attribute in attributes[curr_relative_addr]:
            setattr(resource, attribute.attribute_name.lower().replace(' ', '_'), attribute.attribute_value)
        del attributes[curr_relative_addr]

    def __slice_parent_from_relative_path(self, parent, relative_addr):
        if parent is '':
            return relative_addr
        return relative_addr[len(parent) + 1:] # + 1 because we want to remove the seperator also

    def __generate_datamodel_classes_dict(self):
        return dict(self.__collect_generated_classes())

    def __collect_generated_classes(self):
        import sys, inspect
        return inspect.getmembers(sys.modules[__name__], inspect.isclass)


class VmwareVcenterCloudProvider2G(object):
    def __init__(self, name):
        """
        
        """
        self.attributes = {}
        self.resources = {}
        self._cloudshell_model_name = 'VMware vCenter Cloud Provider 2G'
        self._name = name

    def add_sub_resource(self, relative_path, sub_resource):
        self.resources[relative_path] = sub_resource

    @classmethod
    def create_from_context(cls, context):
        """
        Creates an instance of NXOS by given context
        :param context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :type context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :return:
        :rtype VmwareVcenterCloudProvider2G
        """
        result = VmwareVcenterCloudProvider2G(name=context.resource.name)
        for attr in context.resource.attributes:
            result.attributes[attr] = context.resource.attributes[attr]
        return result

    def create_autoload_details(self, relative_path=''):
        """
        :param relative_path:
        :type relative_path: str
        :return
        """
        resources = [AutoLoadResource(model=self.resources[r].cloudshell_model_name,
            name=self.resources[r].name,
            relative_address=self._get_relative_path(r, relative_path))
            for r in self.resources]
        attributes = [AutoLoadAttribute(relative_path, a, self.attributes[a]) for a in self.attributes]
        autoload_details = AutoLoadDetails(resources, attributes)
        for r in self.resources:
            curr_path = relative_path + '/' + r if relative_path else r
            curr_auto_load_details = self.resources[r].create_autoload_details(curr_path)
            autoload_details = self._merge_autoload_details(autoload_details, curr_auto_load_details)
        return autoload_details

    def _get_relative_path(self, child_path, parent_path):
        """
        Combines relative path
        :param child_path: Path of a model within it parent model, i.e 1
        :type child_path: str
        :param parent_path: Full path of parent model, i.e 1/1. Might be empty for root model
        :type parent_path: str
        :return: Combined path
        :rtype str
        """
        return parent_path + '/' + child_path if parent_path else child_path

    @staticmethod
    def _merge_autoload_details(autoload_details1, autoload_details2):
        """
        Merges two instances of AutoLoadDetails into the first one
        :param autoload_details1:
        :type autoload_details1: AutoLoadDetails
        :param autoload_details2:
        :type autoload_details2: AutoLoadDetails
        :return:
        :rtype AutoLoadDetails
        """
        for attribute in autoload_details2.attributes:
            autoload_details1.attributes.append(attribute)
        for resource in autoload_details2.resources:
            autoload_details1.resources.append(resource)
        return autoload_details1

    @property
    def cloudshell_model_name(self):
        """
        Returns the name of the Cloudshell model
        :return:
        """
        return 'VmwareVcenterCloudProvider2G'

    @property
    def user(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.User'] if 'VMware vCenter Cloud Provider 2G.User' in self.attributes else None

    @user.setter
    def user(self, value):
        """
        
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.User'] = value

    @property
    def password(self):
        """
        :rtype: string
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Password'] if 'VMware vCenter Cloud Provider 2G.Password' in self.attributes else None

    @password.setter
    def password(self, value):
        """
        
        :type value: string
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Password'] = value

    @property
    def default_datacenter(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Default Datacenter'] if 'VMware vCenter Cloud Provider 2G.Default Datacenter' in self.attributes else None

    @default_datacenter.setter
    def default_datacenter(self, value):
        """
        The datacenter within the vCenter that will be used for VM deployment. All other settings of this vCenter resource should refer to entities associated with this datacenter.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Default Datacenter'] = value

    @property
    def default_dvswitch(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Default dvSwitch'] if 'VMware vCenter Cloud Provider 2G.Default dvSwitch' in self.attributes else None

    @default_dvswitch.setter
    def default_dvswitch(self, value):
        """
        The default vCenter vSwitch or dvSwitch that will be used when configuring VM connectivity. Should be under the Default Datacenter.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Default dvSwitch'] = value

    @property
    def holding_network(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Holding Network'] if 'VMware vCenter Cloud Provider 2G.Holding Network' in self.attributes else None

    @holding_network.setter
    def holding_network(self, value):
        """
        The default network that will be configured when disconnecting from another network. Should be under the Default Datacenter.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Holding Network'] = value

    @property
    def vm_cluster(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.VM Cluster'] if 'VMware vCenter Cloud Provider 2G.VM Cluster' in self.attributes else None

    @vm_cluster.setter
    def vm_cluster(self, value):
        """
        The vCenter cluster or host that will be used when deploying a VM. Should be under the Default Datacenter.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.VM Cluster'] = value

    @property
    def vm_resource_pool(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.VM Resource Pool'] if 'VMware vCenter Cloud Provider 2G.VM Resource Pool' in self.attributes else None

    @vm_resource_pool.setter
    def vm_resource_pool(self, value):
        """
        The vCenter Resource Pool in which the VM will be created. Should be under the defined VM Cluster (optional).
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.VM Resource Pool'] = value

    @property
    def vm_storage(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.VM Storage'] if 'VMware vCenter Cloud Provider 2G.VM Storage' in self.attributes else None

    @vm_storage.setter
    def vm_storage(self, value):
        """
        The vCenter storage in which the VMs will be created. The storage can be either a datastore or a datastore cluster. For example: datastore1 (To use a specific datastore inside a cluster, specify the cluster name and the datastore name. For example: clustername/datastore1)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.VM Storage'] = value

    @property
    def saved_sandbox_storage(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Saved Sandbox Storage'] if 'VMware vCenter Cloud Provider 2G.Saved Sandbox Storage' in self.attributes else None

    @saved_sandbox_storage.setter
    def saved_sandbox_storage(self, value):
        """
        The vCenter storage in which the content of saved sandboxes will be created. The storage can be either a datastore or a datastore cluster. For example: datastore1  or clustername/datastore1 (for datastore inside a cluster)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Saved Sandbox Storage'] = value

    @property
    def behavior_during_save(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Behavior during save'] if 'VMware vCenter Cloud Provider 2G.Behavior during save' in self.attributes else None

    @behavior_during_save.setter
    def behavior_during_save(self, value):
        """
        Determines the VM behavior when the sandbox is saved. If Power off is selected, and the VM was powered on before the save, then the VM will shut down for the duration of the save, and then be powered on at the end.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Behavior during save'] = value

    @property
    def vm_location(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.VM Location'] if 'VMware vCenter Cloud Provider 2G.VM Location' in self.attributes else None

    @vm_location.setter
    def vm_location(self, value):
        """
        The full path to the folder within vCenter in which the VM will be created. (e.g vms/quali)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.VM Location'] = value

    @property
    def shutdown_method(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Shutdown Method'] if 'VMware vCenter Cloud Provider 2G.Shutdown Method' in self.attributes else None

    @shutdown_method.setter
    def shutdown_method(self, value):
        """
        The shutdown method that will be used when powering off the VM. Possible options are 'Hard' and 'Soft' shutdown.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Shutdown Method'] = value

    @property
    def ovf_tool_path(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.OVF Tool Path'] if 'VMware vCenter Cloud Provider 2G.OVF Tool Path' in self.attributes else None

    @ovf_tool_path.setter
    def ovf_tool_path(self, value):
        """
        The path for the OVF tool installation. Use the same path for all execution servers.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.OVF Tool Path'] = value

    @property
    def reserved_networks(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Reserved Networks'] if 'VMware vCenter Cloud Provider 2G.Reserved Networks' in self.attributes else None

    @reserved_networks.setter
    def reserved_networks(self, value):
        """
        Reserved networks separated by Semicolon(;), vNICs configured to those networks won't be used for VM connectivity.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Reserved Networks'] = value

    @property
    def promiscuous_mode(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Promiscuous Mode'] if 'VMware vCenter Cloud Provider 2G.Promiscuous Mode' in self.attributes else None

    @promiscuous_mode.setter
    def promiscuous_mode(self, value):
        """
        If enabled the port groups on the virtual switch will be configured to allow promiscuous mode.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Promiscuous Mode'] = value

    @property
    def connectivity_provider(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Connectivity Provider'] if 'VMware vCenter Cloud Provider 2G.Connectivity Provider' in self.attributes else None

    @connectivity_provider.setter
    def connectivity_provider(self, value):
        """
        
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Connectivity Provider'] = value

    @property
    def networking_type(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Networking type'] if 'VMware vCenter Cloud Provider 2G.Networking type' in self.attributes else None

    @networking_type.setter
    def networking_type(self, value):
        """
        Networking type that the cloud provider implements - L2 networking (VLANs) or L3 (Subnets).
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Networking type'] = value

    @property
    def region(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Region'] if 'VMware vCenter Cloud Provider 2G.Region' in self.attributes else None

    @region.setter
    def region(self, value=''):
        """
        The public cloud region to be used by this cloud provider.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Region'] = value

    @property
    def networks_in_use(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.Networks in use'] if 'VMware vCenter Cloud Provider 2G.Networks in use' in self.attributes else None

    @networks_in_use.setter
    def networks_in_use(self, value=''):
        """
        Reserved network ranges to be excluded when allocated sandbox networks (for cloud providers with L3 networking). The syntax is a comma-separated CIDR list. For example, "10.0.0.0/24, 10.1.0.0/26."
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.Networks in use'] = value

    @property
    def vlan_type(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.VLAN Type'] if 'VMware vCenter Cloud Provider 2G.VLAN Type' in self.attributes else None

    @vlan_type.setter
    def vlan_type(self, value='VLAN'):
        """
        Whether to use VLAN or VXLAN (for cloud providers with L2 networking).
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.VLAN Type'] = value

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        
        :type value: str
        """
        self._name = value

    @property
    def cloudshell_model_name(self):
        """
        :rtype: str
        """
        return self._cloudshell_model_name

    @cloudshell_model_name.setter
    def cloudshell_model_name(self, value):
        """
        
        :type value: str
        """
        self._cloudshell_model_name = value


class VcenterVMFromVM2G(object):
    def __init__(self, name):
        """
        
        """
        self.attributes = {}
        self.resources = {}
        self._cloudshell_model_name = 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G'
        self._name = name

    def add_sub_resource(self, relative_path, sub_resource):
        self.resources[relative_path] = sub_resource

    @classmethod
    def create_from_context(cls, context):
        """
        Creates an instance of NXOS by given context
        :param context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :type context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :return:
        :rtype VcenterVMFromVM2G
        """
        result = VcenterVMFromVM2G(name=context.resource.name)
        for attr in context.resource.attributes:
            result.attributes[attr] = context.resource.attributes[attr]
        return result

    def create_autoload_details(self, relative_path=''):
        """
        :param relative_path:
        :type relative_path: str
        :return
        """
        resources = [AutoLoadResource(model=self.resources[r].cloudshell_model_name,
            name=self.resources[r].name,
            relative_address=self._get_relative_path(r, relative_path))
            for r in self.resources]
        attributes = [AutoLoadAttribute(relative_path, a, self.attributes[a]) for a in self.attributes]
        autoload_details = AutoLoadDetails(resources, attributes)
        for r in self.resources:
            curr_path = relative_path + '/' + r if relative_path else r
            curr_auto_load_details = self.resources[r].create_autoload_details(curr_path)
            autoload_details = self._merge_autoload_details(autoload_details, curr_auto_load_details)
        return autoload_details

    def _get_relative_path(self, child_path, parent_path):
        """
        Combines relative path
        :param child_path: Path of a model within it parent model, i.e 1
        :type child_path: str
        :param parent_path: Full path of parent model, i.e 1/1. Might be empty for root model
        :type parent_path: str
        :return: Combined path
        :rtype str
        """
        return parent_path + '/' + child_path if parent_path else child_path

    @staticmethod
    def _merge_autoload_details(autoload_details1, autoload_details2):
        """
        Merges two instances of AutoLoadDetails into the first one
        :param autoload_details1:
        :type autoload_details1: AutoLoadDetails
        :param autoload_details2:
        :type autoload_details2: AutoLoadDetails
        :return:
        :rtype AutoLoadDetails
        """
        for attribute in autoload_details2.attributes:
            autoload_details1.attributes.append(attribute)
        for resource in autoload_details2.resources:
            autoload_details1.resources.append(resource)
        return autoload_details1

    @property
    def cloudshell_model_name(self):
        """
        Returns the name of the Cloudshell model
        :return:
        """
        return 'VcenterVMFromVM2G'

    @property
    def vcenter_vm(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.vCenter VM'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.vCenter VM' in self.attributes else None

    @vcenter_vm.setter
    def vcenter_vm(self, value):
        """
        vCenter VM to use in the VM creation. Should include the full path and the vm name, for example QualiFolder/VM121
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.vCenter VM'] = value

    @property
    def vm_cluster(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Cluster'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Cluster' in self.attributes else None

    @vm_cluster.setter
    def vm_cluster(self, value):
        """
        The vCenter cluster or host that will be used when deploying a VM. Should be under the Default Datacenter.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Cluster'] = value

    @property
    def vm_storage(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Storage'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Storage' in self.attributes else None

    @vm_storage.setter
    def vm_storage(self, value):
        """
        The vCenter storage in which the VMs will be created. The storage can be either a datastore or a datastore cluster. For example: datastore1 (To use a specific datastore inside a cluster, specify the cluster name and the datastore name. For example: clustername/datastore1)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Storage'] = value

    @property
    def behavior_during_save(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Behavior during save'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Behavior during save' in self.attributes else None

    @behavior_during_save.setter
    def behavior_during_save(self, value='Remain Powered On'):
        """
        Determines the VM behavior when the sandbox is saved. If Power off is selected, and the VM was powered on before the save, then the VM will shut down for the duration of the save, and then be powered on at the end.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Behavior during save'] = value

    @property
    def vm_resource_pool(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Resource Pool'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Resource Pool' in self.attributes else None

    @vm_resource_pool.setter
    def vm_resource_pool(self, value):
        """
        The vCenter Resource Pool in which the VM will be created. Should be under the defined V M Cluster (optional).
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Resource Pool'] = value

    @property
    def vm_location(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Location'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Location' in self.attributes else None

    @vm_location.setter
    def vm_location(self, value):
        """
        The full path to the folder within vCenter in which the VM will be created. (e.g vms/quali)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.VM Location'] = value

    @property
    def auto_power_on(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Auto Power On'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Auto Power On' in self.attributes else None

    @auto_power_on.setter
    def auto_power_on(self, value=True):
        """
        Enables the automatic power on of an app following its deployment during reservation Setup.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Auto Power On'] = value

    @property
    def auto_power_off(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Auto Power Off'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Auto Power Off' in self.attributes else None

    @auto_power_off.setter
    def auto_power_off(self, value=True):
        """
        Enables the automatic power off of an app during reservation Teardown.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Auto Power Off'] = value

    @property
    def wait_for_ip(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Wait for IP'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Wait for IP' in self.attributes else None

    @wait_for_ip.setter
    def wait_for_ip(self, value=True):
        """
        If set to False the deployment will not wait for the VM to get an IP.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Wait for IP'] = value

    @property
    def auto_delete(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Auto Delete'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Auto Delete' in self.attributes else None

    @auto_delete.setter
    def auto_delete(self, value=True):
        """
        Enables automatic deletion of an app during reservation Teardown.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Auto Delete'] = value

    @property
    def autoload(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Autoload'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Autoload' in self.attributes else None

    @autoload.setter
    def autoload(self, value=True):
        """
        Enables the automatic execution of the Autoload command during reservation Setup.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Autoload'] = value

    @property
    def ip_regex(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.IP Regex'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.IP Regex' in self.attributes else None

    @ip_regex.setter
    def ip_regex(self, value):
        """
        Filters the IP that can be selected as an App's address.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.IP Regex'] = value

    @property
    def refresh_ip_timeout(self):
        """
        :rtype: float
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Refresh IP Timeout'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Refresh IP Timeout' in self.attributes else None

    @refresh_ip_timeout.setter
    def refresh_ip_timeout(self, value='600'):
        """
        Timeout for waiting when obtaining IP address (in seconds)
        :type value: float
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Refresh IP Timeout'] = value

    @property
    def customization_spec(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Customization Spec'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Customization Spec' in self.attributes else None

    @customization_spec.setter
    def customization_spec(self, value):
        """
        (Only applies to Windows and Linux VMs) Name of the vSphere VM customization specification to apply on the deployed VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Customization Spec'] = value

    @property
    def hostname(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Hostname'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Hostname' in self.attributes else None

    @hostname.setter
    def hostname(self, value):
        """
        (Only applies to Windows and Linux VMs) The hostname to set on the VM. If Customization Spec is specified, the value specified in the Hostname parameter will be used. Note: If Customization Spec is not specified, a new one will be created for the VM. For Windows VMs, make sure to specify a password in the App resource page
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Hostname'] = value

    @property
    def private_ip(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Private IP'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Private IP' in self.attributes else None

    @private_ip.setter
    def private_ip(self, value=''):
        """
        (Only applies to Windows and Linux VMs) The private static IP to set on the first vNIC of the VM. If Customization Spec is specified, the value specified in the Private IP parameter will be used. Note: If Customization Spec is not specified, a new one will be created for the VM. For Windows VMs, make sure to specify a password in the App resource page
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.Private IP'] = value

    @property
    def cpu(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.CPU'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.CPU' in self.attributes else None

    @cpu.setter
    def cpu(self, value):
        """
        The number of CPUs to be configured on the VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.CPU'] = value

    @property
    def ram(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.RAM'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.RAM' in self.attributes else None

    @ram.setter
    def ram(self, value):
        """
        The amount of RAM (GB) to be configured on the VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.RAM'] = value

    @property
    def hdd(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.HDD'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.HDD' in self.attributes else None

    @hdd.setter
    def hdd(self, value):
        """
        Allows to add/edit hard disk size by their number on the VM. The syntax is comma-separated disk pairs Hard Disk Label: Disk Size (GB). Example: 'Hard Disk 1:100;Hard Disk 2:200'. Shortened format is also valid: '1:100;2:200'
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From VM 2G.HDD'] = value

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        
        :type value: str
        """
        self._name = value

    @property
    def cloudshell_model_name(self):
        """
        :rtype: str
        """
        return self._cloudshell_model_name

    @cloudshell_model_name.setter
    def cloudshell_model_name(self, value):
        """
        
        :type value: str
        """
        self._cloudshell_model_name = value


class VcenterVMFromTemplate2G(object):
    def __init__(self, name):
        """
        
        """
        self.attributes = {}
        self.resources = {}
        self._cloudshell_model_name = 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G'
        self._name = name

    def add_sub_resource(self, relative_path, sub_resource):
        self.resources[relative_path] = sub_resource

    @classmethod
    def create_from_context(cls, context):
        """
        Creates an instance of NXOS by given context
        :param context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :type context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :return:
        :rtype VcenterVMFromTemplate2G
        """
        result = VcenterVMFromTemplate2G(name=context.resource.name)
        for attr in context.resource.attributes:
            result.attributes[attr] = context.resource.attributes[attr]
        return result

    def create_autoload_details(self, relative_path=''):
        """
        :param relative_path:
        :type relative_path: str
        :return
        """
        resources = [AutoLoadResource(model=self.resources[r].cloudshell_model_name,
            name=self.resources[r].name,
            relative_address=self._get_relative_path(r, relative_path))
            for r in self.resources]
        attributes = [AutoLoadAttribute(relative_path, a, self.attributes[a]) for a in self.attributes]
        autoload_details = AutoLoadDetails(resources, attributes)
        for r in self.resources:
            curr_path = relative_path + '/' + r if relative_path else r
            curr_auto_load_details = self.resources[r].create_autoload_details(curr_path)
            autoload_details = self._merge_autoload_details(autoload_details, curr_auto_load_details)
        return autoload_details

    def _get_relative_path(self, child_path, parent_path):
        """
        Combines relative path
        :param child_path: Path of a model within it parent model, i.e 1
        :type child_path: str
        :param parent_path: Full path of parent model, i.e 1/1. Might be empty for root model
        :type parent_path: str
        :return: Combined path
        :rtype str
        """
        return parent_path + '/' + child_path if parent_path else child_path

    @staticmethod
    def _merge_autoload_details(autoload_details1, autoload_details2):
        """
        Merges two instances of AutoLoadDetails into the first one
        :param autoload_details1:
        :type autoload_details1: AutoLoadDetails
        :param autoload_details2:
        :type autoload_details2: AutoLoadDetails
        :return:
        :rtype AutoLoadDetails
        """
        for attribute in autoload_details2.attributes:
            autoload_details1.attributes.append(attribute)
        for resource in autoload_details2.resources:
            autoload_details1.resources.append(resource)
        return autoload_details1

    @property
    def cloudshell_model_name(self):
        """
        Returns the name of the Cloudshell model
        :return:
        """
        return 'VcenterVMFromTemplate2G'

    @property
    def vcenter_template(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.vCenter Template'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.vCenter Template' in self.attributes else None

    @vcenter_template.setter
    def vcenter_template(self, value):
        """
        vCenter VM template to use in the VM creation. Should include the full path and the template name, for example QualiFolder/Template1
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.vCenter Template'] = value

    @property
    def vm_cluster(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Cluster'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Cluster' in self.attributes else None

    @vm_cluster.setter
    def vm_cluster(self, value):
        """
        The vCenter cluster or host that will be used when deploying a VM. Should be under the Default Datacenter.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Cluster'] = value

    @property
    def vm_storage(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Storage'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Storage' in self.attributes else None

    @vm_storage.setter
    def vm_storage(self, value):
        """
        The vCenter storage in which the VMs will be created. The storage can be either a datastore or a datastore cluster. For example: datastore1 (To use a specific datastore inside a cluster, specify the cluster name and the datastore name. For example: clustername/datastore1)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Storage'] = value

    @property
    def behavior_during_save(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Behavior during save'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Behavior during save' in self.attributes else None

    @behavior_during_save.setter
    def behavior_during_save(self, value='Remain Powered On'):
        """
        Determines the VM behavior when the sandbox is saved. If Power off is selected, and the VM was powered on before the save, then the VM will shut down for the duration of the save, and then be powered on at the end.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Behavior during save'] = value

    @property
    def vm_resource_pool(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Resource Pool'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Resource Pool' in self.attributes else None

    @vm_resource_pool.setter
    def vm_resource_pool(self, value):
        """
        The vCenter Resource Pool in which the VM will be created. Should be under the defined VM Cluster (optional).
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Resource Pool'] = value

    @property
    def vm_location(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Location'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Location' in self.attributes else None

    @vm_location.setter
    def vm_location(self, value):
        """
        The full path to the folder within vCenter in which the VM will be created. (e.g vms/quali)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.VM Location'] = value

    @property
    def auto_power_on(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Auto Power On'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Auto Power On' in self.attributes else None

    @auto_power_on.setter
    def auto_power_on(self, value=True):
        """
        Enables the automatic power on of an app following its deployment during reservation Setup.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Auto Power On'] = value

    @property
    def auto_power_off(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Auto Power Off'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Auto Power Off' in self.attributes else None

    @auto_power_off.setter
    def auto_power_off(self, value=True):
        """
        Enables the automatic power off of an app during reservation Teardown.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Auto Power Off'] = value

    @property
    def wait_for_ip(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Wait for IP'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Wait for IP' in self.attributes else None

    @wait_for_ip.setter
    def wait_for_ip(self, value=True):
        """
        If set to False the deployment will not wait for the VM to get an IP.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Wait for IP'] = value

    @property
    def auto_delete(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Auto Delete'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Auto Delete' in self.attributes else None

    @auto_delete.setter
    def auto_delete(self, value=True):
        """
        Enables automatic deletion of an app during reservation Teardown.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Auto Delete'] = value

    @property
    def autoload(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Autoload'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Autoload' in self.attributes else None

    @autoload.setter
    def autoload(self, value=True):
        """
        Enables the automatic execution of the Autoload command during reservation Setup.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Autoload'] = value

    @property
    def ip_regex(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.IP Regex'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.IP Regex' in self.attributes else None

    @ip_regex.setter
    def ip_regex(self, value):
        """
        Filters the IP that can be selected as an App's address.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.IP Regex'] = value

    @property
    def refresh_ip_timeout(self):
        """
        :rtype: float
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Refresh IP Timeout'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Refresh IP Timeout' in self.attributes else None

    @refresh_ip_timeout.setter
    def refresh_ip_timeout(self, value='600'):
        """
        Timeout for waiting when obtaining IP address (in seconds)
        :type value: float
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Refresh IP Timeout'] = value

    @property
    def customization_spec(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Customization Spec'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Customization Spec' in self.attributes else None

    @customization_spec.setter
    def customization_spec(self, value):
        """
        (Only applies to Windows and Linux VMs) Name of the vSphere VM customization specification to apply on the deployed VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Customization Spec'] = value

    @property
    def hostname(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Hostname'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Hostname' in self.attributes else None

    @hostname.setter
    def hostname(self, value):
        """
        (Only applies to Windows and Linux VMs) The hostname to set on the VM. If Customization Spec is specified, the value specified in the Hostname parameter will be used. Note: If Customization Spec is not specified, a new one will be created for the VM. For Windows VMs, make sure to specify a password in the App resource page
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Hostname'] = value

    @property
    def private_ip(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Private IP'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Private IP' in self.attributes else None

    @private_ip.setter
    def private_ip(self, value=''):
        """
        (Only applies to Windows and Linux VMs) The private static IP to set on the first vNIC of the VM. If Customization Spec is specified, the value specified in the Private IP parameter will be used. Note: If Customization Spec is not specified, a new one will be created for the VM. For Windows VMs, make sure to specify a password in the App resource page
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.Private IP'] = value

    @property
    def cpu(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.CPU'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.CPU' in self.attributes else None

    @cpu.setter
    def cpu(self, value):
        """
        The number of CPUs to be configured on the VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.CPU'] = value

    @property
    def ram(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.RAM'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.RAM' in self.attributes else None

    @ram.setter
    def ram(self, value):
        """
        The amount of RAM (GB) to be configured on the VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.RAM'] = value

    @property
    def hdd(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.HDD'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.HDD' in self.attributes else None

    @hdd.setter
    def hdd(self, value):
        """
        Allows to add/edit hard disk size by their number on the VM. The syntax is comma-separated disk pairs Hard Disk Label: Disk Size (GB). Example: 'Hard Disk 1:100;Hard Disk 2:200'. Shortened format is also valid: '1:100;2:200'
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Template 2G.HDD'] = value

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        
        :type value: str
        """
        self._name = value

    @property
    def cloudshell_model_name(self):
        """
        :rtype: str
        """
        return self._cloudshell_model_name

    @cloudshell_model_name.setter
    def cloudshell_model_name(self, value):
        """
        
        :type value: str
        """
        self._cloudshell_model_name = value


class VcenterVMFromLinkedClone2G(object):
    def __init__(self, name):
        """
        
        """
        self.attributes = {}
        self.resources = {}
        self._cloudshell_model_name = 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G'
        self._name = name

    def add_sub_resource(self, relative_path, sub_resource):
        self.resources[relative_path] = sub_resource

    @classmethod
    def create_from_context(cls, context):
        """
        Creates an instance of NXOS by given context
        :param context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :type context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :return:
        :rtype VcenterVMFromLinkedClone2G
        """
        result = VcenterVMFromLinkedClone2G(name=context.resource.name)
        for attr in context.resource.attributes:
            result.attributes[attr] = context.resource.attributes[attr]
        return result

    def create_autoload_details(self, relative_path=''):
        """
        :param relative_path:
        :type relative_path: str
        :return
        """
        resources = [AutoLoadResource(model=self.resources[r].cloudshell_model_name,
            name=self.resources[r].name,
            relative_address=self._get_relative_path(r, relative_path))
            for r in self.resources]
        attributes = [AutoLoadAttribute(relative_path, a, self.attributes[a]) for a in self.attributes]
        autoload_details = AutoLoadDetails(resources, attributes)
        for r in self.resources:
            curr_path = relative_path + '/' + r if relative_path else r
            curr_auto_load_details = self.resources[r].create_autoload_details(curr_path)
            autoload_details = self._merge_autoload_details(autoload_details, curr_auto_load_details)
        return autoload_details

    def _get_relative_path(self, child_path, parent_path):
        """
        Combines relative path
        :param child_path: Path of a model within it parent model, i.e 1
        :type child_path: str
        :param parent_path: Full path of parent model, i.e 1/1. Might be empty for root model
        :type parent_path: str
        :return: Combined path
        :rtype str
        """
        return parent_path + '/' + child_path if parent_path else child_path

    @staticmethod
    def _merge_autoload_details(autoload_details1, autoload_details2):
        """
        Merges two instances of AutoLoadDetails into the first one
        :param autoload_details1:
        :type autoload_details1: AutoLoadDetails
        :param autoload_details2:
        :type autoload_details2: AutoLoadDetails
        :return:
        :rtype AutoLoadDetails
        """
        for attribute in autoload_details2.attributes:
            autoload_details1.attributes.append(attribute)
        for resource in autoload_details2.resources:
            autoload_details1.resources.append(resource)
        return autoload_details1

    @property
    def cloudshell_model_name(self):
        """
        Returns the name of the Cloudshell model
        :return:
        """
        return 'VcenterVMFromLinkedClone2G'

    @property
    def vcenter_vm(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM' in self.attributes else None

    @vcenter_vm.setter
    def vcenter_vm(self, value):
        """
        vCenter VM to use in the VM creation. Should include the full path and the vm name, for example QualiFolder/VM121
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM'] = value

    @property
    def vcenter_vm_snapshot(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM Snapshot'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM Snapshot' in self.attributes else None

    @vcenter_vm_snapshot.setter
    def vcenter_vm_snapshot(self, value):
        """
        The snapshot that will be used to clone a new VM. This snapshot should be associated with the VM defined in the vCenter VM input. Should include the full path of the snapshot, for example Snapshot1/Snapshot2
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM Snapshot'] = value

    @property
    def vm_cluster(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Cluster'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Cluster' in self.attributes else None

    @vm_cluster.setter
    def vm_cluster(self, value):
        """
        The vCenter cluster or host that will be used when deploying a VM. Should be under the Default Datacenter.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Cluster'] = value

    @property
    def vm_storage(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Storage'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Storage' in self.attributes else None

    @vm_storage.setter
    def vm_storage(self, value):
        """
        The vCenter storage in which the VMs will be created. The storage can be either a datastore or a datastore cluster. For example: datastore1 (To use a specific datastore inside a cluster, specify the cluster name and the datastore name. For example: clustername/datastore1)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Storage'] = value

    @property
    def behavior_during_save(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Behavior during save'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Behavior during save' in self.attributes else None

    @behavior_during_save.setter
    def behavior_during_save(self, value='Remain Powered On'):
        """
        Determines the VM behavior when the sandbox is saved. If Power off is selected, and the VM was powered on before the save, then the VM will shut down for the duration of the save, and then be powered on at the end.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Behavior during save'] = value

    @property
    def vm_resource_pool(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Resource Pool'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Resource Pool' in self.attributes else None

    @vm_resource_pool.setter
    def vm_resource_pool(self, value):
        """
        The vCenter Resource Pool in which the VM will be created. Should be under the defined VM Cluster (optional).
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Resource Pool'] = value

    @property
    def vm_location(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Location'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Location' in self.attributes else None

    @vm_location.setter
    def vm_location(self, value):
        """
        The full path to the folder within vCenter in which the VM will be created. (e.g vms/quali)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.VM Location'] = value

    @property
    def auto_power_on(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Auto Power On'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Auto Power On' in self.attributes else None

    @auto_power_on.setter
    def auto_power_on(self, value=True):
        """
        Enables the automatic power on of an app following its deployment during reservation Setup.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Auto Power On'] = value

    @property
    def auto_power_off(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Auto Power Off'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Auto Power Off' in self.attributes else None

    @auto_power_off.setter
    def auto_power_off(self, value=True):
        """
        Enables the automatic power off of an app during reservation Teardown.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Auto Power Off'] = value

    @property
    def wait_for_ip(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Wait for IP'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Wait for IP' in self.attributes else None

    @wait_for_ip.setter
    def wait_for_ip(self, value=True):
        """
        If set to False the deployment will not wait for the VM to get an IP.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Wait for IP'] = value

    @property
    def auto_delete(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Auto Delete'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Auto Delete' in self.attributes else None

    @auto_delete.setter
    def auto_delete(self, value=True):
        """
        Enables automatic deletion of an app during reservation Teardown.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Auto Delete'] = value

    @property
    def autoload(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Autoload'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Autoload' in self.attributes else None

    @autoload.setter
    def autoload(self, value=True):
        """
        Enables the automatic execution of the Autoload command during reservation Setup.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Autoload'] = value

    @property
    def ip_regex(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.IP Regex'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.IP Regex' in self.attributes else None

    @ip_regex.setter
    def ip_regex(self, value):
        """
        Filters the IP that can be selected as an App's address.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.IP Regex'] = value

    @property
    def refresh_ip_timeout(self):
        """
        :rtype: float
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Refresh IP Timeout'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Refresh IP Timeout' in self.attributes else None

    @refresh_ip_timeout.setter
    def refresh_ip_timeout(self, value='600'):
        """
        Timeout for waiting when obtaining IP address (in seconds)
        :type value: float
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Refresh IP Timeout'] = value

    @property
    def customization_spec(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Customization Spec'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Customization Spec' in self.attributes else None

    @customization_spec.setter
    def customization_spec(self, value):
        """
        (Only applies to Windows and Linux VMs) Name of the vSphere VM customization specification to apply on the deployed VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Customization Spec'] = value

    @property
    def hostname(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Hostname'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Hostname' in self.attributes else None

    @hostname.setter
    def hostname(self, value):
        """
        (Only applies to Windows and Linux VMs) The hostname to set on the VM. If Customization Spec is specified, the value specified in the Hostname parameter will be used. Note: If Customization Spec is not specified, a new one will be created for the VM. For Windows VMs, make sure to specify a password in the App resource page
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Hostname'] = value

    @property
    def private_ip(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Private IP'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Private IP' in self.attributes else None

    @private_ip.setter
    def private_ip(self, value=''):
        """
        (Only applies to Windows and Linux VMs) The private static IP to set on the first vNIC of the VM. If Customization Spec is specified, the value specified in the Private IP parameter will be used. Note: If Customization Spec is not specified, a new one will be created for the VM. For Windows VMs, make sure to specify a password in the App resource page
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.Private IP'] = value

    @property
    def cpu(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.CPU'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.CPU' in self.attributes else None

    @cpu.setter
    def cpu(self, value):
        """
        The number of CPUs to be configured on the VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.CPU'] = value

    @property
    def ram(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.RAM'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.RAM' in self.attributes else None

    @ram.setter
    def ram(self, value):
        """
        The amount of RAM (GB) to be configured on the VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.RAM'] = value

    @property
    def hdd(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.HDD'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.HDD' in self.attributes else None

    @hdd.setter
    def hdd(self, value):
        """
        Allows to add/edit hard disk size by their number on the VM. The syntax is comma-separated disk pairs Hard Disk Label: Disk Size (GB). Example: 'Hard Disk 1:100;Hard Disk 2:200'. Shortened format is also valid: '1:100;2:200'
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.HDD'] = value

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        
        :type value: str
        """
        self._name = value

    @property
    def cloudshell_model_name(self):
        """
        :rtype: str
        """
        return self._cloudshell_model_name

    @cloudshell_model_name.setter
    def cloudshell_model_name(self, value):
        """
        
        :type value: str
        """
        self._cloudshell_model_name = value


class VcenterVMFromImage2G(object):
    def __init__(self, name):
        """
        
        """
        self.attributes = {}
        self.resources = {}
        self._cloudshell_model_name = 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G'
        self._name = name

    def add_sub_resource(self, relative_path, sub_resource):
        self.resources[relative_path] = sub_resource

    @classmethod
    def create_from_context(cls, context):
        """
        Creates an instance of NXOS by given context
        :param context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :type context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :return:
        :rtype VcenterVMFromImage2G
        """
        result = VcenterVMFromImage2G(name=context.resource.name)
        for attr in context.resource.attributes:
            result.attributes[attr] = context.resource.attributes[attr]
        return result

    def create_autoload_details(self, relative_path=''):
        """
        :param relative_path:
        :type relative_path: str
        :return
        """
        resources = [AutoLoadResource(model=self.resources[r].cloudshell_model_name,
            name=self.resources[r].name,
            relative_address=self._get_relative_path(r, relative_path))
            for r in self.resources]
        attributes = [AutoLoadAttribute(relative_path, a, self.attributes[a]) for a in self.attributes]
        autoload_details = AutoLoadDetails(resources, attributes)
        for r in self.resources:
            curr_path = relative_path + '/' + r if relative_path else r
            curr_auto_load_details = self.resources[r].create_autoload_details(curr_path)
            autoload_details = self._merge_autoload_details(autoload_details, curr_auto_load_details)
        return autoload_details

    def _get_relative_path(self, child_path, parent_path):
        """
        Combines relative path
        :param child_path: Path of a model within it parent model, i.e 1
        :type child_path: str
        :param parent_path: Full path of parent model, i.e 1/1. Might be empty for root model
        :type parent_path: str
        :return: Combined path
        :rtype str
        """
        return parent_path + '/' + child_path if parent_path else child_path

    @staticmethod
    def _merge_autoload_details(autoload_details1, autoload_details2):
        """
        Merges two instances of AutoLoadDetails into the first one
        :param autoload_details1:
        :type autoload_details1: AutoLoadDetails
        :param autoload_details2:
        :type autoload_details2: AutoLoadDetails
        :return:
        :rtype AutoLoadDetails
        """
        for attribute in autoload_details2.attributes:
            autoload_details1.attributes.append(attribute)
        for resource in autoload_details2.resources:
            autoload_details1.resources.append(resource)
        return autoload_details1

    @property
    def cloudshell_model_name(self):
        """
        Returns the name of the Cloudshell model
        :return:
        """
        return 'VcenterVMFromImage2G'

    @property
    def vcenter_image(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.vCenter Image'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.vCenter Image' in self.attributes else None

    @vcenter_image.setter
    def vcenter_image(self, value):
        """
        The full path to the image file. Note that the path should be accessible to the Execution Servers.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.vCenter Image'] = value

    @property
    def vcenter_image_arguments(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.vCenter Image Arguments'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.vCenter Image Arguments' in self.attributes else None

    @vcenter_image_arguments.setter
    def vcenter_image_arguments(self, value):
        """
        Customized properties of the image separated by comma ( , ). Example for OVF: --allowExtraConfig, --prop:Hostname=ASAvtest, --prop:HARole=Standalone, --prop:SSHEnable=True, --prop:DHCP=True, --net:Management0-0=Office LAN 41, --net:GigabitEthernet0-0=VLAN access 101
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.vCenter Image Arguments'] = value

    @property
    def default_datacenter(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Default Datacenter'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Default Datacenter' in self.attributes else None

    @default_datacenter.setter
    def default_datacenter(self, value):
        """
        The datacenter within the vCenter that will be used for VM deployment. All other settings of this vCenter resource should refer to entities associated with this datacenter.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Default Datacenter'] = value

    @property
    def vm_cluster(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Cluster'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Cluster' in self.attributes else None

    @vm_cluster.setter
    def vm_cluster(self, value):
        """
        The vCenter cluster or host that will be used when deploying a VM. Should be under the Default Datacenter.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Cluster'] = value

    @property
    def vm_storage(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Storage'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Storage' in self.attributes else None

    @vm_storage.setter
    def vm_storage(self, value):
        """
        The vCenter storage in which the VMs will be created. The storage can be either a datastore or a datastore cluster. For example: datastore1 (To use a specific datastore inside a cluster, specify the cluster name and the datastore name. For example: clustername/datastore1)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Storage'] = value

    @property
    def behavior_during_save(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Behavior during save'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Behavior during save' in self.attributes else None

    @behavior_during_save.setter
    def behavior_during_save(self, value='Remain Powered On'):
        """
        Determines the VM behavior when the sandbox is saved. If Power off is selected, and the VM was powered on before the save, then the VM will shut down for the duration of the save, and then be powered on at the end.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Behavior during save'] = value

    @property
    def vm_resource_pool(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Resource Pool'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Resource Pool' in self.attributes else None

    @vm_resource_pool.setter
    def vm_resource_pool(self, value):
        """
        The vCenter Resource Pool in which the VM will be created. Should be under the defined VM Cluster (optional).
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Resource Pool'] = value

    @property
    def vm_location(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Location'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Location' in self.attributes else None

    @vm_location.setter
    def vm_location(self, value):
        """
        The full path to the folder within vCenter in which the VM will be created. (e.g vms/quali)
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.VM Location'] = value

    @property
    def auto_power_on(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Auto Power On'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Auto Power On' in self.attributes else None

    @auto_power_on.setter
    def auto_power_on(self, value=True):
        """
        Enables the automatic power on of an app following its deployment during reservation Setup.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Auto Power On'] = value

    @property
    def auto_power_off(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Auto Power Off'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Auto Power Off' in self.attributes else None

    @auto_power_off.setter
    def auto_power_off(self, value=True):
        """
        Enables the automatic power off of an app during reservation Teardown.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Auto Power Off'] = value

    @property
    def wait_for_ip(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Wait for IP'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Wait for IP' in self.attributes else None

    @wait_for_ip.setter
    def wait_for_ip(self, value=True):
        """
        If set to False the deployment will not wait for the VM to get an IP.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Wait for IP'] = value

    @property
    def auto_delete(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Auto Delete'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Auto Delete' in self.attributes else None

    @auto_delete.setter
    def auto_delete(self, value=True):
        """
        Enables automatic deletion of an app during reservation Teardown.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Auto Delete'] = value

    @property
    def autoload(self):
        """
        :rtype: bool
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Autoload'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Autoload' in self.attributes else None

    @autoload.setter
    def autoload(self, value=True):
        """
        Enables the automatic execution of the Autoload command during reservation Setup.
        :type value: bool
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Autoload'] = value

    @property
    def ip_regex(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.IP Regex'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.IP Regex' in self.attributes else None

    @ip_regex.setter
    def ip_regex(self, value):
        """
        Filters the IP that can be selected as an App's address.
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.IP Regex'] = value

    @property
    def refresh_ip_timeout(self):
        """
        :rtype: float
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Refresh IP Timeout'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Refresh IP Timeout' in self.attributes else None

    @refresh_ip_timeout.setter
    def refresh_ip_timeout(self, value='600'):
        """
        Timeout for waiting when obtaining IP address (in seconds)
        :type value: float
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Refresh IP Timeout'] = value

    @property
    def cpu(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.CPU'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.CPU' in self.attributes else None

    @cpu.setter
    def cpu(self, value):
        """
        The number of CPUs to be configured on the VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.CPU'] = value

    @property
    def ram(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.RAM'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.RAM' in self.attributes else None

    @ram.setter
    def ram(self, value):
        """
        The amount of RAM (GB) to be configured on the VM
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.RAM'] = value

    @property
    def hdd(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.HDD'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.HDD' in self.attributes else None

    @hdd.setter
    def hdd(self, value):
        """
        Allows to add/edit hard disk size by their number on the VM. The syntax is comma-separated disk pairs Hard Disk Label: Disk Size (GB). Example: 'Hard Disk 1:100;Hard Disk 2:200'. Shortened format is also valid: '1:100;2:200'
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.HDD'] = value

    @property
    def private_ip(self):
        """
        :rtype: str
        """
        return self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Private IP'] if 'VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Private IP' in self.attributes else None

    @private_ip.setter
    def private_ip(self, value=''):
        """
        Custom private IPs to be allocated to the VM's vNICs. IPs must be within the Subnet range. For example, "10.0.0.2,10.0.0.3-4;10.0.1.2,10.0.1.5,10.0.1.9."
        :type value: str
        """
        self.attributes['VMware vCenter Cloud Provider 2G.vCenter VM From Image 2G.Private IP'] = value

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        
        :type value: str
        """
        self._name = value

    @property
    def cloudshell_model_name(self):
        """
        :rtype: str
        """
        return self._cloudshell_model_name

    @cloudshell_model_name.setter
    def cloudshell_model_name(self, value):
        """
        
        :type value: str
        """
        self._cloudshell_model_name = value



