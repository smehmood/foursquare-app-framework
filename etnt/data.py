from config import CONFIG
import logging

class ChainData(object):
  def __init__(self, filename):
    self.chains_by_name = {}
    self.chains_by_id = {}
    self.all_names = []
    self.readDataFromFile(filename)

  def processRow(self, message, url, chain_id, names):
    entry = (message, url)
    self.all_names += names
    for name in names:
      self.chains_by_name[name] = entry
    if chain_id:
      self.chains_by_id[chain_id] = entry

  def readDataFromFile(self, filename):
    with open(filename, "r") as f:
      for line in f:
        row = line.strip().split("\t")
        # We must have a message, URL, the (optional) chain ID field at least one name.
        assert len(row) >= 4
        (message, url) = row[:2]
        chain_id_str = row[2]
        try:
          chain_id = long(chain_id_str)
        except ValueError:
          chain_id = None
        names = row[3:]
        self.processRow(message, url, chain_id, names)

# We want this available globally. App Engine will calculate this once, on start-up, then
# cache it for all future requests.
CHAIN_DATA = ChainData(CONFIG["etnt_data_file"])

logging.debug("No. of names: {}, No. named chains {}, No. id'd chains {}".format(
  len(CHAIN_DATA.all_names),
  len(CHAIN_DATA.chains_by_name),
  len(CHAIN_DATA.chains_by_id)
))
