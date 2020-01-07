"""
Model class for MyTardis API v1's GroupResource.
"""
import urllib.parse

import requests

from ..conf import settings
from ..logs import logger


class Group:
    """
    Model class for MyTardis API v1's GroupResource.
    """

    def __init__(self, name=None, group_dict=None):
        self.group_id = None
        self.name = name
        self.group_dict = group_dict

        if group_dict is not None:
            self.group_id = group_dict["id"]
            if name is None:
                self.name = group_dict["name"]

        self.short_name = name
        length = len(settings.advanced.group_prefix)
        self.short_name = self.name[length:]

    def get_value_for_key(self, key):
        """
        Return value of field from the Group model
        to display in the Groups or Folders view
        """
        return getattr(self, key)

    @staticmethod
    def get_group_by_name(name):
        """
        Return the group record matching the supplied name

        :raises requests.exceptions.HTTPError:
        """
        url = "%s/api/v1/group/?format=json&name=%s" % (
            settings.general.mytardis_url,
            urllib.parse.quote(name.encode("utf-8")),
        )
        response = requests.get(url=url, headers=settings.default_headers)
        response.raise_for_status()
        groups_dict = response.json()
        num_groups_found = groups_dict["meta"]["total_count"]

        if num_groups_found == 0:
            return None
        logger.debug("Found group record for name '" + name + "'.")
        return Group(name=name, group_dict=groups_dict["objects"][0])
