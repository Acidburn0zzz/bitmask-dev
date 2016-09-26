# -*- coding: utf-8 -*-
# dispatcher.py
# Copyright (C) 2016 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Command dispatcher.
"""
import json

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from twisted.internet import defer
from twisted.python import failure, log

from leap.common.events import register_async as register
from leap.common.events import unregister_async as unregister
from leap.common.events import catalog

from .api import APICommand, register_method


class SubCommand(object):

    __metaclass__ = APICommand

    def dispatch(self, service, *parts, **kw):
        try:
            subcmd = parts[1]
            _method = getattr(self, 'do_' + subcmd.upper(), None)
        except IndexError:
            _method = None

        if not _method:
            raise RuntimeError('No such subcommand: ' + subcmd)
        return defer.maybeDeferred(_method, service, *parts, **kw)


class BonafideCmd(SubCommand):

    label = 'bonafide'

    def __init__(self):
        self.subcommand_user = UserCmd()
        self.subcommand_provider = ProviderCmd()

    def do_USER(self, bonafide, *parts):
        return self.subcommand_user.dispatch(bonafide, *parts[1:])

    def do_PROVIDER(self, bonafide, *parts):
        return self.subcommand_provider.dispatch(bonafide, *parts[1:])


class ProviderCmd(SubCommand):

    label = 'bonafide.provider'

    @register_method("{'domain': str, 'api_uri': str, 'api_version': str}")
    def do_CREATE(self, bonafide, *parts):
        domain = parts[2]
        return bonafide.do_provider_create(domain)

    @register_method("{'domain': str, 'api_uri': str, 'api_version': str}")
    def do_READ(self, bonafide, *parts):
        domain = parts[2]
        return bonafide.do_provider_read(domain)

    @register_method("")
    def do_DELETE(self, bonafide, *parts):
        domain = parts[2]
        bonafide.do_provider_delete(domain)

    @register_method("[{'domain': str}]")
    def do_LIST(self, bonafide, *parts):
        seeded = False
        if len(parts) > 2:
            seeded = parts[2]
        return bonafide.do_provider_list(seeded)


class UserCmd(SubCommand):

    label = 'bonafide.user'

    @register_method("{'srp_token': unicode, 'uuid': unicode}")
    def do_AUTHENTICATE(self, bonafide, *parts):
        user, password = parts[2], parts[3]
        autoconf = False
        if len(parts) > 4:
            if parts[4] == 'true':
                autoconf = True
        return bonafide.do_authenticate(user, password, autoconf)

    @register_method("{'signup': 'ok', 'user': str}")
    def do_CREATE(self, bonafide, *parts):
        user, password = parts[2], parts[3]
        autoconf = False
        if len(parts) > 4:
            if parts[4] == 'true':
                autoconf = True
        return bonafide.do_signup(user, password, autoconf)

    @register_method("{'logout': 'ok'}")
    def do_LOGOUT(self, bonafide, *parts):
        user = parts[2]
        return bonafide.do_logout(user)

    @register_method('str')
    def do_ACTIVE(self, bonafide, *parts):
        return bonafide.do_get_active_user()


class EIPCmd(SubCommand):

    label = 'eip'

    @register_method('dict')
    def do_ENABLE(self, service, *parts):
        d = service.do_enable_service(self.label)
        return d

    @register_method('dict')
    def do_DISABLE(self, service, *parts):
        d = service.do_disable_service(self.label)
        return d

    @register_method('dict')
    def do_STATUS(self, eip, *parts):
        d = eip.do_status()
        return d

    @register_method('dict')
    def do_START(self, eip, *parts):
        # TODO --- attempt to get active provider
        # TODO or catch the exception and send error
        provider = parts[2]
        d = eip.do_start(provider)
        return d

    @register_method('dict')
    def do_STOP(self, eip, *parts):
        d = eip.do_stop()
        return d


class MailCmd(SubCommand):

    label = 'mail'

    @register_method('dict')
    def do_ENABLE(self, service, *parts, **kw):
        # FIXME -- service doesn't have this method
        d = service.do_enable_service(self.label)
        return d

    @register_method('dict')
    def do_DISABLE(self, service, *parts, **kw):
        d = service.do_disable_service(self.label)
        return d

    @register_method('dict')
    def do_STATUS(self, mail, *parts, **kw):
        d = mail.do_status()
        return d

    @register_method('dict')
    def do_GET_TOKEN(self, mail, *parts, **kw):
        d = mail.get_token()
        return d

    @register_method('dict')
    def do_GET_SMTP_CERTIFICATE(self, mail, *parts, **kw):
        # TODO move to mail service
        # TODO should ask for confirmation? like --force or something,
        # if we already have a valid one. or better just refuse if cert
        # exists.
        # TODO how should we pass the userid??
        # - Keep an 'active' user in bonafide (last authenticated)
        # (doing it now)
        # - Get active user from Mail Service (maybe preferred?)
        # - Have a command/method to set 'active' user.

        @defer.inlineCallbacks
        def save_cert(cert_data):
            userid, cert_str = cert_data
            cert_path = yield mail.do_get_smtp_cert_path(userid)
            with open(cert_path, 'w') as outf:
                outf.write(cert_str)
            defer.returnValue('certificate saved to %s' % cert_path)

        bonafide = kw['bonafide']
        d = bonafide.do_get_smtp_cert()
        d.addCallback(save_cert)
        return d


class WebUICmd(SubCommand):

    label = 'web'

    @register_method('dict')
    def do_ENABLE(self, service, *parts, **kw):
        d = service.do_enable_service(self.label)
        return d

    @register_method('dict')
    def do_DISABLE(self, service, *parts, **kw):
        d = service.do_disable_service(self.label)
        return d

    @register_method('dict')
    def do_STATUS(self, webui, *parts, **kw):
        print 'webui', webui
        d = webui.do_status()
        return d


class KeysCmd(SubCommand):

    label = 'keys'

    @register_method("[dict]")
    def do_LIST(self, service, *parts, **kw):
        private = False
        if parts[-1] == 'private':
            private = True

        bonafide = kw['bonafide']
        d = bonafide.do_get_active_user()
        d.addCallback(service.do_list_keys, private)
        return d

    @register_method('dict')
    def do_EXPORT(self, service, *parts, **kw):
        if len(parts) < 3:
            return defer.fail("An email address is needed")
        address = parts[2]

        private = False
        if parts[-1] == 'private':
            private = True

        bonafide = kw['bonafide']
        d = bonafide.do_get_active_user()
        d.addCallback(service.do_export, address, private)
        return d

    @register_method('dict')
    def do_INSERT(self, service, *parts, **kw):
        if len(parts) < 5:
            return defer.fail("An email address is needed")
        address = parts[2]
        validation = parts[3]
        rawkey = parts[4]

        bonafide = kw['bonafide']
        d = bonafide.do_get_active_user()
        d.addCallback(service.do_insert, address, rawkey, validation)
        return d

    @register_method('str')
    def do_DELETE(self, service, *parts, **kw):
        if len(parts) < 3:
            return defer.fail("An email address is needed")
        address = parts[2]

        private = False
        if parts[-1] == 'private':
            private = True

        bonafide = kw['bonafide']
        d = bonafide.do_get_active_user()
        d.addCallback(service.do_delete, address, private)
        return d


class EventsCmd(SubCommand):

    label = 'events'

    def __init__(self):
        self.queue = Queue()
        self.waiting = []

    @register_method("")
    def do_REGISTER(self, _, *parts, **kw):
        event = getattr(catalog, parts[2])
        register(event, self._callback)

    @register_method("")
    def do_UNREGISTER(self, _, *parts, **kw):
        event = getattr(catalog, parts[2])
        unregister(event)

    @register_method("(str, [])")
    def do_POLL(self, _, *parts, **kw):
        if not self.queue.empty():
            return self.queue.get()

        d = defer.Deferred()
        self.waiting.append(d)
        return d

    @register_method("")
    def _callback(self, event, *content):
        payload = (str(event), content)
        if not self.waiting:
            self.queue.put(payload)
            return

        while self.waiting:
            d = self.waiting.pop()
            d.callback(payload)


class CommandDispatcher(object):

    __metaclass__ = APICommand

    label = 'core'

    def __init__(self, core):

        self.core = core
        self.subcommand_bonafide = BonafideCmd()
        self.subcommand_eip = EIPCmd()
        self.subcommand_mail = MailCmd()
        self.subcommand_keys = KeysCmd()
        self.subcommand_events = EventsCmd()
        self.subcommand_webui = WebUICmd()

    # XXX --------------------------------------------
    # TODO move general services to another subclass

    @register_method("{'mem_usage': str}")
    def do_STATS(self, *parts):
        return _format_result(self.core.do_stats())

    @register_method("{version_core': '0.0.0'}")
    def do_VERSION(self, *parts):
        return _format_result(self.core.do_version())

    @register_method("{'mail': 'running'}")
    def do_STATUS(self, *parts):
        return _format_result(self.core.do_status())

    @register_method("{'stop': 'ok'}")
    def do_STOP(self, *parts):
        return _format_result(self.core.do_stop())

    # -----------------------------------------------

    def do_BONAFIDE(self, *parts):
        bonafide = self._get_service('bonafide')
        d = self.subcommand_bonafide.dispatch(bonafide, *parts)
        d.addCallbacks(_format_result, _format_error)
        return d

    def do_EIP(self, *parts):
        eip = self._get_service(self.subcommand_eip.label)
        if not eip:
            return _format_result({'eip': 'disabled'})
        subcmd = parts[1]

        dispatch = self._subcommand_eip.dispatch
        if subcmd in ('enable', 'disable'):
            d = dispatch(self.core, *parts)
        else:
            d = dispatch(eip, *parts)

        d.addCallbacks(_format_result, _format_error)
        return d

    def do_MAIL(self, *parts):
        subcmd = parts[1]
        dispatch = self.subcommand_mail.dispatch

        if subcmd == 'enable':
            d = dispatch(self.core, *parts)

        mail = self._get_service(self.subcommand_mail.label)
        bonafide = self._get_service('bonafide')
        kw = {'bonafide': bonafide}

        if not mail:
            return _format_result({'mail': 'disabled'})

        if subcmd == 'disable':
            d = dispatch(self.core)
        elif subcmd != 'enable':
            d = dispatch(mail, *parts, **kw)

        d.addCallbacks(_format_result, _format_error)
        return d

    def do_WEBUI(self, *parts):
        subcmd = parts[1]
        dispatch = self.subcommand_webui.dispatch

        if subcmd == 'enable':
            d = dispatch(self.core, *parts)

        webui_label = 'web'
        webui = self._get_service(webui_label)
        kw = {}

        if not webui:
            return _format_result({'webui': 'disabled'})
        if subcmd == 'disable':
            d = dispatch(self.core, *parts)
        elif subcmd != 'enable':
            d = dispatch(webui, *parts, **kw)

        d.addCallbacks(_format_result, _format_error)
        return d

    def do_KEYS(self, *parts):
        dispatch = self.subcommand_keys.dispatch

        keymanager_label = 'keymanager'
        keymanager = self._get_service(keymanager_label)
        bonafide = self._get_service('bonafide')
        kw = {'bonafide': bonafide}

        if not keymanager:
            return _format_result('keymanager: disabled')

        d = dispatch(keymanager, *parts, **kw)
        d.addCallbacks(_format_result, _format_error)
        return d

    def do_EVENTS(self, *parts):
        dispatch = self.subcommand_events.dispatch
        d = dispatch(None, *parts)
        d.addCallbacks(_format_result, _format_error)
        return d

    def dispatch(self, msg):
        cmd = msg[0]

        _method = getattr(self, 'do_' + cmd.upper(), None)

        if not _method:
            return defer.fail(failure.Failure(RuntimeError('No such command')))

        return defer.maybeDeferred(_method, *msg)

    def _get_service(self, name):
        try:
            return self.core.getServiceNamed(name)
        except KeyError:
            return None


def _format_result(result):
    return json.dumps({'error': None, 'result': result})


def _format_error(failure):
    log.err(failure)
    return json.dumps({'error': failure.value.message, 'result': None})
