import xml.etree.ElementTree as ET
from timecode_class import Timecode_Parser




def extract_content(captions, output):
    line_position = 1
    new_line = None
    fps = None
    for p in captions.iter():

        if p.tag == "{http://www.w3.org/ns/ttml}p":
            if new_line != None:
                save_to_srt(new_line, output)
                line_position+=1
                new_line = None

            begin_tc = p.get("begin")
            end_tc = p.get("end")
            dialogue = p.text


            begin, end = convert_timecodes(begin_tc, end_tc, fps)

            new_line = f"\n{line_position}\n{begin.timecode} --> {end.timecode}\n{dialogue}\n"
            
    
        elif p.tag == "{http://www.w3.org/ns/ttml}br":
            new_line = new_line + p.tail + '\n'
        
        elif p.tag == "{http://www.w3.org/ns/ttml}tt":
            # Process "tt" elements
            frame_rate = p.get("{http://www.w3.org/ns/ttml#parameter}frameRate")
            multiplier = p.get("{http://www.w3.org/ns/ttml#parameter}frameRateMultiplier")
            # print(frame_rate, multiplier)
            fps = get_the_framerate(frame_rate, multiplier)
            print(fps)
        else:
            # print(p.tag)
            continue
    
    if new_line != None:
        save_to_srt(new_line, output)
        return



def get_the_framerate(frame_rate, multiplier):
    a, b = multiplier.split(" ")
    return round(int(frame_rate) * (int(a)/int(b)), 3)


def save_to_srt(line, output):

    # Write each line to an output file:
    with open(output, 'a') as f:
        f.write(line)
        f.close()


def convert_timecodes(begin_tc, end_tc, fps):
    begin = Timecode_Parser(begin_tc, fps)
    end = Timecode_Parser(end_tc, fps)
    return (begin, end)


if __name__ == '__main__':
    og_subs = input("drag the file: ").strip()
    tree = ET.parse(og_subs)
    root = tree.getroot()
    output_file = f"{og_subs.removesuffix('.itt')}_applehit-fhfix.srt"

    extract_content(root, output_file)
