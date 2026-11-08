"""Serialize explicit vector geometry as portable, canonical SVG documents."""
from xml.etree import ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ELEMENTS = {"svg", "title", "desc", "g", "path", "rect"}


def clean(content):
    """Keep vector geometry, flatten empty groups and emit one namespace."""
    def rebuild(node):
        tag = node.tag.split("}")[-1]
        assert tag in ELEMENTS, f"Unexpected SVG element: {tag}"
        attributes = dict(sorted(node.attrib.items()))
        assert not any(
            key.endswith("href") or key.startswith(("on", "{"))
            or key in ("class", "style", "data-name")
            for key in attributes
        ), "SVG masters must use explicit geometry and presentation attributes"
        result = ET.Element(f"{{{SVG_NS}}}{tag}", attributes)
        if tag in ("title", "desc"):
            result.text = node.text
        for child in node:
            child = rebuild(child)
            if child.tag == f"{{{SVG_NS}}}g" and not child.attrib:
                result.extend(list(child))
            else:
                result.append(child)
        return result

    result = ET.tostring(rebuild(ET.fromstring(content)), encoding="unicode") + "\n"
    assert result.count("xmlns=") == 1
    return result
