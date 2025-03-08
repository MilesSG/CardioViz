import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import Patch

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

# 定义节点类别和内容
symptoms = ['胸痛', '气短', '心悸', '晕厥', '疲劳', '水肿', '头晕']
treatments = ['标准药物治疗', '介入治疗', '外科手术', '生活方式干预', '康复治疗']
medications = ['阿司匹林', '他汀类药物', 'β受体阻滞剂', 'ACE抑制剂', '钙通道阻滞剂', '利尿剂']

# 创建图
G = nx.Graph()

# 添加节点
for s in symptoms:
    G.add_node(s, category='symptom')
for t in treatments:
    G.add_node(t, category='treatment')
for m in medications:
    G.add_node(m, category='medication')

# 手动定义关联关系
connections = [
    # 症状-治疗
    ('胸痛', '标准药物治疗', 2.5),
    ('胸痛', '介入治疗', 2.0),
    ('气短', '标准药物治疗', 1.5),
    ('心悸', '标准药物治疗', 2.0),
    ('晕厥', '介入治疗', 1.8),
    ('疲劳', '生活方式干预', 1.2),
    ('水肿', '标准药物治疗', 1.5),
    ('头晕', '标准药物治疗', 1.0),
    # 治疗-药物
    ('标准药物治疗', '阿司匹林', 2.2),
    ('标准药物治疗', '他汀类药物', 2.0),
    ('标准药物治疗', 'β受体阻滞剂', 2.5),
    ('标准药物治疗', 'ACE抑制剂', 1.8),
    ('标准药物治疗', '钙通道阻滞剂', 1.5),
    ('标准药物治疗', '利尿剂', 1.2),
    ('介入治疗', '阿司匹林', 1.5),
    ('介入治疗', '抗凝药物', 2.0),
    ('外科手术', 'β受体阻滞剂', 1.0),
    ('康复治疗', 'β受体阻滞剂', 0.8),
]

# 添加连接
for source, target, weight in connections:
    if source in G and target in G:  # 确保节点存在
        G.add_edge(source, target, weight=weight)

# 布局
pos = nx.spring_layout(G, k=0.4, seed=42)

# 节点颜色映射
color_map = {'symptom': '#E57373', 'treatment': '#64B5F6', 'medication': '#81C784'}
node_colors = []
for node in G.nodes():
    category = G.nodes[node].get('category')
    if category in color_map:
        node_colors.append(color_map[category])
    else:
        node_colors.append('#AAAAAA')  # 默认颜色

# 节点大小基于度
node_sizes = [300 + G.degree(node) * 100 for node in G.nodes()]

# 获取边的权重
edge_weights = [G[u][v].get('weight', 1.0) for u, v in G.edges()]

# 创建图形
plt.figure(figsize=(14, 10))

# 绘制边
nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.7, edge_color='#AAAAAA')

# 绘制节点
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9)

# 绘制标签
nx.draw_networkx_labels(G, pos, font_size=10, font_family='SimHei', font_weight='bold')

# 添加图例
legend_elements = [
    Patch(facecolor=color_map['symptom'], edgecolor='k', label='症状'),
    Patch(facecolor=color_map['treatment'], edgecolor='k', label='治疗方案'),
    Patch(facecolor=color_map['medication'], edgecolor='k', label='药物')
]
plt.legend(handles=legend_elements, fontsize=12, loc='upper right')

# 添加标题
plt.title('图2-1 心血管疾病症状-治疗-药物关联网络可视化', fontsize=16, fontweight='bold', pad=20)

# 去除坐标轴
plt.axis('off')

# 保存图像
output_dir = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
plt.savefig(os.path.join(output_dir, 'network_visualization.png'), bbox_inches='tight', dpi=600)
print(f"图像已保存到: {output_dir}")

plt.show() 