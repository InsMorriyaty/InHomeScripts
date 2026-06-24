import json

def extract_dnds_mle(json_path, output_txt="branch_dnds_mle.txt"):
    """
    解析HyPhy FitMG94结果JSON，提取各分支dN、dS、MLE(ω)
    :param json_path: HyPhy输出的JSON文件路径
    :param output_txt: 结果输出文本路径
    """
    # 读取JSON文件
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 定位分支属性核心数据
    branch_info = data.get("branch attributes", {}).get("0", {})
    output_lines = []
    # 写入表头
    output_lines.append("分支名称\tdN\t\t\tdS\t\t\tMLE(ω)")

    # 遍历所有物种/节点分支
    for branch_name, attr_dict in branch_info.items():
        # 提取核心指标
        dN = attr_dict.get("dN", "N/A")
        dS = attr_dict.get("dS", "N/A")
        mle_omega = attr_dict.get("Confidence Intervals", {}).get("MLE", "N/A")

        # 统一保留8位小数，规范数值格式
        try:
            dN = f"{float(dN):.8f}"
            dS = f"{float(dS):.8f}"
            mle_omega = f"{float(mle_omega):.8f}"
        except (ValueError, TypeError):
            pass

        # 拼接单行结果
        line = f"{branch_name}\t{dN}\t{dS}\t{mle_omega}"
        output_lines.append(line)

    # 写入结果文件
    with open(output_txt, "w", encoding="utf-8") as out_file:
        out_file.write("\n".join(output_lines))

    print(f"✅ 数据提取完成！结果已保存至：{output_txt}")
    print("\n===== 提取结果预览 =====")
    print("\n".join(output_lines))

import sys 

f1 = sys.argv[1]
f2 = sys.argv[2]
extract_dnds_mle(f1, f2)
