import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import os

# 设置随机种子以确保结果可重现
np.random.seed(42)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

# 生成模拟心血管疾病相关健康指标数据
def generate_health_data(n_samples=500):
    # 定义指标及其范围
    age = np.random.randint(30, 85, n_samples)
    sbp = np.random.normal(130, 20, n_samples)  # 收缩压
    dbp = np.random.normal(85, 15, n_samples)   # 舒张压
    
    # 定义一些生理上的相关性
    # 年龄与血压相关
    sbp = sbp + 0.5 * age + np.random.normal(0, 5, n_samples)
    dbp = dbp + 0.3 * age + np.random.normal(0, 5, n_samples)
    
    # 生成心率 (与年龄负相关)
    heart_rate = 80 - 0.2 * age + np.random.normal(0, 10, n_samples)
    
    # 胆固醇 (与年龄和血压相关)
    total_cholesterol = 180 + 0.5 * age + 0.1 * sbp + np.random.normal(0, 30, n_samples)
    hdl_cholesterol = 55 - 0.1 * age + np.random.normal(0, 10, n_samples)  # 好胆固醇
    ldl_cholesterol = total_cholesterol - hdl_cholesterol - 30 + np.random.normal(0, 20, n_samples)  # 坏胆固醇
    
    # 血糖 (与年龄和胆固醇相关)
    blood_glucose = 90 + 0.2 * age + 0.05 * total_cholesterol + np.random.normal(0, 15, n_samples)
    
    # BMI (与多个指标相关)
    bmi = 22 + 0.05 * age + 0.01 * sbp + 0.02 * blood_glucose + np.random.normal(0, 3, n_samples)
    
    # 创建DataFrame
    data = pd.DataFrame({
        '年龄': age,
        '收缩压': sbp,
        '舒张压': dbp,
        '心率': heart_rate,
        '总胆固醇': total_cholesterol,
        'HDL胆固醇': hdl_cholesterol,
        'LDL胆固醇': ldl_cholesterol,
        '血糖': blood_glucose,
        'BMI指数': bmi
    })
    
    # 生成风险评分（作为多因素综合影响）
    risk_factors = (
        (data['年龄'] - 50) / 10 * 1.5 + 
        (data['收缩压'] - 120) / 20 * 2.0 +
        (data['舒张压'] - 80) / 10 * 1.0 +
        (data['总胆固醇'] - 200) / 40 * 1.2 +
        (data['HDL胆固醇'] - 40) / (-10) * 1.3 +  # HDL越高风险越低
        (data['LDL胆固醇'] - 100) / 30 * 1.5 +
        (data['血糖'] - 100) / 20 * 1.0 +
        (data['BMI指数'] - 25) / 5 * 1.2
    )
    
    # 添加脉压差计算（收缩压-舒张压）
    data['脉压差'] = data['收缩压'] - data['舒张压']
    
    # 标准化风险评分
    scaler = StandardScaler()
    risk_factors_scaled = scaler.fit_transform(risk_factors.values.reshape(-1, 1)).flatten()
    
    # 将风险评分映射到0-100之间
    risk_score = (risk_factors_scaled - np.min(risk_factors_scaled)) / (np.max(risk_factors_scaled) - np.min(risk_factors_scaled)) * 100
    data['风险评分'] = risk_score.astype(int)
    
    return data

# 生成数据
df = generate_health_data(500)

# 计算相关性矩阵
correlation = df.corr()

# 创建热图可视化
plt.figure(figsize=(12, 10))

# 创建热图
mask = np.triu(np.ones_like(correlation))
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# 绘制热图
sns.heatmap(correlation, 
            mask=mask,
            annot=True, 
            fmt=".2f", 
            cmap=cmap, 
            center=0,
            square=True, 
            linewidths=.5,
            cbar_kws={"shrink": .8})

# 添加标题和调整布局
plt.title('图4-1 心血管疾病健康指标相关性矩阵', fontsize=16, pad=20)
plt.tight_layout()

# 保存图像
output_dir = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
plt.savefig(os.path.join(output_dir, 'feature_correlation.png'), bbox_inches='tight', dpi=600)
print(f"相关性矩阵图已保存到: {output_dir}")

# 显示图表
plt.show()

# 额外创建特征分布图
plt.figure(figsize=(14, 10))

# 设置子图网格
features = ['年龄', '收缩压', '舒张压', '心率', '总胆固醇', 'HDL胆固醇', 'LDL胆固醇', '血糖', 'BMI指数', '脉压差']
n_features = len(features)
n_rows = (n_features + 1) // 2  # 向上取整

# 为每个特征创建直方图和密度图
for i, feature in enumerate(features):
    plt.subplot(n_rows, 2, i+1)
    
    # 根据风险评分对数据着色
    scatter = plt.scatter(df[feature], np.random.normal(0, 0.02, len(df)), 
              c=df['风险评分'], cmap='coolwarm', alpha=0.6, s=10)
    
    # 添加核密度估计曲线
    sns.kdeplot(df[feature], color='black', label='密度曲线')
    
    plt.title(f'{feature}分布', fontsize=12)
    plt.xlabel(feature)
    plt.grid(True, linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.suptitle('图4-2 心血管健康指标分布与风险相关性', fontsize=16, y=0.98)

# 添加颜色条
cbar_ax = plt.figure().add_axes([0.15, 0.05, 0.7, 0.02])
cbar = plt.colorbar(scatter, cax=cbar_ax, orientation='horizontal', label='风险评分')
plt.close()  # 关闭临时创建的图形

# 保存图像
plt.savefig(os.path.join(output_dir, 'feature_distribution.png'), bbox_inches='tight', dpi=600)
print(f"特征分布图已保存到: {output_dir}")

plt.show() 