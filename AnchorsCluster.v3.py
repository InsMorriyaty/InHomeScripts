import sys

# 检查输入参数
if len(sys.argv) < 2:
    print("用法：python script.py '文件1-文件2-文件3'")
    print("示例：python script.py 'file1.txt-file2.txt'")
    sys.exit(1)

f1 = sys.argv[1]
files = f1.split("-")

# 核心优化：字典+集合存储聚类（查找O(1)，自动去重）
# 初始聚类：根据你的需求，若无需默认初始值，可改为 clusters = {}，next_cluster_id = 0
clusters = {}
next_cluster_id = 0  # 聚类ID从0开始（无初始值时更合理）

for file in files:
    try:
        with open(file, 'r', encoding="utf-8") as inputfile:
            for line_num, line in enumerate(inputfile, 1):
                line = line.strip()
                # 跳过空行和###分隔符行（核心适配：你的文件用###分隔）
                if not line or line == "###":
                    continue
                parts = line.split()
                # 跳过格式错误的行（必须3列，否则视为无效）
                if len(parts) != 3:
                    print(f"警告：{file} 第{line_num}行格式错误（需3列，实际{len(parts)}列），跳过：{line}")
                    continue
                # 提取前两列RNA ID（第三列数值无需参与聚类，仅保留前两列关联）
                elem1, elem2 = parts[0], parts[1]
                
                # 关键逻辑：找到第一个包含elem1或elem2的聚类（提前break，减少循环）
                matched_cluster = None
                for cluster_id, elements in clusters.items():
                    if elem1 in elements or elem2 in elements:
                        matched_cluster = cluster_id
                        break
                
                if matched_cluster:
                    # 加入已匹配的聚类（集合自动去重）
                    clusters[matched_cluster].add(elem1)
                    clusters[matched_cluster].add(elem2)
                else:
                    # 新建聚类（用集合存储，ID自增）
                    cluster_id = f"cluster{next_cluster_id}"
                    clusters[cluster_id] = {elem1, elem2}
                    next_cluster_id += 1
    except FileNotFoundError:
        print(f"错误：文件 {file} 不存在，跳过")
        continue

# 输出结果（按聚类ID排序，元素排序后用逗号连接，格式整洁）
for cluster_id in sorted(clusters.keys(), key=lambda k: int(k.replace("cluster", ""))):
    # 集合转排序后的列表，保证输出顺序一致
    sorted_elements = sorted(clusters[cluster_id])
    print(f'{cluster_id}\t{",".join(sorted_elements)}')
