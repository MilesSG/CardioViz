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
fig, ax = plt.subplots(figsize=(12, 14))

# 定义层次和颜色
layers = ['数据层', '服务层', '表现层', '用户层']
colors = ['#A5D6A7', '#81C784', '#66BB6A', '#4CAF50']
layer_height = 2.5  # 增加高度
layer_spacing = 0.6  # 增加间距
total_width = 9.0    # 增加宽度

# 画架构层次
for i, (layer, color) in enumerate(zip(layers, colors)):
    y_pos = i * (layer_height + layer_spacing)
    rect = patches.Rectangle((0, y_pos), total_width, layer_height, 
                            linewidth=1, edgecolor='black', facecolor=color, alpha=0.8)
    ax.add_patch(rect)
    ax.text(total_width/2, y_pos + layer_height/2, layer, 
            ha='center', va='center', fontsize=16, fontweight='bold')

# 添加数据层组件
data_components = [
    '原始数据存储区', 
    '处理结果存储区'
]
comp_width = total_width/len(data_components) - 0.4  # 增加组件间距
for i, comp in enumerate(data_components):
    x_pos = i * (comp_width + 0.4) + 0.2
    y_pos = 0 * (layer_height + layer_spacing) + 0.5
    rect = patches.Rectangle((x_pos, y_pos), comp_width, layer_height - 1.0, 
                            linewidth=1, edgecolor='black', facecolor='white', alpha=0.9)
    ax.add_patch(rect)
    ax.text(x_pos + comp_width/2, y_pos + (layer_height - 1.0)/2, comp, 
            ha='center', va='center', fontsize=12)

# 添加服务层组件
service_components = [
    '数据处理模块', 
    '模型构建模块', 
    'API服务模块'
]
comp_width = total_width/len(service_components) - 0.4  # 增加组件间距
for i, comp in enumerate(service_components):
    x_pos = i * (comp_width + 0.4) + 0.2
    y_pos = 1 * (layer_height + layer_spacing) + 0.5
    rect = patches.Rectangle((x_pos, y_pos), comp_width, layer_height - 1.0, 
                            linewidth=1, edgecolor='black', facecolor='white', alpha=0.9)
    ax.add_patch(rect)
    ax.text(x_pos + comp_width/2, y_pos + (layer_height - 1.0)/2, comp, 
            ha='center', va='center', fontsize=12)

# 添加表现层组件
presentation_components = [
    '可视化组件', 
    '交互控制器', 
    '状态管理器'
]
comp_width = total_width/len(presentation_components) - 0.4  # 增加组件间距
for i, comp in enumerate(presentation_components):
    x_pos = i * (comp_width + 0.4) + 0.2
    y_pos = 2 * (layer_height + layer_spacing) + 0.5
    rect = patches.Rectangle((x_pos, y_pos), comp_width, layer_height - 1.0, 
                            linewidth=1, edgecolor='black', facecolor='white', alpha=0.9)
    ax.add_patch(rect)
    ax.text(x_pos + comp_width/2, y_pos + (layer_height - 1.0)/2, comp, 
            ha='center', va='center', fontsize=12)

# 添加用户层组件
user_components = [
    'Web浏览器', 
    '移动应用',
    '用户权限管理'
]
comp_width = total_width/len(user_components) - 0.4  # 增加组件间距
for i, comp in enumerate(user_components):
    x_pos = i * (comp_width + 0.4) + 0.2
    y_pos = 3 * (layer_height + layer_spacing) + 0.5
    rect = patches.Rectangle((x_pos, y_pos), comp_width, layer_height - 1.0, 
                            linewidth=1, edgecolor='black', facecolor='white', alpha=0.9)
    ax.add_patch(rect)
    ax.text(x_pos + comp_width/2, y_pos + (layer_height - 1.0)/2, comp, 
            ha='center', va='center', fontsize=12)

# 添加层间连接
arrow_props = dict(arrowstyle='->', connectionstyle='arc3,rad=0', linewidth=1.5, color='gray')
# 数据层到服务层
ax.annotate('', xy=(total_width/2, 1*(layer_height + layer_spacing)), 
            xytext=(total_width/2, 0*layer_height + 0*(layer_height + layer_spacing) + layer_height), 
            arrowprops=arrow_props)
# 服务层到表现层
ax.annotate('', xy=(total_width/2, 2*(layer_height + layer_spacing)), 
            xytext=(total_width/2, 1*layer_height + 1*(layer_height + layer_spacing) + layer_height), 
            arrowprops=arrow_props)
# 表现层到用户层
ax.annotate('', xy=(total_width/2, 3*(layer_height + layer_spacing)), 
            xytext=(total_width/2, 2*layer_height + 2*(layer_height + layer_spacing) + layer_height), 
            arrowprops=arrow_props)

# 添加数据流说明
ax.text(total_width/2 + 0.3, 0*layer_height + 0*(layer_height + layer_spacing) + layer_height + 0.15, 
        '数据访问接口', ha='left', va='center', fontsize=10, style='italic')
ax.text(total_width/2 + 0.3, 1*layer_height + 1*(layer_height + layer_spacing) + layer_height + 0.15, 
        '业务功能接口', ha='left', va='center', fontsize=10, style='italic')
ax.text(total_width/2 + 0.3, 2*layer_height + 2*(layer_height + layer_spacing) + layer_height + 0.15, 
        '用户交互界面', ha='left', va='center', fontsize=10, style='italic')

# 添加技术说明
technology_text = """技术实现:
数据层: MySQL, MongoDB, Redis
服务层: Python, Flask, Scikit-learn
表现层: Vue.js, ECharts, Element Plus
用户层: HTML5, CSS3, JavaScript"""

# 在右侧添加技术说明文本框
tech_rect = patches.Rectangle((total_width + 0.5, 2.0), 3.5, 6.0, 
                             linewidth=1, edgecolor='black', facecolor='#E0F2F1', alpha=0.5)
ax.add_patch(tech_rect)
ax.text(total_width + 0.5 + 0.2, 2.0 + 0.3, technology_text,
        ha='left', va='top', fontsize=11, linespacing=1.8)

# 添加标题
ax.text(total_width/2, 3*layer_height + 3*(layer_height + layer_spacing) + 1.2, 
        '图3-1 心血管疾病数据挖掘与可视化系统架构',
        ha='center', va='center', fontsize=16, fontweight='bold')

# 设置坐标轴范围和隐藏坐标轴
ax.set_xlim(-0.5, total_width + 4.5)
ax.set_ylim(-0.5, 3*layer_height + 3*(layer_height + layer_spacing) + 2.0)
ax.axis('off')

# 保存图像
output_dir = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
plt.savefig(os.path.join(output_dir, 'system_architecture.png'), bbox_inches='tight', dpi=600)
print(f"系统架构图已保存到: {output_dir}")

plt.show() 