#!/usr/bin/python
# -*- coding: utf-8 -*-

from proxy_list import ProxyList
from base64 import b64encode
from random import choice
from httplib import HTTPSConnection
from ssl import _create_unverified_context


class ProxyRequest:
    def __init__(self):
        self._proxy_lit = ProxyList()
        self._proxies = None

    def __get_new_proxies(self):
        self._proxies = self._proxy_lit.get_proxies()

    def get_auth_token(self):
        if self._proxies is None:
            self.__get_new_proxies()

        assert 'username' in self._proxies
        assert 'password' in self._proxies

        return b64encode(self._proxies['username'] + ':' + self._proxies['password'])

    def __get_random_proxy(self):
        if self._proxies is None:
            self.__get_new_proxies()

        assert 'hosts' in self._proxies

        result = choice(self._proxies['hosts'])

        assert 'ip' in result
        assert 'port' in result

        return result['ip'] + ':' + str(result['port'])

    def http_get(self, url):
        connection = HTTPSConnection(self.__get_random_proxy(),
                                     context=_create_unverified_context())
        connection.request(method='GET', url=url,
                           headers={'Proxy-Authorization': 'Basic ' + self.get_auth_token()})

        response = connection.getresponse()

        return {'status': response.status,
                'reason': response.reason,
                'data': response.read()}
