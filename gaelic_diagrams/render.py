# gaelic_diagrams.render

# pygraphviz
import pygraphviz


class DiagramRenderer():
	def __init__(self, filename):
		self.graph = pygraphviz.AGraph(filename)

	def highlight_node(self, nodename):
		node = self.graph.get_node(nodename)
		node.attr['style'] = 'filled, bold'
		node.attr['fillcolor'] = 'grey80'

	def highlight_edge(self, nodeA, nodeB):
		edge = self.graph.get_edge(nodeA, nodeB)
		edge.attr['style'] = 'bold'

	def write(self, filename):
		if filename.endswith('.dot'):
			self.graph.write(filename)
		else:
			self.graph.layout(prog='dot')
			self.graph.draw(filename)
