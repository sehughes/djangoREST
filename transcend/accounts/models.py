from __future__ import unicode_literals
from django.db import models
from django.contrib import auth
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

import logging

class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)


class AgilePartNumber(models.Model):
    part_num = models.CharField(max_length=15)
    part_type = models.CharField(max_length=10)

class Cm(models.Model):
    code = models.CharField(max_length=4, unique=True)
    ip_space = models.GenericIPAddressField(max_length=15, unique=True)
    netmask = models.GenericIPAddressField(max_length=15)
    gateway_ip = models.GenericIPAddressField(protocol='ipv4')
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'cm'

    def __unicode__(self):
        return "%s" % (self.code)


class Cpus(models.Model):
    cpu_model = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, default='Qualified')
    allowed_modes = models.ManyToManyField('Modes')
    appliance_models = models.ManyToManyField('Models')
    cpu_log = GenericRelation('ComponentLog', related_query_name='cpus')

    # agile_part_num = models.ForeignKey(AgilePartNumber)

    class Meta:
        db_table = 'cpus'

    def __unicode__(self):
        return "%s" % (self.cpu_model)


#
# class CpuApplianceMapping(models.Model):
#     cpu_model = models.ForeignKey(Cpus)
#     appliance_models = models.ManyToManyField('Models')
#     component_vendor = models.ForeignKey('ComponentVendors', null=True,
#                                          blank=True)
#
#     class Meta:
#         db_table = 'cpu_appliance_mapping'


class ComponentVendors(models.Model):
    vendor_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'component_vendors'


class ComponentProductCode(models.Model):
    product_code = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'component_product_code'


class ComponentLog(models.Model):
    result = models.ForeignKey('Results', on_delete=models.CASCADE)
    identifier = models.CharField(max_length=100, default=None)

    # Below the mandatory fields for generic relation
    # https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'component_log'


class ComponentLogError(models.Model):
    result = models.ForeignKey('Results',on_delete=models.CASCADE)
    kind = models.CharField(max_length=10)
    model = models.CharField(max_length=50)
    identifier = models.CharField(max_length=100,default=None)
    location = models.CharField(max_length=100)
    firmware = models.CharField(max_length=50,default=None)
    error = models.CharField(max_length=50)

    class Meta:
        db_table = 'component_log_error'

class Dimms(models.Model):
    dimm_model = models.CharField(max_length=50, unique=True)
    dimm_size = models.CharField(max_length=10)
    status = models.CharField(max_length=50, default='Qualified')
    appliance_models = models.ManyToManyField('Models',
                                              through='DimmAppliance')
    allowed_modes = models.ManyToManyField('Modes')
    # agile_part_num = models.ForeignKey(AgilePartNumber)

    class Meta:
        db_table = 'dimms'

    def __unicode__(self):
        return "%s" % (self.dimm_model)


class DimmAppliance(models.Model):
    dimm_model = models.ForeignKey('Dimms', on_delete=models.CASCADE)
    appliance = models.ForeignKey('Models', default=1, on_delete=models.CASCADE)
    component_vendor = models.ForeignKey(ComponentVendors, null=True,
                                         blank=True, on_delete=models.CASCADE)
    locator = models.CharField(max_length=20, null=True, blank=True)
    bank_locator = models.CharField(max_length=30, null=True, blank=True)
    asset_tag = models.CharField(max_length=10, null=True, blank=True)
    dimm_log = GenericRelation('ComponentLog', related_query_name='dimms')

    class Meta:
        db_table = 'dimm_appliance'

class DriveModels(models.Model):
    drive_name = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50, default='Qualified')
    drive_size_in_GB = models.IntegerField()
    component_vendor = models.ForeignKey(ComponentVendors, null=True,
                                         blank=True, on_delete=models.CASCADE)
    component_product_code = models.ForeignKey(ComponentProductCode,
                                               null=True, blank=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    appliance_models = models.ManyToManyField('Models',
                                              through='DriveAppliance')
    allowed_modes = models.ManyToManyField('Modes')

    # agile_part_num = models.ForeignKey(AgilePartNumber)

    class Meta:
        db_table = 'drive_models'


class DriveFirmwares(models.Model):
    drive_firmware = models.CharField(max_length=30)
    drive_firmware_binary = models.CharField(max_length=50, blank=True,
                                             null=True)
    drive_model = models.ForeignKey(DriveModels, on_delete=models.CASCADE)
    is_upgradable = models.BooleanField(default=False)
    fw_upgrade_method = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'drive_firmwares'
        unique_together = ("drive_firmware", "drive_model")


class SmartAttributes(models.Model):
    smart_attribute = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'smart_attributes'


class DriveSmartMapping(models.Model):
    drive_model = models.ForeignKey(DriveModels, on_delete=models.CASCADE)
    smart_attribute = models.ForeignKey(SmartAttributes, on_delete=models.CASCADE)
    threshold = models.IntegerField()

    class Meta:
        db_table = 'drive_smart_mapping'


# class DriveApplianceMapping(models.Model):
#     drive_model = models.ForeignKey(DriveModels)
#     appliance_models = models.ManyToManyField('Models')
#     allowed_modes = models.ManyToManyField('Modes')
#
#     class Meta:
#         db_table = 'drive_appliance_mapping'


class DriveSlots(models.Model):
    drive_slot = models.CharField(max_length=10)

    class Meta:
        db_table = 'drive_slots'

    def __unicode__(self):
        return "%s" % (self.drive_slot)


class DriveAppliance(models.Model):
    drive = models.ForeignKey(DriveModels, on_delete=models.CASCADE)
    appliance = models.ForeignKey('Models', on_delete=models.CASCADE)
    allowed_slots = models.ManyToManyField(DriveSlots)

    class Meta:
        db_table = 'drive_appliance'


class Modes(models.Model):
    mode = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'modes'

    def __unicode__(self):
        return "%s" % (self.mode)


class ModelAttributes(models.Model):
    model_attribute = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'model_attributes'

    def __unicode__(self):
        return "%s" % self.model_attribute


class ModelAttributesMapping(models.Model):
    model = models.ForeignKey('Models', on_delete=models.CASCADE)
    model_attribute = models.ForeignKey(ModelAttributes, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'model_attributes_mapping'


class Models(models.Model):
    CHOICES = ((1, 'enable'), (0, 'disable'))
    model = models.CharField(max_length=15, unique=True)
    state = models.BooleanField(choices=CHOICES, default=True)

    # state = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'models'

    def get_slots_for_model(self):
        logger = logging.getLogger(__name__)
        slots = []
        n_slots = self.modelattributesmapping_set.filter(
            model_attribute__model_attribute='drive_count')

        if n_slots:
            # logger.debug("No. of Slots %s "
            #              % n_slots[0].value)
            slots = [str(i) for i in range(int(n_slots[0].value))]
        else:
            return 0

        has_flash = self.modelattributesmapping_set.filter(
            model_attribute__model_attribute='has_flash')
        if has_flash and has_flash[0].value == '1':
            slots.append('flash')

        # logger.debug("Slots: %s" % slots)
        return slots

    def __unicode__(self):
        return "%s" % self.model


class OnBoardFirmwares(models.Model):
    category = models.CharField(max_length=10)
    model = models.ForeignKey(Models, on_delete=models.CASCADE)
    version = models.CharField(max_length=10, blank=True, null=True)
    required = models.BooleanField()


class ParentChildTestsAssoc(models.Model):
    parent = models.ForeignKey('ParentTests', blank=True, null=True, on_delete=models.CASCADE)
    test = models.ForeignKey('Tests', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'testfarm_parent_child_tests_assoc'


class ParentTests(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'testfarm_parent_tests'

    def __unicode__(self):
        return "%s" % (self.description)


class ResourceAttributes(models.Model):
    resource_attribute = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'resource_attributes'

    def __unicode__(self):
        return "%s" % self.resource_attribute


class ResourceAttributesMapping(models.Model):
    resource = models.OneToOneField('Resources', on_delete=models.CASCADE)
    resource_attribute = models.ForeignKey(ResourceAttributes, on_delete=models.CASCADE)
    value = models.CharField(max_length=20)

    class Meta:
        db_table = 'resource_attributes_mapping'


class Resources(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=50, blank=True, null=True)
    cm = models.ForeignKey(Cm, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'resources'

    def __unicode__(self):
        return "%s" % (self.name)


class Results(models.Model):
    uut = models.ForeignKey('Uut', blank=True, null=True, on_delete=models.CASCADE)
    supervisor = models.ForeignKey('Resources', related_name='supervisor', on_delete=models.CASCADE)
    station = models.ForeignKey('Resources', related_name='station', on_delete=models.CASCADE)
    model = models.ForeignKey(Models, on_delete=models.CASCADE)
    cm_serial = models.CharField(max_length=20)
    rvbd_serial = models.CharField(max_length=20)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    outcome = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, blank=True, null=True)
    test = models.ForeignKey('Tests', on_delete=models.CASCADE)
    workflow = models.ForeignKey('TestWorkflow', blank=True, null=True, on_delete=models.CASCADE)
    test_case = models.ManyToManyField('TestCase', through='TestCaseResult',
                                       blank=True)
    log_dir = models.CharField(max_length=50, blank=True, null=True)
    updated_time = models.DateTimeField()
    user = models.ForeignKey('Users', blank=True, null=True, on_delete=models.CASCADE)
    mfg_sw_version = models.CharField(max_length=60, blank=True, null=True,
                                        default=None)

    class Meta:
        db_table = 'results'


class Sku(models.Model):
    sku = models.CharField(max_length=50)
    parent_sku = models.ForeignKey('self', related_name='base_sku',
                                   blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sku'

    def __unicode__(self):
        return "%s" % self.sku


# class SkuData(models.Model):
#     sku = models.CharField(max_length=20, blank=True, null=True)
#     base_SKU = models.CharField(max_length=20, blank=True, null=True)
#     model = models.CharField(max_length=20, blank=True, null=True)
#     mclass = models.CharField(max_length=20, blank=True, null=True)
#     netcfg = models.CharField(max_length=20, blank=True, null=True)
#     preconfig = models.CharField(max_length=20, blank=True, null=True)
#     serial_prefix = models.CharField(max_length=20, blank=True, null=True)
#     sku_attribute = models.CharField(max_length=20, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'sku'


class SkuAttributes(models.Model):
    sku_attribute = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'sku_attributes'

    def __unicode__(self):
        return "%s" % self.sku_attribute


class SkuAttributesMapping(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE)
    sku_attribute = models.ForeignKey(SkuAttributes, on_delete=models.CASCADE)
    value = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'sku_attributes_mapping'


class TestCase(models.Model):
    test_case = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'test_case'

    def __unicode__(self):
        return "%s" % (self.test_case)


class TestCaseResult(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    result = models.ForeignKey(Results, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    outcome = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'testcase_result'


class TestSuite(models.Model):
    test_suite = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'test_suite'

    def __unicode__(self):
        return "%s" % (self.test_suite)


class TestWorkflow(models.Model):
    test_workflow = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'test_workflow'

    def __unicode__(self):
        return "%s" % (self.test_workflow)


class Tests(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE)
    # parameters = JSONField()
    mode = models.ForeignKey(Modes, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tests'


class Users(models.Model):
    operator_id = models.CharField(max_length=50, blank=True, null=True,
                                   unique=True)
    fullname = models.CharField(max_length=50, blank=True, null=True,
                                unique=True)
    password = models.CharField(max_length=12, blank=True, null=True,
                                unique=True)
    cm = models.ForeignKey(Cm, blank=True, null=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, blank=True, null=True, unique=True)

    class Meta:
        db_table = 'user'

    def __unicode__(self):
        return "%s" % (self.fullname)


class Macs(models.Model):
    data = models.CharField(max_length=50, blank=True, null=True,
                                   unique=True)
    # data = JSONField()

    class Meta:
        db_table = 'macs'


class Uut(models.Model):
    cm_serial = models.CharField(max_length=20, blank=True, null=True)
    rvbd_serial = models.CharField(max_length=20, blank=True, null=True)
    station = models.ForeignKey(Resources, blank=True, null=True, on_delete=models.CASCADE)
    sku = models.ForeignKey(Sku, blank=True, null=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, blank=True, default='active')
    cm = models.ForeignKey(Cm, blank=True, null=True, on_delete=models.CASCADE)
    model = models.ForeignKey(Models, blank=True, null=True, on_delete=models.CASCADE)
    mac = models.ForeignKey(Macs, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'testfarm_uut'


class WorkflowTestAssoc(models.Model):
    workflow = models.ForeignKey(TestWorkflow, blank=True, null=True, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, blank=True, null=True, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'workflow_test_assoc'


class WorkflowTestSuiteAssoc(models.Model):
    workflow = models.ForeignKey(TestWorkflow, blank=True, null=True, on_delete=models.CASCADE)
    test_suite = models.ForeignKey(TestSuite, blank=True, null=True, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'workflow_test_suite_assoc'


class Interfaces(models.Model):
    resource = models.ForeignKey(Resources, on_delete=models.CASCADE)
    device = models.CharField(max_length=25)
    wired_to = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    ip_addr = models.GenericIPAddressField(max_length=60, blank=True, null=True)
    netmask = models.GenericIPAddressField(max_length=40, blank=True,
                                           null=True)
    gateway = models.GenericIPAddressField(max_length=60, blank=True, null=True)
    mac = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'interfaces'
