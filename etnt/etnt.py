import difflib
import logging
import re
import urllib

from config import CONFIG
from data import CHAIN_DATA
from abstract_app import AbstractApp


class EatThisNotThat(AbstractApp):
  def checkinTaskQueue(self, client, checkin_json):
    venue_name = checkin_json['venue']['name']
    name_list = difflib.get_close_matches(venue_name, CHAIN_DATA.all_names, 1, 0.85)
    logging.debug(
        "Venue name {} produced name_list {}"
        .format(venue_name, str(name_list))
    )
    if not name_list:
      return  # This venue is not in Eat This, Not That!
    canonical_name = name_list[0]
    entry = CHAIN_DATA.chains_by_name.get(canonical_name)
    if entry is None:
      logging.error(
          "Venue name {} matched canonical name {} but wasn't found in CHAIN_DATA"
          .format(venue_name, canonical_name)
      )
      return
    (text, url) = entry

    params = { 'text' : text,
               'url' : url }
    logging.debug('%s local params: %s' % (checkin_json['id'], params))
    if not CONFIG['local_dev']:
      client.checkins.reply(checkin_json['id'], params)
