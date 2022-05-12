import requests
from requests.exceptions import HTTPError
import json
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class EhvaApi:
    """ EHVA API class. performs requests to the EHVA REST server """

    API_URL = "api/v1"

    def __init__(self, host_url, api_key):

        self.host_url = host_url
        self.base_url = urllib.parse.urljoin(host_url, self.API_URL)
        self.api_key = api_key
        self.request_headers = {"ApiKey" : self.api_key}

    def __repr__(self):
        return f"EhvaApi hosted on {self.host_url}"
    

    def request_wrapper(func):
        """ This is a wrapper to perform the requests and assess their success """
        def f(*args, **kwargs):
            try:
                response = func(*args, **kwargs)

                if response.ok:
                    return response.json()
                else:
                    return f"{response.reason}: {response.text}"

            except Exception as ex:
                raise ConnectionError(ex)
        return f


    @request_wrapper
    def _perform_get(self, route, params=None):
        return requests.get(self.base_url + route, params=params, headers=self.request_headers, verify=False)


    @request_wrapper
    def _perform_post(self, route, params=None, data=None):
        return requests.post(self.base_url + route, params=params, headers=self.request_headers, data=data, verify=False)


    @property
    def wafers(self):
        """ Returns a list of all wafers """
        return self._perform_get("/components/wafers")

    @property
    def reticles(self):
        """ Returns a list of all reticles """
        return self._perform_get("/components/reticles")

    @property
    def dies(self):
        """ Returns a list of all dies """
        return self._perform_get("/components/dies")

    @property
    def circuits(self):
        """ Returns a list of all circuits """
        return self._perform_get("/components/circuits")

    @property
    def optical_ports(self):
        """ Returns a list of all optical ports """
        return self._perform_get("/components/opticalports")

    @property
    def electrical_ports(self):
        """ Returns a list of all electrical ports """
        return self._perform_get("/components/electricalports")

    @property
    def station_configurations(self):
        """ Returns a list of all station configs """
        return self._perform_get("/stationconfigurations")

    @property
    def measurement_sequences(self):
        """ Returns a list of all measurement sequences """
        return self._perform_get("/measurementsequences")



    def run_sequence(self, sequence_name, sequence_version, station_config : dict = None, dut : dict = None, debug_mode = False, nosave_mode = False):
        """ Run an existing Measurement Sequence
        
        Args:
            sequence_name (str): Name of the Sequence to be run
            sequence_version (str): Version of the sequence to be run
            station_config (dict, optional): The Station Config to be used. Must be a dict with string fields 'name' and 'version'.
            dut (dict, optional): Device Under Test to be used. Must be a dict containing fields 'wafer', 'reticle', 'die', 'circuit', 'optical port', 'electrical port'.
            debug_mode (bool, optional): Whether to run in debug (slowed-down) mode.
            nosave_mode (bool, optional): Whether to prevent saving to database. Useful for testing and debugging.

        Returns:
            dict: A dictionary containing all Sequence Variables in the form (Name, Value).
        """

        # Verify Measurement Sequence
        matching_sequence = [s for s in self.measurement_sequences if s['name'] == sequence_name and s['version'] == sequence_version]
        if not matching_sequence:
            raise ValueError(f"The Measurement Sequence with name '{sequence_name}' and version '{sequence_version}' could not be found.")
        sequence_id = matching_sequence[0]['id']

        # Make Station config verifications
        config_id = None
        if station_config is not None:
            if not all(key in station_config.keys() for key in ['name', 'version']):
                raise ValueError("argument station_config must contain 'name' and 'version' fields.")

            config = [c for c in self.station_configurations if c['name'] == station_config['name'] and c['version'] == station_config['version']]
            if not config:
                raise ValueError(f"Station Config with name '{station_config['name']}' and version '{station_config['version']}' was not found.")
            config_id = config[0]['id']        


        # Make DUT verifications
        optical_port_id = None 
        electrical_port_id = None
        if dut is not None and (dut['optical port'] is not None or dut['electrical port'] is not None):

            if not all(key in ['wafer', 'reticle', 'die', 'circuit', 'optical port', 'electrical port'] for key in dut.keys()):
                raise ValueError("argument 'dut' must contain the following fields: 'wafer', 'reticle', 'die', 'circuit', 'optical port', 'electrical port'.")

            try:
                wafer = [w for w in self.wafers if w['name'] == dut['wafer']][0]
                reticle = [r for r in self.reticles if r['name'] == dut['reticle'] and r['waferId'] == wafer['id']][0]
                die = [d for d in self.dies if d['name'] == dut['die'] and d['reticleId'] == reticle['id']][0]
                circuit = [c for c in self.circuits if c['name'] == dut['circuit'] and c['dieId'] == die['id']][0]
                optical_port_id = [p['id'] for p in self.optical_ports if p['name'] == dut['optical port'] and p['componentId'] == circuit['id']]
                electrical_port_id = [p['id'] for p in self.electrical_ports if p['name'] == dut['electrical port'] and p['componentId'] == circuit['id']]

            except Exception:
                raise ValueError(f"The provided DUT could not be found, please review hierarchy: {dut}.")
            

        # Perform request
        params = {
                    'sequenceId' : sequence_id,
        'stationConfigurationId' : config_id,
                'opticalPortsId' : optical_port_id,
             'electricalPortsId' : electrical_port_id,
                   'isDebugMode' : debug_mode,
                  'isNoSaveMode' : nosave_mode
                  }

        result = self._perform_get("/runtime/runexisting", params=params)

        return result







