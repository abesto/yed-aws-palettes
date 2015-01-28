import sys
import xml.etree.ElementTree as ET

ns = '{http://graphml.graphdrawing.org/xmlns}'
filepath = sys.argv[1]
labels = [l.strip() for l in sys.stdin.readlines()]

print "Will mutate file \"%s\"" % filepath

tree = ET.parse(filepath)
nodes = tree.findall('.//%sgraph/%snode' % (ns, ns))
if len(nodes) != len(labels):
    print "Error: number of nodes (%d) != (%d) number of labels from STDIN" % (len(nodes), len(labels))
    sys.exit(1)

tooltip_keys = tree.findall(".//%skey[@attr.name='Palette ToolTip']" % ns)
tooltip_ids = [el.get('id') for el in tooltip_keys]
print "Palette ToolTip keys: %s" % ', '.join(tooltip_ids)

for node, label in zip(nodes, labels):
    node_id = node.get('id')
    for tooltip_id in tooltip_ids:
        tooltip_node = node.find(".//%sdata[@key='%s']" % (ns, tooltip_id))
        if tooltip_node is not None:
            tooltip_node.text = label
            print '%s: data %s set to %s' % (node_id, tooltip_id, label)

tree.write(filepath)
