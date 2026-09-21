"""Convert classroom LaTeX to editable Office Math (no TeX executable needed)."""
import re
from lxml import etree
from latex2mathml.converter import convert
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def element(name, *children):
    node = OxmlElement("m:" + name)
    for child in children:
        if child.tag == "group":
            node.extend(list(child))
        else:
            node.append(child)
    return node


def prop(name, value):
    node = element(name)
    node.set(qn("m:val"), str(value))
    return node


def run(text, plain=False):
    if "\\" in text:
        raise ValueError(f"Unsupported LaTeX command: {text}")
    node = element("r")
    if plain:
        node.append(element("rPr", prop("sty", "p")))
    value = element("t")
    value.set(qn("xml:space"), "preserve")
    value.text = text
    node.append(value)
    return node


def contents(source):
    return [convert_node(child) for child in source]


def convert_node(source):
    tag = etree.QName(source).localname
    children = list(source)
    if tag in ("mi", "mn", "mo", "mtext", "ms"):
        return run(source.text or "", tag in ("mtext", "ms"))
    if tag in ("math", "mrow", "mstyle", "mpadded"):
        # Stretch surrounding delimiters with tall fractions and matrices.
        if len(children) >= 3 and children[0].text in ("(", "[", "{") and children[-1].text in (")", "]", "}"):
            return element("d", element("dPr", prop("begChr", children[0].text), prop("endChr", children[-1].text)),
                           element("e", *[convert_node(c) for c in children[1:-1]]))
        group = etree.Element("group")
        for child in contents(source):
            if child.tag == "group":
                group.extend(list(child))
            else:
                group.append(child)
        return group
    if tag == "mfrac":
        return element("f", element("num", convert_node(children[0])), element("den", convert_node(children[1])))
    if tag in ("msup", "msub", "msubsup"):
        name = {"msup": "sSup", "msub": "sSub", "msubsup": "sSubSup"}[tag]
        node = element(name, element("e", convert_node(children[0])))
        if tag in ("msub", "msubsup"):
            node.append(element("sub", convert_node(children[1])))
        if tag in ("msup", "msubsup"):
            node.append(element("sup", convert_node(children[-1])))
        return node
    if tag in ("msqrt", "mroot"):
        degree = element("deg") if tag == "msqrt" else element("deg", convert_node(children[1]))
        body = contents(source) if tag == "msqrt" else [convert_node(children[0])]
        return element("rad", element("radPr", prop("degHide", int(tag == "msqrt"))), degree, element("e", *body))
    if tag == "mtable":
        matrix = element("m")
        for row in children:
            matrix.append(element("mr", *[element("e", *contents(cell)) for cell in row]))
        return matrix
    if tag == "mfenced":
        return element("d", element("dPr", prop("begChr", source.get("open", "(")), prop("endChr", source.get("close", ")"))),
                       *[element("e", convert_node(c)) for c in children])
    if tag in ("mover", "munder"):
        if tag == "mover" and children[1].text in ("→", "^", "ˆ", "¯", "˙", "¨", "~", "˜"):
            return element("acc", element("accPr", prop("chr", children[1].text)), element("e", convert_node(children[0])))
        return element("limUpp" if tag == "mover" else "limLow", element("e", convert_node(children[0])), element("lim", convert_node(children[1])))
    if tag == "munderover":
        return element("limUpp", element("e", element("limLow", element("e", convert_node(children[0])), element("lim", convert_node(children[1])))), element("lim", convert_node(children[2])))
    if tag == "mspace":
        if source.get("linebreak"):
            raise ValueError("Use an aligned/gathered environment for multiline equations")
        return run(" ", True)
    if tag == "menclose" and source.get("notation") == "box":
        return element("borderBox", element("e", *contents(source)))
    raise ValueError(f"Unsupported math structure: {tag}")


def office_math(latex):
    # latex2mathml's array support supplies a proper table for aligned equations.
    def array(match):
        body = match.group(2)
        columns = max((row.count("&") + 1 for row in re.split(r"\\\\", body)), default=1)
        return r"\begin{array}{" + "r" + "l" * (columns - 1) + "}" + body + r"\end{array}"
    latex = re.sub(r"\\begin\{(aligned|align\*?|gathered|gather\*?|equation\*?)\}(.*?)\\end\{\1\}", array, latex, flags=re.S)
    try:
        root = etree.fromstring(convert(latex).encode())
        result = element("oMath")
        for child in root:
            converted = convert_node(child)
            if converted.tag == "group":
                result.extend(list(converted))
            else:
                result.append(converted)
        return result
    except Exception as exc:
        raise ValueError(f"Cannot render worksheet equation {latex!r}: {exc}") from exc
