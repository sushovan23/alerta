
import os
import datetime
import json

from uuid import uuid4

from alerta.alert import severity
from alerta.common import log as logging

_DEFAULT_TIMEOUT = 3600  # default number of seconds before alert is EXPIRED

LOG = logging.getLogger(__name__)


class Alert(object):

    def __init__(self, resource, event, correlate=list(), group='Misc', value=None,
                 severity=severity.NORMAL, environment=list('PROD'), service=list(),
                 text=None, event_type='exceptionAlert', tags=list(), origin=None,
                 threshold_info=None, summary=None, timeout=_DEFAULT_TIMEOUT):

        # FIXME(nsatterl): how to fix __program__ for origin???
        __program__ = 'THIS IS BROKEN'

        self.alertid = str(uuid4())
        self.origin = origin or '%s/%s' % (__program__, os.uname()[1])
        self.summary = summary or '%s - %s %s is %s on %s %s' % (','.join(environment), severity, event,
                                                     value, ','.join(service), resource)
        self.header = {
            'type': event_type,
            'correlation-id': self.alertid,
        }

        self.alert = {
            'id': self.alertid,
            'resource': resource,
            'event': event,
            'correlatedEvents': correlate,
            'group': group,
            'value': value,
            'severity': severity,
            'environment': environment,
            'service': service,
            'text': text,
            'type': event_type,
            'tags': tags,
            'summary': summary,
            'createTime': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z',
            'origin': origin,
            'thresholdInfo': threshold_info,
            'timeout': timeout,
        }

    def __repr__(self):
        return self.header, self.alert

    def __str__(self):
        return json.dumps(self.alert, indent=4)

    def get_id(self):
        return self.alertid

    def get_header(self):
        return json.dumps(self.header, indent=4)

    def get_body(self):
        return json.dumps(self.alert, indent=4)


class Heartbeat(object):

    def __init__(self, origin=None, version='unknown'):

        # FIXME(nsatterl): how to fix __program__ for origin???
        __program__ = 'THIS IS BROKEN'

        self.heartbeatid = str(uuid4())
        self.origin = origin or '%s/%s' % (__program__, os.uname()[1])

        self.header = {
            'type': 'heartbeat',
            'correlation-id': self.heartbeatid,
        }

        self.heartbeat = {
            'id': self.heartbeatid,
            'type': 'heartbeat',
            'createTime': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z',
            'origin': origin,
            'version': version,
        }

    def __repr__(self):
        return self.header, self.heartbeat

    def __str__(self):
        return json.dumps(self.heartbeat, indent=4)

    def get_id(self):
        return self.heartbeatid

    def get_header(self):
        LOG.debug(json.dumps(self.header, indent=4))
        return json.dumps(self.header, indent=4)

    def get_body(self):
        return json.dumps(self.heartbeat, indent=4)

