import os
#
#----------------------------------------------- Get Initial Data
# Open https://datastore.iatistandard.org/
# Do an advanced search, filter down to a starting subset (add Recipient Country Code maybe?)
# Download Activity XML, save as "activities.xml"
#
#
#

import iatikit.process.base_task
import iatikit.process.worker
import iatikit.process.tasks.add_geonames_information

#------------------------------- Add Geoname Information
#
def add_geoname_info():
    worker = iatikit.process.worker.ProcessXMLWorker(
        tasks=  [
            iatikit.process.tasks.add_geonames_information.AddGeonameInformationProcessXMLTask(
                geoname_username=os.getenv("GEONAMES_USERNAME")
            )
        ]
    )
    worker.process_file_and_write_result("activities.xml", "activities-more-info.xml")

add_geoname_info()
