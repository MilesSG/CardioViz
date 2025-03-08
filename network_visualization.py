import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import random
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
import json
import os

# 设置高分辨率图像输出
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# 设置中文字体显示
try:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
except:
    print("无法设置中文字体，使用系统默认字体")

# 定义症状、治疗方案和药物
symptoms = [
    '胸痛', '气短', '心悸', '晕厥', '疲劳', 
    '水肿', '头晕', '呼吸困难', '咳嗽', '夜间呼吸困难',
    '食欲不振', '心前区不适', '出汗增多', '焦虑', '心律不齐'
]

treatments = [
    '标准药物治疗', '介入治疗', '外科手术', '生活方式干预',
    '康复治疗', '心脏再同步治疗', '射频消融术',
    '心脏起搏器植入', '心脏瓣膜修复', '冠状动脉搭桥术'
]

medications = [
    '阿司匹林', '他汀类药物', 'β受体阻滞剂', 'ACE抑制剂', 
    '钙通道阻滞剂', '利尿剂', '抗凝药物', '硝酸酯类', 
    '抗心律失常药物', '血管紧张素受体阻滞剂',
    '噻嗪类利尿剂', '环磷酰胺', '抗血小板药物', '强心苷',
    '醛固酮拮抗剂'
]

# 创建图形对象
G = nx.Graph()

# 添加节点
for symptom in symptoms:
    G.add_node(symptom, node_type='symptom')

for treatment in treatments:
    G.add_node(treatment, node_type='treatment')

for medication in medications:
    G.add_node(medication, node_type='medication')

# 生成更现实的连接关系
# 症状与治疗方案的关联
symptom_treatment_links = {
    '胸痛': ['标准药物治疗', '介入治疗', '外科手术', '生活方式干预'],
    '气短': ['标准药物治疗', '心脏再同步治疗', '生活方式干预'],
    '心悸': ['标准药物治疗', '射频消融术', '心脏起搏器植入'],
    '晕厥': ['心脏起搏器植入', '标准药物治疗'],
    '疲劳': ['标准药物治疗', '生活方式干预', '康复治疗'],
    '水肿': ['标准药物治疗', '生活方式干预'],
    '头晕': ['标准药物治疗', '介入治疗'],
    '呼吸困难': ['标准药物治疗', '心脏再同步治疗', '生活方式干预'],
    '咳嗽': ['标准药物治疗'],
    '夜间呼吸困难': ['标准药物治疗', '生活方式干预'],
    '食欲不振': ['生活方式干预'],
    '心前区不适': ['标准药物治疗', '介入治疗'],
    '出汗增多': ['标准药物治疗', '生活方式干预'],
    '焦虑': ['生活方式干预', '标准药物治疗'],
    '心律不齐': ['抗心律失常药物', '射频消融术', '心脏起搏器植入']
}

# 治疗方案与药物的关联
treatment_medication_links = {
    '标准药物治疗': ['阿司匹林', '他汀类药物', 'β受体阻滞剂', 'ACE抑制剂', '钙通道阻滞剂', '利尿剂', '抗凝药物', '硝酸酯类'],
    '介入治疗': ['阿司匹林', '抗凝药物', '抗血小板药物'],
    '外科手术': ['抗凝药物', 'β受体阻滞剂'],
    '生活方式干预': [],
    '康复治疗': ['β受体阻滞剂', 'ACE抑制剂'],
    '心脏再同步治疗': ['β受体阻滞剂', 'ACE抑制剂', '醛固酮拮抗剂'],
    '射频消融术': ['抗心律失常药物', '抗凝药物'],
    '心脏起搏器植入': ['抗凝药物'],
    '心脏瓣膜修复': ['抗凝药物', '抗生素'],
    '冠状动脉搭桥术': ['阿司匹林', '他汀类药物', 'β受体阻滞剂']
}

# 添加边，使用权重表示关联强度
for symptom, treatments_list in symptom_treatment_links.items():
    for treatment in treatments_list:
        # 设置不同的权重表示关联强度
        weight = np.random.uniform(0.5, 2.5)
        if symptom in ['胸痛', '呼吸困难', '心悸'] and treatment in ['标准药物治疗', '介入治疗']:
            weight = np.random.uniform(2.0, 3.0)  # 更强的关联
        G.add_edge(symptom, treatment, weight=weight)

for treatment, medications_list in treatment_medication_links.items():
    for medication in medications_list:
        # 设置不同的权重表示关联强度
        weight = np.random.uniform(0.5, 2.5)
        if treatment == '标准药物治疗' and medication in ['阿司匹林', '他汀类药物', 'β受体阻滞剂', 'ACE抑制剂']:
            weight = np.random.uniform(2.0, 3.0)  # 更强的关联
        G.add_edge(treatment, medication, weight=weight)

# 设置节点类型的颜色映射
color_map = {'symptom': '#E57373', 'treatment': '#64B5F6', 'medication': '#81C784'}
node_colors = [color_map[G.nodes[node]['node_type']] for node in G.nodes()]

# 设置节点大小，基于连接数（度）
node_sizes = [max(100, G.degree(node) * 100) for node in G.nodes()]

# 边的权重影响连线的宽度
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

# 创建布局 - 使用spring_layout增加可读性
np.random.seed(42)  # 确保结果可复现
pos = nx.spring_layout(G, k=0.3, iterations=50)

# 调整位置，使类型相似的节点相对聚集
pos_adjusted = pos.copy()
centers = {'symptom': np.array([-0.3, 0.3]), 'treatment': np.array([0.3, 0.3]), 'medication': np.array([0, -0.3])}
for node in G.nodes():
    node_type = G.nodes[node]['node_type']
    # 向各类型中心靠近，但保持一定的原始分布
    pos_adjusted[node] = pos[node] * 0.7 + centers[node_type] * 0.3

# 创建图形
plt.figure(figsize=(16, 12))
plt.margins(0.15)

# 绘制边，使用权重调整线宽
nx.draw_networkx_edges(G, pos_adjusted, width=edge_weights, alpha=0.7, edge_color="#AAAAAA")

# 绘制节点
nx.draw_networkx_nodes(G, pos_adjusted, 
                      nodelist=list(G.nodes()),
                      node_size=node_sizes,
                      node_color=node_colors,
                      alpha=0.9)

# 添加节点标签，根据节点类型设置不同的字体大小
label_font_sizes = {}
for node in G.nodes():
    if G.nodes[node]['node_type'] == 'symptom':
        label_font_sizes[node] = 10
    elif G.nodes[node]['node_type'] == 'treatment':
        label_font_sizes[node] = 11
    else:  # medication
        label_font_sizes[node] = 9

# 分别绘制不同类型的标签，使用不同字体大小
for node_type, font_size in [('symptom', 10), ('treatment', 11), ('medication', 9)]:
    nodes_of_type = [node for node in G.nodes() if G.nodes[node]['node_type'] == node_type]
    labels = {node: node for node in nodes_of_type}
    nx.draw_networkx_labels(G, pos_adjusted, labels=labels, font_size=font_size, 
                           font_family='SimHei', font_weight='bold')

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

# 保存图形
output_dir = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
plt.savefig(os.path.join(output_dir, 'network_visualization.png'), bbox_inches='tight', dpi=600)
plt.savefig(os.path.join(output_dir, 'network_visualization.pdf'), bbox_inches='tight', dpi=600)
print(f"图像已保存到: {output_dir}")

plt.show() 