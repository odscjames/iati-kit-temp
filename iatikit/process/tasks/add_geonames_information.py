from lxml import etree
import os
import json
import requests
import time

import iatikit.process.base_task

class AddGeonameInformationProcessXMLTask(iatikit.process.base_task.ProcessXMLTask):

    def __init__(self, geonames_cache_dir_name=".geonames_cache", sleep=15, geoname_username="demo"):
        self._geonames_cache_dir_name = geonames_cache_dir_name
        self._sleep = sleep
        self._geoname_username = geoname_username

    def process(self, activity_xml):
        locations = activity_xml.xpath("location")
        for location in locations:

            admins =  location.xpath("administrative")
            for admin in admins:

                vocab = admin.attrib.get("vocabulary", "")
                if vocab == "G1":
                    code = admin.attrib.get("code", "")
                    if code:
                        data = self.get_geoname_id(code)
                        if data.get("lat") and data.get("lng"):
                            lat = data.get("lat")
                            lng = data.get("lng")
                            point_element = etree.Element("point")
                            point_element.attrib["source"] = "From Geonames (Locality G1) lookup for feature " + code
                            point_element.attrib["srsName"] = "http://www.opengis.net/def/crs/EPSG/0/4326"
                            pos_element = etree.Element("pos")
                            pos_element.text = str(lat) + " " + str(lng)
                            point_element.insert(0, pos_element)
                            location.insert(1000000, point_element)

    def get_geoname_id(self, geoname_id):
        os.makedirs(self._geonames_cache_dir_name, exist_ok=True)
        cache_file = os.path.join(self._geonames_cache_dir_name, geoname_id + ".json" )
        # In cache?
        if os.path.exists(cache_file):
            with open(cache_file) as fp:
                return json.load(fp)
        # make request
        print("GETTING " + str(geoname_id))
        url = 'http://api.geonames.org/getJSON?username={username}&id={id}'.format(username=self._geoname_username, id=geoname_id)
        r = requests.get(url)
        # sort out data
        out_data = {"status":{"http_status_code": r.status_code}} if  r.status_code != 200 else r.json()
        # Cache
        with open(cache_file, "w") as fp:
            json.dump(out_data, fp)
        # Sleep
        time.sleep(self._sleep)
        # Return
        return out_data


