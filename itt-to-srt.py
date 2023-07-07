import xml.etree.ElementTree as ET




def extract_content(captions, output):
    line_position = 1
    new_line = None
    for p in captions.iter():

        if p.tag == "{http://www.w3.org/ns/ttml}p":
            if new_line != None:
                save_to_srt(new_line, output)
                line_position+=1
                new_line = None

            begin_tc = p.get("begin")
            end_tc = p.get("end")
            dialogue = p.text

            new_line = f"\n{line_position}\n{begin_tc} --> {end_tc}\n{dialogue}\n"
        
            # print(line_position, end_tc, dialogue)
    
        elif p.tag == "{http://www.w3.org/ns/ttml}br":
            new_line = new_line + p.tail + '\n'
        
        else:
            print(p.tag)
    
    if new_line != None:
        save_to_srt(new_line, output)
        return




def save_to_srt(line, output):

    # Write each line to an output file:
    with open(output, 'a') as f:
        f.write(line)
        f.close()



if __name__ == '__main__':
    # og_subs = input("drag the file: ").strip()
    og_subs = '/Users/albertorodriguez/Desktop/peer_review/chapters_titles/cc.itt'
    tree = ET.parse(og_subs)
    root = tree.getroot()
    output_file = f"{og_subs.removesuffix('.itt')}_applehit-fhfix.srt"

    extract_content(root, output_file)
