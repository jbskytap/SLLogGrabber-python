#!/usr/bin/env python

"""
Copyright 2018 Skytap Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import SoftLayer
import datetime

class SLLogGrabber(object):

    def __init__(self, api_user, api_key):
        self.api_user = api_user
        self.api_key = api_key
        self.connection = SoftLayer.create_client_from_env(username=self.api_user, api_key=self.api_key)

    def _get_log_objects(self, _filter, limit=50, offset=0):
        """Pages through all results from the Event_Log. This might take long time."""
        result = []
        while True:
            events = self.connection.call('SoftLayer_Event_Log',
                                          'getAllObjects', filter=_filter, limit=limit, offset=offset)

            if isinstance(events, list):
                result = result + events

            if len(events) < limit:
                break

            offset = offset + limit

        return result


    def get_recent_logs(self, days=1):
        """ Get the full event logs for
        all current users, going back to 'days' number of days"""

        # calculate date back 'days' ago and \
        # make it the input for the get_events call
        date_object = datetime.datetime.today() - datetime.timedelta(days=days)
        start_date = date_object.strftime("%Y-%m-%dT00:00:00")

        object_filter = {
            'eventCreateDate': {
                'operation': 'greaterThanDate',
                'options': [{'name': 'date', 'value': [start_date]}]
            }
        }

        events = self._get_log_objects(_filter=object_filter)
        return events


if __name__ == '__main__':

    import os
    import logging
    api_user = os.environ['SL_USER']
    api_key = os.environ['SL_PASS']

    sl = SLLogGrabber(api_key=api_key, api_user=api_user)
    for x in range(0,10):
        # repeatedly grab logs
        logs = sl.get_recent_logs()

    print logs

