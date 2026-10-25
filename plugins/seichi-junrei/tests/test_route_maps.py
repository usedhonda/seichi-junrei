"""Geographic input safety and timed-stop/day consistency."""
import copy
import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from route_maps import prepare

class MapContracts(unittest.TestCase):
    def test_coordinates_and_timed_stop_membership(self):
        data={'stages':[{'id':'place'}], 'route_map':{'stops':[{'id':'one','label':'Public square','lat':50.0,'lon':14.0,'stage_id':'place'}]}}
        days=[{'id':'1','label':'DAY 1','map_stop_ids':['one'],'events':[{'map_stop_id':'one'}]}]
        fragment,payload=prepare(data,days)
        self.assertIn('journey-map',fragment)
        self.assertIn('Public square',payload)
        for bad in [float('nan'),91,True,'<script>']:
            broken=copy.deepcopy(data);broken['route_map']['stops'][0]['lat']=bad
            with self.assertRaises(ValueError):prepare(broken,days)
        broken=copy.deepcopy(days);broken[0]['map_stop_ids']=[]
        with self.assertRaises(ValueError):prepare(data,broken)
