import json

def json_to_xml(json_data):
    # 创建XML头部
    xml = "<KG>\n\t教学知识图谱\n\t<entities>\n"
    
    # 映射关系：class到level
    class_to_level = {
        "知识领域": "一级",
        "知识单元": "二级",
        "知识点": "归纳级",
        "关键知识细节": "内容级"
    }
    
    # 添加实体节点
    for entity in json_data['entities']:
        # 根据class自动推导level
        level = class_to_level.get(entity['class'], "归纳级")  # 默认为归纳级
        
        xml += f"\t\t<entity>\n"
        xml += f"\t\t\t<id>{entity['id']}</id>\n"
        xml += f"\t\t\t<class_name>{entity['class']}</class_name>\n"
        xml += f"\t\t\t<classification>内容方法型节点</classification>\n"
        xml += f"\t\t\t<identity>知识</identity>\n"
        xml += f"\t\t\t<level>{level}</level>\n"
        xml += f"\t\t\t<attach>{entity['attach']}</attach>\n"
        xml += f"\t\t\t<opentool>无</opentool>\n"
        xml += f"\t\t\t<content>{entity['content']}</content>\n"
        xml += f"\t\t\t<x>0.0</x>\n"
        xml += f"\t\t\t<y>0.0</y>\n"
        xml += f"\t\t</entity>\n"
    
    # 添加关系
    xml += "\t</entities>\n\t<relations>\n"
    
    for relation in json_data['relations']:
        rel_type = relation['type']
        xml += f"\t\t<relation>\n"
        xml += f"\t\t\t<name>{rel_type}</name>\n"
        xml += f"\t\t\t<headnodeid>{relation['head']}</headnodeid>\n"
        xml += f"\t\t\t<tailnodeid>{relation['tail']}</tailnodeid>\n"
        
        # 设置关系类型
        class_name = "包含关系" if rel_type == "包含" else "次序：次序关系"
        classification = "包含关系" if rel_type == "包含" else "次序关系"
        
        xml += f"\t\t\t<class_name>{class_name}</class_name>\n"
        xml += f"\t\t\t<mask>知识连线</mask>\n"
        xml += f"\t\t\t<classification>{classification}</classification>\n"
        xml += f"\t\t\t<head_need>内容方法型节点</head_need>\n"
        xml += f"\t\t\t<tail_need>内容方法型节点</tail_need>\n"
        xml += f"\t\t</relation>\n"
    
    xml += "\t</relations>\n</KG>"
    return xml

# 使用示例
import argparse

def main():
    parser = argparse.ArgumentParser(description='Convert JSON to XML for knowledge graph')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('-o', '--output_file', type=str, default=None, help='Path to the output XML file')
    args = parser.parse_args()

    print(args.input_file)

    with open(args.input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    xml_output = json_to_xml(json_data)
    out_path = args.output_file if args.output_file else args.input_file.replace('.json', '.xml')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml_output)
    print(f"XML file saved to {out_path}")

if __name__ == "__main__":
    main()
