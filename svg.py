import xml.etree.ElementTree as ET
import re
import os

def convert(input_file):
    # ファイルを読み込んで内容を取得
    with open(input_file, 'r') as file:
        file_content = file.read()

    # 置換を行う
    modified_content = file_content.replace("sodipodi:cx","sodipodicx").replace("sodipodi:cy","sodipodicy").replace("sodipodi:rx","sodipodirx").replace("sodipodi:ry","sodipodiry").replace("sodipodi:start","sodipodistart").replace("sodipodi:end","sodipodiend").replace("sodipodi:arc-type","sodipodiarctype")

    # 結果を新しいファイルに保存
    with open("running.svg", 'w') as output_file:
        output_file.write(modified_content)

    print(f'"{input_file}" が置換され、結果が"running.svg"に保存されました。')


def svg_to_processing(input_file, output_file):
    # XMLファイルを読み込む
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Processingのコードを構築する.
    processing_code = "void setup(){\n  size(360,640);\n  background(#ffffff);\n  svgDraw();\n}\n  void svgDraw() {\n  colorMode( RGB );\n"
    print(processing_code)
    # 各要素を処理する.
    for elem in root.iter():
        if elem.tag in ['{http://www.w3.org/2000/svg}circle', '{http://www.w3.org/2000/svg}ellipse']:
            # 円または楕円の場合

            processing_code += drawmode(elem.attrib['style'])

            
            cx = float(elem.attrib['cx'])
            cy = float(elem.attrib['cy'])
            if elem.tag == '{http://www.w3.org/2000/svg}circle':
                r = float(elem.attrib['r'])
            else:
                rx = float(elem.attrib['rx'])
                ry = float(elem.attrib['ry'])



            if elem.tag == '{http://www.w3.org/2000/svg}circle':
                processing_code += f"  ellipse({cx}, {cy}, {r * 2}, {r * 2});\n"
                print(f"ellipse({cx}, {cy}, {r * 2}, {r * 2});\n")
            else:
                processing_code += f"  ellipse({cx}, {cy}, {rx * 2}, {ry * 2});\n"
                print(f"ellipse({cx}, {cy}, {rx * 2}, {ry * 2});\n")

        elif elem.tag == '{http://www.w3.org/2000/svg}rect':
            # 四角形の場合

            processing_code += drawmode(elem.attrib['style'])

            x = float(elem.attrib['x'])
            y = float(elem.attrib['y'])
            width = float(elem.attrib['width'])
            height = float(elem.attrib['height'])
            processing_code += f"  rect({x}, {y}, {width}, {height});\n"
            print(f"rect({x}, {y}, {width}, {height});\n")

        elif elem.tag == '{http://www.w3.org/2000/svg}path':
            # 直線,弧の場合

            processing_code += drawmode(elem.attrib['style'])

            try:
                cx = float(elem.attrib['sodipodicx'])
                cy = float(elem.attrib['sodipodicy'])
                rx = float(elem.attrib['sodipodirx'])
                ry = float(elem.attrib['sodipodiry'])
                start = float(elem.attrib['sodipodistart'])
                end = float(elem.attrib['sodipodiend']) 
                type = elem.attrib['sodipodiarctype']

                while(end < start): end += 6.2831853

                if(type == "slice"): 
                    processing_code += f"  arc({cx}, {cy}, {rx * 2}, {ry * 2},{start},{end},PIE);\n"
                    print(f"arc({cx}, {cy}, {rx * 2}, {ry * 2},{start},{end},PIE);\n")
                elif(type == "arc"): 
                    processing_code += f"  arc({cx}, {cy}, {rx * 2}, {ry * 2},{start},{end},OPEN);\n"
                    print(f"arc({cx}, {cy}, {rx * 2}, {ry * 2},{start},{end},OPEN);\n")
                elif(type == "chord"): 
                    processing_code += f"  arc({cx}, {cy}, {rx * 2}, {ry * 2},{start},{end},CHORD);\n"
                    print(f"arc({cx}, {cy}, {rx * 2}, {ry * 2},{start},{end},CHORD);\n")
            except:
                d = (elem.attrib['d'])

                # 正規表現パターン
                M_pattern = re.compile(r'[Mm]')
                float_pattern = re.compile(r'[-+]?\d*\.\d+|\d+')

                # パターンにマッチする部分を取得
                M_match = M_pattern.match(d)
                float_matches = float_pattern.findall(d)

                line = [float(match) for match in float_matches]

                m_value = M_match[0]
                x1 = line[0]
                y1 = line[1]
                x2 = line[2]
                y2 = line[3]
                if( m_value == "m" ):
                    processing_code += f"  line({x1}, {y1}, {x1+x2}, {y1+y2});\n"
                    print(f"m mode line({x1}, {y1}, {x1+x2}, {y1+y2})")
                else:
                    processing_code += f"  line({x1}, {y1}, {x2}, {y2});\n"
                    print(f"M mode line({x1}, {y1}, {x2}, {y2})")


    processing_code += "}\n"

    print("}\n")

    # Processingコードをファイルに保存
    with open(output_file, 'w') as f:
        f.write(processing_code)


def drawmode(style):

    stylecode = ""

    fill_pattern = re.compile(r'fill:(#?[0-9a-fA-F]{3,6})')
    fill_opacity_pattern = re.compile(r'fill-opacity:([\d.]+)')
    stroke_pattern = re.compile(r'stroke:(#?[0-9a-fA-F]{3,6})')
    stroke_width_pattern = re.compile(r'stroke-width:([\d.]+)')
    stroke_opacity_pattern = re.compile(r'stroke-opacity:([\d.]+)')

    fill_match = fill_pattern.search(style)
    fill_opacity_match = fill_opacity_pattern.search(style)
    stroke_match = stroke_pattern.search(style)
    stroke_width_match = stroke_width_pattern.search(style)
    stroke_opacity_match = stroke_opacity_pattern.search(style)

    fill_value = fill_match.group(1) if fill_match else None
    fill_opacity_value = fill_opacity_match.group(1) if fill_opacity_match else None
    stroke_value = stroke_match.group(1) if stroke_match else None
    stroke_width_value = float(stroke_width_match.group(1)) if stroke_width_match else None
    stroke_opacity_value = stroke_opacity_match.group(1) if stroke_opacity_match else None

    if (fill_match): stylecode += f"  fill({fill_value});\n"
    if (fill_opacity_match and fill_opacity_value == "0" ): stylecode += f"  noFill();\n"
    if (stroke_match): stylecode += f"  stroke({stroke_value});\n"
    if (stroke_width_match): stylecode += f"  strokeWeight({stroke_width_value});\n"
    if (stroke_opacity_match and stroke_opacity_value == "0" ): stylecode += f"  noStroke();\n"

    print(stylecode)
    return stylecode

def main():
    svg_file = str(input("write file name without .svg\n"))
    convert("{}.svg".format(svg_file))
    svg_to_processing("running.svg","{}.pde".format(svg_file))
    os.remove("running.svg")


if __name__ == "__main__":
    main()