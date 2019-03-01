import logging
import os

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_exceptions import CloudError

import azure.functions as func


def main(msg: func.QueueMessage) -> None:
    """
    Queue から VM 名を取り出し、スタートさせる Queue トリガ関数
    """

    # VM を操作するための認証情報をアプリケーション設定から取り出す。
    client_id = os.environ['CLIENT_ID']
    client_secret =os.environ['CLIENT_SECRET']
    tenant_id = os.environ['TENANT_ID']
    subscription_id = os.environ['SUBSCRIPTION_ID']

    # 対象となる VM 名とリソースグループ名
    resource_group_name = os.environ['RESOURCE_GROUP_NAME']
    vm_name = msg.get_body().decode('utf-8')

    logging.info('client id: %s', client_id)
    logging.info('client secret: %s', client_secret)
    logging.info('tenant id: %s', tenant_id)
    logging.info('subscription id: %s', subscription_id)
    logging.info('resource group name: %s', resource_group_name)
    logging.info('vm name: %s', vm_name)

    try:
        credentials = ServicePrincipalCredentials(
            client_id=client_id,
            secret=client_secret,
            tenant=tenant_id)

        compute_client = ComputeManagementClient(credentials, subscription_id)
        iv = compute_client.virtual_machines.instance_view(resource_group_name, vm_name)

        for status in iv.statuses:
            logging.info(status.code)
    
        dic = unfold_statuses(iv.statuses)
        power_state = dic['PowerState']
        provisioning_state = dic['ProvisioningState']

        logging.info('Power State: %s', power_state)
        logging.info('Provisioning State: %s', provisioning_state)

        # VM の状態にあわせて必要なら VM の Start をリクエストする。
        # https://docs.microsoft.com/ja-jp/azure/virtual-machines/linux/states-lifecycle
        if not power_state:
            if provisioning_state == 'updating':
                async_vm_start = compute_client.virtual_machines.start(resource_group_name, vm_name)
                # async_vm_start.wait()
                logging.info('vm start request was sent...')
            else:
                # warning でもするか？
                pass
        elif power_state == 'starting' or power_state == 'running':
            # 起動中または実行中だから Start 指示する必要はない。
            pass
        else:
            async_vm_start = compute_client.virtual_machines.start(resource_group_name, vm_name)
            # async_vm_start.wait()
            logging.info('vm start request was sent...')

    except CloudError as ce:
        logging.error(ce, exc_info=True)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise



def unfold_statuses(status_list):
    dic = {'ProvisioningState': None, 'PowerState': None}
    for status in status_list:
        name, value = status.code.split('/')
        if name == 'ProvisioningState':
            dic['ProvisioningState'] = value
        elif name == 'PowerState':
            dic['PowerState'] = value
    
    return dic




