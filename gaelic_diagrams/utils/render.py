# gaelic_diagrams.utils.render

# pygraphviz
import pygraphviz


class DiagramRenderer():
    def __init__(self, filename):
        self.graph = pygraphviz.AGraph(filename)

    def add_attrs(self, element, attr_name, new_attrs):
        attrs = set(
            [attr.strip() for attr in element.attr[attr_name].split(',')]
        )
        attrs.update(
            [attr.strip() for attr in new_attrs.split(',')]
        )
        element.attr[attr_name] = ', '.join(list(attrs))

    def highlight_node(self, nodename):
        node = self.graph.get_node(nodename)
        self.add_attrs(node, 'style', 'filled, bold')
        node.attr['fillcolor'] = 'grey80'

    def highlight_edge(self, nodeA, nodeB):
        edge = self.graph.get_edge(nodeA, nodeB)
        edge.attr['style'] = 'bold'

    def highlight_path(self, nodelist):
        for index, node in enumerate(nodelist[:-1]):
            self.highlight_node(node)
            self.highlight_edge(node, nodelist[index+1])
        self.highlight_node(nodelist[-1])

    def add_example_column(self, text, rankwith):
        node = self.graph.add_node(
            self.make_node_name(text),
            label=text,
            shape='plaintext',
            fontsize=36
        )
        self.graph.add_subgraph(node, rank='same')
        self.graph.add_subgraph(
            self.graph.get_node(rankwith),
            rank='same'
        )

    def add_example_node(self, text, linkfrom):
        nodename = self.make_node_name(text)
        self.graph.add_node(
            nodename,
            label=text,
            shape='plaintext',
            fontsize=36
        )
        self.graph.add_edge(linkfrom, nodename, color='invis')

    def make_node_name(self, text):
        nodename = text.lower().replace(' ', '_')
        nodename_src = nodename
        count = 0
        while self.graph.has_node(nodename):
            count += 1
            nodename = '{name}_{count}'.format(
                name=nodename_src,
                count=count
            )
        return nodename

    def write(self, filename):
        if filename.endswith('.dot'):
            self.graph.write(filename)
        else:
            self.graph.layout(prog='dot')
            self.graph.draw(filename)
