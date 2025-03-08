import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

# 创建图形
fig, ax = plt.subplots(figsize=(16, 12))

# 定义模块和颜色
modules = ['数据管理模块', '风险预测模块', '患者分群模块', '治疗效果分析模块', '实时监测模块']
colors = ['#64B5F6', '#81C784', '#FFD54F', '#FF8A65', '#BA68C8']
module_width = 3.2  # 增加模块宽度
module_height = 2.5  # 增加模块高度
padding = 0.4

# 定义模块位置 - 更大的间距
positions = {
    '数据管理模块': (7, 2),
    '风险预测模块': (3, 6),
    '患者分群模块': (7, 6),
    '治疗效果分析模块': (11, 6),
    '实时监测模块': (7, 10)
}

# 定义模块功能
module_functions = {
    '数据管理模块': ['数据存储管理', '数据预处理', '数据采集'],
    '风险预测模块': ['风险分层预警', '风险评分计算', '特征工程'],
    '患者分群模块': ['群体画像生成', '群体特征识别', '聚类分析'],
    '治疗效果分析模块': ['关联规则挖掘', '方案效果评估', '治疗前后对比'],
    '实时监测模块': ['实时预警推送', '异常波动识别', '生理指标监测']
}

# 绘制模块
for module, color in zip(modules, colors):
    x, y = positions[module]
    # 使用圆角矩形
    rect = patches.FancyBboxPatch(
        (x-module_width/2, y-module_height/2), 
        module_width, 
        module_height, 
        boxstyle=patches.BoxStyle("Round", pad=0.4),
        linewidth=1, 
        edgecolor='black', 
        facecolor=color, 
        alpha=0.7
    )
    ax.add_patch(rect)
    # 将模块名称放在矩形顶部中央，以避免与功能描述重叠
    ax.text(x, y-module_height/2+0.4, module, 
            ha='center', va='center', fontsize=13, fontweight='bold')

# 添加模块功能描述 - 更大的间距、竖直排列
for module, functions in module_functions.items():
    x, y = positions[module]
    for i, func in enumerate(functions):
        y_offset = 0.2 + i * 0.6  # 显著增加行间距，从模块中部开始向下排列
        ax.text(x, y-0.1+y_offset, f"- {func}", ha='center', va='center', fontsize=11)

# 在模块之间添加数据流
data_flows = [
    # 从数据管理模块到其他模块
    {'from': '数据管理模块', 'to': '风险预测模块', 'label': '规范化数据', 'color': '#64B5F6', 'offset': (0, 0), 'rad': 0.2},
    {'from': '数据管理模块', 'to': '患者分群模块', 'label': '规范化数据', 'color': '#64B5F6', 'offset': (0, 0), 'rad': 0},
    {'from': '数据管理模块', 'to': '治疗效果分析模块', 'label': '规范化数据', 'color': '#64B5F6', 'offset': (0, 0), 'rad': -0.2},
    
    # 从风险预测模块到治疗效果分析模块
    {'from': '风险预测模块', 'to': '治疗效果分析模块', 'label': '风险预测结果', 'color': '#81C784', 'offset': (0, -0.5), 'rad': 0.15},
    
    # 从患者分群模块到治疗效果分析模块
    {'from': '患者分群模块', 'to': '治疗效果分析模块', 'label': '患者分群结果', 'color': '#FFD54F', 'offset': (0, 0.5), 'rad': -0.15},
    
    # 从实时监测模块到风险预测模块
    {'from': '实时监测模块', 'to': '风险预测模块', 'label': '实时监测数据', 'color': '#BA68C8', 'offset': (-0.5, 0), 'rad': 0.3},
    
    # 从数据管理模块到实时监测模块
    {'from': '数据管理模块', 'to': '实时监测模块', 'label': '规范化数据', 'color': '#64B5F6', 'offset': (1, 0), 'rad': -0.2},
]

# 绘制数据流
for flow in data_flows:
    source = flow['from']
    target = flow['to']
    label = flow['label']
    color = flow['color']
    offset_x, offset_y = flow['offset']
    rad = flow['rad']
    
    src_x, src_y = positions[source]
    dst_x, dst_y = positions[target]
    
    # 根据模块相对位置调整连线起点和终点
    if src_y < dst_y:  # 从下到上
        src_y += module_height/2 - padding
        dst_y -= module_height/2 - padding
    elif src_y > dst_y:  # 从上到下
        src_y -= module_height/2 - padding
        dst_y += module_height/2 - padding
    elif src_x < dst_x:  # 从左到右
        src_x += module_width/2 - padding
        dst_x -= module_width/2 - padding
    elif src_x > dst_x:  # 从右到左
        src_x -= module_width/2 - padding
        dst_x += module_width/2 - padding
    
    # 应用偏移量以防止重叠
    src_x += offset_x
    src_y += offset_y
    dst_x += offset_x
    dst_y += offset_y
    
    # 创建箭头
    arrow = patches.FancyArrowPatch(
        (src_x, src_y), 
        (dst_x, dst_y),
        connectionstyle=f'arc3,rad={rad}', 
        arrowstyle='->', 
        linewidth=1.5, 
        color=color,
        mutation_scale=15
    )
    ax.add_patch(arrow)
    
    # 获取箭头路径以计算标签位置
    path = arrow.get_path()
    vertices = path.vertices
    mid_point_idx = len(vertices) // 2
    if mid_point_idx > 0:
        label_x, label_y = vertices[mid_point_idx]
    else:
        label_x = (src_x + dst_x) / 2
        label_y = (src_y + dst_y) / 2
    
    # 为标签创建白色背景，提高可读性
    text_bg = patches.Rectangle((label_x - 1, label_y - 0.2), 2, 0.4, 
                              linewidth=0, facecolor='white', alpha=0.8)
    ax.add_patch(text_bg)
    ax.text(label_x, label_y, label, ha='center', va='center', fontsize=10, fontweight='bold')

# 添加图例
legend_elements = []
for i, (module, color) in enumerate(zip(modules, colors)):
    legend_elements.append(patches.Patch(facecolor=color, edgecolor='black', alpha=0.7, label=module))

ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.05), 
         fancybox=True, shadow=True, ncol=3, fontsize=11)

# 添加标题
ax.text(7, 12, '图3-2 心血管疾病数据挖掘与可视化系统功能模块设计', 
        ha='center', va='center', fontsize=16, fontweight='bold')

# 设置坐标轴范围和隐藏坐标轴
ax.set_xlim(0, 14)
ax.set_ylim(0, 13)
ax.axis('off')

# 保存图像
output_dir = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
plt.savefig(os.path.join(output_dir, 'functional_modules.png'), bbox_inches='tight', dpi=600)
print(f"功能模块图已保存到: {output_dir}")

plt.show() 