#!/usr/bin/python
# -*- coding: utf-8 -*-

from hashlib import sha1
from uuid import uuid4
from requests import Session


class ProxyListException(Exception):
    pass


class ProxyList:
    def __init__(self, client_type='se0306',
                 client_key='7502E43F3381C82E571733A350099BB5D449DD48311839C099ADC4631BA0CC04'):
        self._device_id = ''
        self._device_id_hash = ''
        self._device_password = ''

        self._client_type = client_type
        self._client_key = client_key

        self._session = Session()

    def __calc_sha1(self, data):
        return sha1(str(data).encode('ascii')).hexdigest().upper()

    def __http_request(self, url, data):
        headers = {
            'SE-Client-Type': self._client_type,
            'SE-Client-API-Key': self._client_key
        }

        result = self._session.post('https://api.surfeasy.com%s' % url, data,
                                    headers=headers).json()

        code = list(result['return_code'].keys())[0]
        if code != '0':
            raise ProxyListException('ERROR: %s' % result['return_code'][code])
        else:
            return result

    def __register_subscriber(self):
        email = '%s@mailinator.com' % uuid4()
        password = self.__calc_sha1(uuid4())

        data = {
            'email': email,
            'password': password
        }
        self.__http_request('/v2/register_subscriber', data)

    def __register_device(self):
        data = {
            'client_type': self._client_type,
            'device_hash': '4BE7D6F1BD040DE45A371FD831167BC108554111',
            'device_name': 'Opera-Browser-Client'
        }

        result = self.__http_request('/v2/register_device', data)
        self._device_id = result['data']['device_id']
        self._device_id_hash = self.__calc_sha1(self._device_id)
        self._device_password = result['data']['device_password']

    def __enum_geo(self):
        data = {'device_id': self._device_id_hash}
        result = self.__http_request('/v2/geo_list', data)

        for geo in result['data']['geos']:
            yield geo['country_code']

    def __enum_hosts(self, country_code):
        data = {
            'serial_no': self._device_id_hash,
            'requested_geo': '"%s"' % country_code
        }
        result = self.__http_request('/v2/discover', data)

        for ip in result['data']['ips']:
            for port in ip['ports']:
                yield {
                    'ip': ip['ip'],
                    'port': port,
                    'country': ip['geo']['country_code'],
                    'state_code': ip['geo']['state_code']
                }

    def get_proxies(self):
        self.__register_subscriber()
        self.__register_device()

        hosts = []
        for country_code in self.__enum_geo():
            for host in self.__enum_hosts(country_code):
                hosts.append(host)

        return {
            'username': self._device_id_hash,
            'password': self._device_password,
            'hosts': hosts
        }
