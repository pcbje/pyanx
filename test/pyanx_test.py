#!/usr/bin/env python
"""
This work is made available under the Apache License, Version 2.0.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""

import os
import unittest

from lxml import objectify

import pyanx

__author__ = 'Petter Bjelland (petter.bjelland@gmail.com)'


class PyanxUnitTest(unittest.TestCase):
  def setUp(self):
    chart = pyanx.Pyanx()

    tyrion = chart.add_node(entity_type='Person', label='Tyrion') # n0
    tywin = chart.add_node(entity_type='Person', label='Tywin') # n1
    jaime = chart.add_node(entity_type='Person', label='Jaime') # n2
    cersei = chart.add_node(entity_type='Woman', label='Cersei') # n3

    chart.add_edge(tywin, tyrion, 'Father of')
    chart.add_edge(jaime, tyrion, 'Brother of')
    chart.add_edge(cersei, tyrion, 'Sister of')

    probe = 'test_probe.anx'

    chart.create(probe)

    self.parsed_chart = pyanx.anx.parse(probe, silence=True)

    os.remove(probe)

  def test_EntityTypes(self):
    entity_types = self.parsed_chart.get_EntityTypeCollection()[0].get_EntityType()

    self.assertEquals(2, len(entity_types))
    self.assertEquals("Person", entity_types[0].get_Name())
    self.assertEquals("Woman", entity_types[1].get_Name())

  def test_LinkTypes(self):
    link_types = self.parsed_chart.get_LinkTypeCollection()[0].get_LinkType()

    self.assertEquals(1, len(link_types))
    self.assertEquals("Link", link_types[0].get_Name())
    
  def test_ChartItemCount(self):
    chart_items = self.parsed_chart.get_ChartItemCollection()[0].get_ChartItem()

    self.assertEquals(4, len(chart_items))

  def test_ChartItemNodes(self):
    chart_items = self.parsed_chart.get_ChartItemCollection()[0].get_ChartItem()

    self.assertEquals('Tyrion', chart_items[0].get_Label())
    self.assertEquals('Person', chart_items[0].get_End().get_Entity().get_Icon().get_IconStyle().get_Type())

    self.assertEquals('Tywin', chart_items[1].get_Label())
    self.assertEquals('Person', chart_items[1].get_End().get_Entity().get_Icon().get_IconStyle().get_Type())

    self.assertEquals('Jaime', chart_items[2].get_Label())
    self.assertEquals('Person', chart_items[2].get_End().get_Entity().get_Icon().get_IconStyle().get_Type())

    self.assertEquals('Cersei', chart_items[3].get_Label())
    self.assertEquals('Woman', chart_items[3].get_End().get_Entity().get_Icon().get_IconStyle().get_Type())

  def test_ChartItemEdges(self):
    chart_items = self.parsed_chart.get_ChartItemCollection()[1].get_ChartItem()

    self.assertEquals('Father of', chart_items[0].get_Label())
    self.assertEquals('n1', chart_items[0].get_Link().get_End1Id())
    self.assertEquals('n0', chart_items[0].get_Link().get_End2Id())

    self.assertEquals('Brother of', chart_items[1].get_Label())
    self.assertEquals('n2', chart_items[1].get_Link().get_End1Id())
    self.assertEquals('n0', chart_items[1].get_Link().get_End2Id())

    self.assertEquals('Sister of', chart_items[2].get_Label())
    self.assertEquals('n3', chart_items[2].get_Link().get_End1Id())
    self.assertEquals('n0', chart_items[2].get_Link().get_End2Id())

if __name__ == '__main__':
  unittest.main()
