import xml.etree.ElementTree as ET

og_subs = input("drag the file: ").strip()


tree = ET.parse(og_subs)

root = tree.getroot()

line_position = 1
for p in root.iter("{http://www.w3.org/ns/ttml}p"):
    begin_tc = p.get("begin")
    end_tc = p.get("end")
    dialogue = p.text

    print(line_position, end_tc, dialogue)

    line_position+=1




