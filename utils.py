import json
import argparse
# 可用
def escape_for_xml(text):
    """
    将文本中的：
     - XML 特殊字符 转义为标准实体（如 & → &amp;）
     - 中文字符 转义为 XML 数字字符引用格式（如 ERP系统 → ERP&#31995;&#32479;）
     - 其他字符保持不变
    """
    if not isinstance(text, str):
        text = str(text)

    result = []
    for char in text:
        if char == '&':
            result.append('&amp;')
        elif char == '<':
            result.append('<')
        elif char == '>':
            result.append('>')
        elif char == '"':
            result.append('&quot;')
        elif char == "'":
            result.append('&apos;')
        elif '\u4e00' <= char <= '\u9fff':
            result.append(f'&#{ord(char)};')
        else:
            result.append(char)
    return ''.join(result)

def json_to_xml(json_data):
    class_to_level = {
        "知识领域": "一级",
        "知识单元": "二级",
        "知识点": "归纳级",
        "关键知识细节": "内容级"
    }

    xml = "<KG>\n\t" + escape_for_xml("教学知识图谱") + "\n\t<entities>\n"

    for entity in json_data['entities']:
        level = class_to_level.get(entity['class'], "归纳级")
        xml += f"\t\t<entity>\n"
        xml += f"\t\t\t<id>{str(entity['id'])}</id>\n"
        xml += f"\t\t\t<class_name>{escape_for_xml(entity['class'])}</class_name>\n"
        xml += f"\t\t\t<classification>{escape_for_xml('内容方法型节点')}</classification>\n"
        xml += f"\t\t\t<identity>{escape_for_xml('知识')}</identity>\n"
        xml += f"\t\t\t<level>{escape_for_xml(level)}</level>\n"
        xml += f"\t\t\t<attach>{str(entity['attach'])}</attach>\n"
        xml += f"\t\t\t<opentool>{escape_for_xml('无')}</opentool>\n"
        xml += f"\t\t\t<content>{escape_for_xml(entity['content'])}</content>\n"
        xml += f"\t\t\t<x>0.0</x>\n"
        xml += f"\t\t\t<y>0.0</y>\n"
        xml += f"\t\t</entity>\n"

    xml += "\t</entities>\n\t<relations>\n"

    for relation in json_data['relations']:
        rel_type = relation['type']
        xml += f"\t\t<relation>\n"
        xml += f"\t\t\t<name>{escape_for_xml(rel_type)}</name>\n"
        xml += f"\t\t\t<headnodeid>{str(relation['head'])}</headnodeid>\n"
        xml += f"\t\t\t<tailnodeid>{str(relation['tail'])}</tailnodeid>\n"

        class_name = "包含关系" if rel_type == "包含" else "次序：次序关系"
        classification = "包含关系" if rel_type == "包含" else "次序关系"

        xml += f"\t\t\t<class_name>{escape_for_xml(class_name)}</class_name>\n"
        xml += f"\t\t\t<mask>{escape_for_xml('知识连线')}</mask>\n"
        xml += f"\t\t\t<classification>{escape_for_xml(classification)}</classification>\n"
        xml += f"\t\t\t<head_need>{escape_for_xml('内容方法型节点')}</head_need>\n"
        xml += f"\t\t\t<tail_need>{escape_for_xml('内容方法型节点')}</tail_need>\n"
        xml += f"\t\t</relation>\n"

    xml += "\t</relations>\n</KG>"
    return xml

def main():
    parser = argparse.ArgumentParser(description='Convert JSON to XML for knowledge graph')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('-o', '--output_file', type=str, default=None, help='Path to the output XML file')
    args = parser.parse_args()

    print(f"[INFO] 输入文件路径: {args.input_file}")

    with open(args.input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    xml_output = json_to_xml(json_data)
    out_path = args.output_file if args.output_file else args.input_file.replace('.json', '.xml')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml_output)
    print(f"[INFO] XML 文件已保存至: {out_path}")

if __name__ == "__main__":
    main()