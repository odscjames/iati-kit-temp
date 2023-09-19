from lxml import etree
import os
import json
import requests
import time

class ProcessXMLWorker:

    def __init__(self, tasks=[]):
        self.tasks = tasks

    def process_file(self, in_filename):
        context = etree.iterparse(in_filename, tag='iati-activity', huge_tree=True)
        for _, activity in context:
            for task in self.tasks:
                task.process(activity_xml=activity)

    def process_file_and_write_result(self, in_filename, out_filename):
        # Set up data recipient
        with etree.xmlfile(out_filename, encoding='utf-8') as xf:
            xf.write_declaration() # standalone=True
            #xf.write_doctype('<!DOCTYPE root SYSTEM "some.dtd">')
            with xf.element('iati-activities', attrib={"version": "TODO"}):
                # Now process
                context = etree.iterparse(in_filename, tag='iati-activity', huge_tree=True)
                for _, activity in context:
                    for task in self.tasks:
                        task.process(activity_xml=activity)
                    xf.write(activity)
