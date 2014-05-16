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

import random

import anx
import matplotlib
import networkx

_author__ = 'Petter Bjelland (petter.bjelland@gmail.com)'


class Pyanx(networkx.DiGraph):
  def __init__(self):
    super(Pyanx, self).__init__()
    self.node_id = 0
    self.positions = {}
    self.entity_types = {}

  def add_node(self, entity_type='Anon', label=None):
    current_id = 'n' + str(self.node_id)

    if entity_type not in self.entity_types:
      self.entity_types[entity_type] = True

    self.node_id += 1

    super(Pyanx, self).add_node(current_id, 
        dict(entity_type=entity_type, label=label))

    return current_id

  def add_edge(self, n0, n1, label=''):
    super(Pyanx, self).add_edge(n0, n1, dict(label=label))

  def layout(self, layout, iterations, space=75):
    layout_func = getattr(networkx, layout)

    scale = len(self.nodes()) * space

    positions = layout_func(self, scale=scale, iterations=iterations)

    for pos in positions:
      self.positions[pos] = {
        'x': str(int(positions[pos][0])),
        'y': str(int(positions[pos][1]))
      }

  def __add_entity_types(self, chart):
    entity_type_collection = anx.EntityTypeCollection()

    for entity_type in self.entity_types:
      entity_type_collection.add_EntityType(
          anx.EntityType(Name=entity_type, IconFile=entity_type))

    chart.add_EntityTypeCollection(entity_type_collection)

  def __add_link_types(self, chart):
    link_type_collection = anx.LinkTypeCollection()

    link_type_collection.add_LinkType(anx.LinkType(Name="Link"))

    chart.add_LinkTypeCollection(link_type_collection)

  def __add_entities(self, chart):
    chart_item_collection = anx.ChartItemCollection()

    for node in self.nodes(data=True):
      node_id, data = node

      icon = anx.Icon(IconStyle=anx.IconStyle(Type=data['entity_type']))
      entity = anx.Entity(Icon=icon, EntityId=node_id, Identity=data['label'])
      end = anx.End(
          X=self.positions[node_id]['x'],
          Y=self.positions[node_id]['y'],
          Entity=entity)
      chart_item = anx.ChartItem(
          XPosition=self.positions[node_id]['x'],
          Label=data['label'],
          End=end)

      chart_item_collection.add_ChartItem(chart_item)

    chart.add_ChartItemCollection(chart_item_collection)

  def __add_links(self, chart):
    chart_item_collection = anx.ChartItemCollection()

    for edge in self.edges(data=True):
      source, sink, data = edge

      link_style = anx.LinkStyle(Type='Link', ArrowStyle='ArrowOnHead')
      link = anx.Link(End1Id=source, End2Id=sink, LinkStyle=link_style)
      chart_item = anx.ChartItem(Label=data['label'], Link=link)

      chart_item_collection.add_ChartItem(chart_item)

    chart.add_ChartItemCollection(chart_item_collection)

  def create(self, path, layout='spring_layout', pretty=True, iterations=50):
    self.layout(layout, iterations)

    chart = anx.Chart(IdReferenceLinking=False)
    self.__add_entity_types(chart)
    self.__add_link_types(chart)
    self.__add_entities(chart)
    self.__add_links(chart)

    with open(path, 'w') as output_file:
      chart.export(output_file, 0, pretty_print=pretty,
          namespacedef_=None)
