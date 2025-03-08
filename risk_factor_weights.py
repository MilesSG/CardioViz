import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import os

# 设置随机种子以确保结果可重现
np.random.seed(42)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

# 设置图表大小
plt.figure(figsize=(14, 10))

# 创建子图布局
gs = plt.GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1], hspace=0.3, wspace=0.3)

# 主要风险因素及其权重
risk_factors = [
    '年龄', '收缩压', 'LDL胆固醇', '吸烟史', 
    '糖尿病', '家族史', 'HDL胆固醇', 'BMI指数', 
    '心率', '血糖', '运动量', '舒张压'
]

# 权重（模拟基于医学知识和数据分析的结果）
weights = {
    '年龄': 2.30,
    '收缩压': 1.85,
    'LDL胆固醇': 1.70,
    '吸烟史': 1.60,
    '糖尿病': 1.55,
    '家族史': 1.50,
    'HDL胆固醇': -1.40,  # 负值表示保护因素
    'BMI指数': 1.25,
    '心率': 1.10,
    '血糖': 1.05,
    '运动量': -1.00,  # 负值表示保护因素
    '舒张压': 0.95
}

# 模拟不同年龄组的权重变化
age_groups = ['<45岁', '45-60岁', '61-75岁', '>75岁']
weight_by_age = {
    '<45岁': {
        '年龄': 1.50,
        '收缩压': 1.40,
        'LDL胆固醇': 1.50,
        '吸烟史': 1.80,
        '糖尿病': 1.40,
        '家族史': 1.70,
        'HDL胆固醇': -1.30,
        'BMI指数': 1.50,
        '心率': 1.00,
        '血糖': 0.90,
        '运动量': -1.20,
        '舒张压': 1.00
    },
    '45-60岁': {
        '年龄': 1.90,
        '收缩压': 1.70,
        'LDL胆固醇': 1.80,
        '吸烟史': 1.70,
        '糖尿病': 1.60,
        '家族史': 1.60,
        'HDL胆固醇': -1.40,
        'BMI指数': 1.30,
        '心率': 1.10,
        '血糖': 1.05,
        '运动量': -1.10,
        '舒张压': 0.95
    },
    '61-75岁': {
        '年龄': 2.30,
        '收缩压': 2.00,
        'LDL胆固醇': 1.70,
        '吸烟史': 1.50,
        '糖尿病': 1.70,
        '家族史': 1.40,
        'HDL胆固醇': -1.50,
        'BMI指数': 1.10,
        '心率': 1.15,
        '血糖': 1.20,
        '运动量': -0.90,
        '舒张压': 0.90
    },
    '>75岁': {
        '年龄': 2.50,
        '收缩压': 2.10,
        'LDL胆固醇': 1.60,
        '吸烟史': 1.30,
        '糖尿病': 1.80,
        '家族史': 1.20,
        'HDL胆固醇': -1.30,
        'BMI指数': 0.90,
        '心率': 1.20,
        '血糖': 1.30,
        '运动量': -0.70,
        '舒张压': 0.85
    }
}

# 模拟不同模型的风险因素重要性
model_importance = {
    '随机森林': {
        '年龄': 2.40,
        '收缩压': 1.95,
        'LDL胆固醇': 1.80,
        '吸烟史': 1.55,
        '糖尿病': 1.60,
        '家族史': 1.45,
        'HDL胆固醇': 1.35,
        'BMI指数': 1.20,
        '心率': 1.05,
        '血糖': 1.10,
        '运动量': 0.90,
        '舒张压': 0.95
    },
    'XGBoost': {
        '年龄': 2.35,
        '收缩压': 1.90,
        'LDL胆固醇': 1.75,
        '吸烟史': 1.70,
        '糖尿病': 1.55,
        '家族史': 1.50,
        'HDL胆固醇': 1.40,
        'BMI指数': 1.25,
        '心率': 1.15,
        '血糖': 1.00,
        '运动量': 0.95,
        '舒张压': 0.90
    },
    'SHAP分析': {
        '年龄': 2.25,
        '收缩压': 1.90,
        'LDL胆固醇': 1.65,
        '吸烟史': 1.55,
        '糖尿病': 1.60,
        '家族史': 1.45,
        'HDL胆固醇': 1.50,
        'BMI指数': 1.30,
        '心率': 1.10,
        '血糖': 1.05,
        '运动量': 1.10,
        '舒张压': 1.00
    }
}

# 子图1：主要风险因素权重水平条形图
ax1 = plt.subplot(gs[0, 0])

# 对风险因素按权重绝对值进行排序
sorted_factors = sorted(risk_factors, key=lambda x: abs(weights[x]), reverse=True)
sorted_weights = [weights[factor] for factor in sorted_factors]

# 设置条形图颜色
colors = ['#ff6b6b' if w > 0 else '#4ecdc4' for w in sorted_weights]

# 绘制条形图
bars = ax1.barh(sorted_factors, sorted_weights, color=colors)

# 添加数值标签
for bar in bars:
    width = bar.get_width()
    label_x_pos = width + 0.05 if width > 0 else width - 0.2
    ax1.text(label_x_pos, bar.get_y() + bar.get_height()/2, 
             f'{abs(width):.2f}', 
             va='center', fontsize=9)

# 添加网格和标签
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.set_xlabel('权重系数', fontsize=12)
ax1.set_title('主要心血管疾病风险因素权重', fontsize=14)

# 添加解释性文本
props = dict(boxstyle='round', facecolor='white', alpha=0.7)
ax1.text(1.85, 0.05, '注：正值表示风险因素，\n负值表示保护因素',
         transform=ax1.transAxes, fontsize=10,
         verticalalignment='bottom', bbox=props)

# 子图2：不同年龄组的权重变化
ax2 = plt.subplot(gs[0, 1])

# 选择主要的几个风险因素进行展示
key_factors = ['年龄', '收缩压', 'LDL胆固醇', '吸烟史', '糖尿病']
age_weights_data = []

for factor in key_factors:
    weights_by_age = [weight_by_age[age][factor] for age in age_groups]
    age_weights_data.append(weights_by_age)

# 绘制热图
im = ax2.imshow(age_weights_data, cmap='YlOrRd')

# 设置标签
ax2.set_yticks(np.arange(len(key_factors)))
ax2.set_xticks(np.arange(len(age_groups)))
ax2.set_yticklabels(key_factors)
ax2.set_xticklabels(age_groups)
ax2.set_title('不同年龄组的风险因素权重变化', fontsize=14)

# 为热图单元格添加文本标注
for i in range(len(key_factors)):
    for j in range(len(age_groups)):
        text = ax2.text(j, i, f'{age_weights_data[i][j]:.2f}',
                      ha="center", va="center", color="black", fontsize=9)

# 添加颜色条
plt.colorbar(im, ax=ax2, label='权重系数')

# 子图3：不同模型的风险因素重要性比较
ax3 = plt.subplot(gs[1, 0])

# 准备数据
models = list(model_importance.keys())
comparison_factors = ['年龄', '收缩压', 'LDL胆固醇', '吸烟史', '糖尿病', 'BMI指数']
model_data = []

for model in models:
    model_data.append([model_importance[model][factor] for factor in comparison_factors])

# 绘制分组条形图
x = np.arange(len(comparison_factors))  # 因素位置
width = 0.25  # 条形宽度

# 绘制不同模型的条形
for i, model in enumerate(models):
    offset = (i - len(models)/2 + 0.5) * width
    ax3.bar(x + offset, model_data[i], width, label=model, 
           alpha=0.7, color=plt.cm.Set2(i))

# 设置标签和图例
ax3.set_xticks(x)
ax3.set_xticklabels(comparison_factors)
ax3.set_ylabel('重要性得分')
ax3.set_title('不同模型的风险因素重要性比较', fontsize=14)
ax3.legend(loc='upper right')
ax3.grid(True, linestyle='--', alpha=0.7)

# 子图4：专家校准前后的权重变化
ax4 = plt.subplot(gs[1, 1])

# 模拟专家校准前后的权重变化
calibration_factors = ['年龄', '收缩压', 'LDL胆固醇', '吸烟史']
before_calibration = [2.20, 1.70, 1.60, 1.50]
after_calibration = [2.30, 1.85, 1.70, 1.60]

# 计算变化百分比
change_pct = [(after - before)/before * 100 for before, after in 
             zip(before_calibration, after_calibration)]

# 创建数据框
calibration_df = pd.DataFrame({
    '因素': calibration_factors,
    '校准前': before_calibration,
    '校准后': after_calibration,
    '变化百分比': change_pct
})

# 绘制校准前后对比
x = np.arange(len(calibration_factors))
width = 0.35

ax4.bar(x - width/2, before_calibration, width, label='校准前', color='#95a5a6')
ax4.bar(x + width/2, after_calibration, width, label='校准后', color='#e67e22')

# 添加文本标注
for i, (before, after, change) in enumerate(zip(before_calibration, after_calibration, change_pct)):
    ax4.text(i - width/2, before + 0.05, f'{before:.2f}', 
             ha='center', va='bottom', fontsize=8)
    ax4.text(i + width/2, after + 0.05, f'{after:.2f}', 
             ha='center', va='bottom', fontsize=8)
    ax4.text(i, max(before, after) + 0.2, f'+{change:.1f}%', 
             ha='center', va='bottom', fontsize=8, color='#e74c3c')

# 设置标签和图例
ax4.set_xticks(x)
ax4.set_xticklabels(calibration_factors)
ax4.set_ylabel('权重系数')
ax4.set_title('专家校准前后的权重变化', fontsize=14)
ax4.legend(loc='upper right')
ax4.grid(True, linestyle='--', alpha=0.7)

# 添加总标题
plt.suptitle('图4-3 心血管疾病风险因素权重分析', fontsize=16, y=0.98)

# 调整布局
plt.tight_layout()
plt.subplots_adjust(top=0.9)

# 保存图像
output_dir = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
plt.savefig(os.path.join(output_dir, 'risk_factor_weights.png'), bbox_inches='tight', dpi=600)
print(f"风险因素权重分析图已保存到: {output_dir}")

# 显示图表
plt.show() 