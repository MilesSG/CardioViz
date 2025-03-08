import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.gridspec as gridspec
import os

# 设置随机种子以确保结果可重现
np.random.seed(42)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

# 生成模拟患者数据
def generate_patient_data(n_samples=1000):
    # 基础特征
    age = np.random.normal(60, 15, n_samples)
    age = np.clip(age, 30, 90)
    
    # 构造三个患者群体
    group_probs = [0.42, 0.35, 0.23]  # 各组占比
    group = np.random.choice([0, 1, 2], size=n_samples, p=group_probs)
    
    # 特征生成，不同组有不同的特征分布
    # 组0：低风险稳定型 - 年轻，指标正常
    # 组1：中风险波动型 - 中年，部分指标异常
    # 组2：高风险复杂型 - 老年，多指标异常
    
    # 年龄 - 不同组年龄分布不同
    age = np.where(group == 0, np.random.normal(45, 8, n_samples), age)
    age = np.where(group == 1, np.random.normal(60, 10, n_samples), age)
    age = np.where(group == 2, np.random.normal(72, 7, n_samples), age)
    age = np.clip(age, 30, 90)
    
    # 收缩压
    sbp = np.zeros(n_samples)
    sbp = np.where(group == 0, np.random.normal(118, 8, n_samples), sbp)
    sbp = np.where(group == 1, np.random.normal(135, 12, n_samples), sbp)
    sbp = np.where(group == 2, np.random.normal(150, 15, n_samples), sbp)
    sbp = np.clip(sbp, 90, 200)
    
    # 舒张压
    dbp = np.zeros(n_samples)
    dbp = np.where(group == 0, np.random.normal(75, 6, n_samples), dbp)
    dbp = np.where(group == 1, np.random.normal(85, 8, n_samples), dbp)
    dbp = np.where(group == 2, np.random.normal(95, 10, n_samples), dbp)
    dbp = np.clip(dbp, 60, 120)
    
    # 总胆固醇
    tc = np.zeros(n_samples)
    tc = np.where(group == 0, np.random.normal(170, 20, n_samples), tc)
    tc = np.where(group == 1, np.random.normal(210, 25, n_samples), tc)
    tc = np.where(group == 2, np.random.normal(250, 30, n_samples), tc)
    tc = np.clip(tc, 120, 300)
    
    # HDL胆固醇 (高密度脂蛋白，"好"胆固醇)
    hdl = np.zeros(n_samples)
    hdl = np.where(group == 0, np.random.normal(60, 10, n_samples), hdl)
    hdl = np.where(group == 1, np.random.normal(45, 8, n_samples), hdl)
    hdl = np.where(group == 2, np.random.normal(35, 7, n_samples), hdl)
    hdl = np.clip(hdl, 20, 80)
    
    # 血糖
    glucose = np.zeros(n_samples)
    glucose = np.where(group == 0, np.random.normal(90, 10, n_samples), glucose)
    glucose = np.where(group == 1, np.random.normal(110, 20, n_samples), glucose)
    glucose = np.where(group == 2, np.random.normal(140, 30, n_samples), glucose)
    glucose = np.clip(glucose, 70, 200)
    
    # BMI
    bmi = np.zeros(n_samples)
    bmi = np.where(group == 0, np.random.normal(23, 2, n_samples), bmi)
    bmi = np.where(group == 1, np.random.normal(27, 3, n_samples), bmi)
    bmi = np.where(group == 2, np.random.normal(30, 4, n_samples), bmi)
    bmi = np.clip(bmi, 18, 40)
    
    # 心率
    heart_rate = np.zeros(n_samples)
    heart_rate = np.where(group == 0, np.random.normal(70, 6, n_samples), heart_rate)
    heart_rate = np.where(group == 1, np.random.normal(78, 8, n_samples), heart_rate)
    heart_rate = np.where(group == 2, np.random.normal(85, 10, n_samples), heart_rate)
    heart_rate = np.clip(heart_rate, 50, 110)
    
    # 吸烟状态 (0=不吸烟, 1=吸烟)
    smoking_prob = np.zeros(n_samples)
    smoking_prob = np.where(group == 0, 0.1, smoking_prob)
    smoking_prob = np.where(group == 1, 0.3, smoking_prob)
    smoking_prob = np.where(group == 2, 0.5, smoking_prob)
    smoking = np.random.binomial(1, smoking_prob)
    
    # 糖尿病 (0=无, 1=有)
    diabetes_prob = np.zeros(n_samples)
    diabetes_prob = np.where(group == 0, 0.05, diabetes_prob)
    diabetes_prob = np.where(group == 1, 0.2, diabetes_prob)
    diabetes_prob = np.where(group == 2, 0.4, diabetes_prob)
    diabetes = np.random.binomial(1, diabetes_prob)
    
    # 创建DataFrame
    df = pd.DataFrame({
        '年龄': age,
        '收缩压': sbp,
        '舒张压': dbp,
        '总胆固醇': tc,
        'HDL胆固醇': hdl,
        '血糖': glucose,
        'BMI指数': bmi,
        '心率': heart_rate,
        '吸烟': smoking,
        '糖尿病': diabetes,
        '真实分组': group
    })
    
    # 添加事件发生率
    event_rate = np.zeros(n_samples)
    event_rate = np.where(group == 0, np.random.uniform(0.01, 0.05, n_samples), event_rate)
    event_rate = np.where(group == 1, np.random.uniform(0.05, 0.15, n_samples), event_rate)
    event_rate = np.where(group == 2, np.random.uniform(0.15, 0.3, n_samples), event_rate)
    df['事件发生率'] = event_rate
    
    return df

# 生成数据
df = generate_patient_data(1000)

# 提取用于聚类的特征
features = ['年龄', '收缩压', '舒张压', '总胆固醇', 'HDL胆固醇', '血糖', 'BMI指数', '心率', '吸烟', '糖尿病']
X = df[features].values

# 标准化数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 降维用于可视化
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# t-SNE降维
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)

# K-means聚类
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

# 将聚类结果添加到DataFrame
df['聚类结果'] = cluster_labels

# 创建可视化图表
plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])

# 子图1：t-SNE降维可视化聚类结果
ax1 = plt.subplot(gs[0, 0])

# 获取每个真实组在每个聚类中的数量
cross_tab = pd.crosstab(df['真实分组'], df['聚类结果'])
cluster_to_group = {i: cross_tab[i].idxmax() for i in range(n_clusters)}

# 根据主要的真实组重命名聚类
cluster_names = {
    cluster_to_group.get(0, 0): "低风险稳定型",
    cluster_to_group.get(1, 1): "中风险波动型",
    cluster_to_group.get(2, 2): "高风险复杂型"
}

scatter = ax1.scatter(X_tsne[:, 0], X_tsne[:, 1], c=df['聚类结果'], cmap='viridis', s=50, alpha=0.7)
ax1.set_title('患者分群的t-SNE可视化', fontsize=14)
ax1.set_xlabel('t-SNE特征1', fontsize=12)
ax1.set_ylabel('t-SNE特征2', fontsize=12)

# 创建自定义图例
handles = []
for i in range(n_clusters):
    mask = df['聚类结果'] == i
    percent = mask.mean() * 100
    label = f"{cluster_names.get(i, f'群体{i+1}')} ({percent:.1f}%)"
    handle = plt.Line2D([0], [0], marker='o', color='w', 
                       markerfacecolor=scatter.cmap(scatter.norm(i)), 
                       markersize=10, label=label)
    handles.append(handle)
ax1.legend(handles=handles, loc='best', fontsize=10)

# 子图2：各群体特征平均值比较
ax2 = plt.subplot(gs[0, 1])

# 计算每个聚类在各个特征上的平均值
cluster_means = df.groupby('聚类结果')[features].mean()

# 为了可视化效果，选择部分重要特征
selected_features = ['年龄', '收缩压', '总胆固醇', 'HDL胆固醇', '血糖', 'BMI指数']
cluster_means_selected = cluster_means[selected_features]

# 归一化平均值以便比较
normalized_means = (cluster_means_selected - cluster_means_selected.min()) / (cluster_means_selected.max() - cluster_means_selected.min())

# 绘制热图
sns.heatmap(normalized_means, annot=cluster_means_selected.round(1), fmt='.1f', cmap='YlGnBu', 
           linewidths=.5, ax=ax2, cbar_kws={"shrink": .8})
ax2.set_title('各群体特征平均值比较', fontsize=14)
ax2.set_xticklabels(selected_features, rotation=45, ha='right')
ax2.set_yticklabels([cluster_names.get(i, f'群体{i+1}') for i in range(n_clusters)], rotation=0)

# 子图3：雷达图 - 各群体特征对比
ax3 = plt.subplot(gs[1, 0], polar=True)

# 准备雷达图数据
features_radar = ['年龄', '收缩压', '总胆固醇', '血糖', 'BMI指数', '心率']
feature_values = cluster_means[features_radar].copy()

# 归一化数据到0-1范围
for feature in features_radar:
    feature_values[feature] = (feature_values[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())

# 设置角度
angles = np.linspace(0, 2*np.pi, len(features_radar), endpoint=False).tolist()
angles += angles[:1]  # 闭合雷达图

# 准备数据
values = feature_values.values
values = np.concatenate([values, values[:, :1]], axis=1)

# 绘制雷达图
for i, color in zip(range(n_clusters), ['#4CAF50', '#FFC107', '#F44336']):
    ax3.plot(angles, values[i], 'o-', linewidth=2, color=color, label=cluster_names.get(i, f'群体{i+1}'))
    ax3.fill(angles, values[i], alpha=0.1, color=color)

# 设置雷达图属性
ax3.set_thetagrids(np.degrees(angles[:-1]), features_radar)
ax3.set_ylim(0, 1)
ax3.set_title('各群体特征雷达图', fontsize=14, y=1.1)
ax3.legend(loc='upper right', bbox_to_anchor=(0.1, 1.1), fontsize=10)

# 子图4：各群体心血管事件发生率对比
ax4 = plt.subplot(gs[1, 1])

# 计算每个聚类的事件发生率平均值和标准误
event_stats = df.groupby('聚类结果')['事件发生率'].agg(['mean', 'sem'])
event_stats.index = event_stats.index.map(lambda x: cluster_names.get(x, f'群体{x+1}'))

# 绘制条形图
bars = ax4.bar(event_stats.index, event_stats['mean'], yerr=event_stats['sem'], 
              capsize=5, color=['#4CAF50', '#FFC107', '#F44336'], alpha=0.7)

# 添加数值标签
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.005,
             f'{height:.2%}', ha='center', va='bottom', fontsize=10)

# 计算高风险组相对于低风险组的风险倍数
risk_fold = event_stats.loc['高风险复杂型', 'mean'] / event_stats.loc['低风险稳定型', 'mean']
ax4.text(0.5, 0.85, f'高/低风险比 = {risk_fold:.1f}倍', 
         ha='center', va='center', transform=ax4.transAxes, 
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8), fontsize=12)

# 设置属性
ax4.set_ylabel('5年心血管事件发生率', fontsize=12)
ax4.set_ylim(0, max(event_stats['mean'] + event_stats['sem']) * 1.2)
ax4.set_title('各群体心血管事件发生率比较', fontsize=14)
ax4.grid(axis='y', linestyle='--', alpha=0.7)

# 设置标题和布局
plt.suptitle('图4-3 心血管疾病患者分群分析', fontsize=16, y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 保存图像
output_dir = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
plt.savefig(os.path.join(output_dir, 'patient_clustering.png'), bbox_inches='tight', dpi=600)
print(f"患者分群分析图已保存到: {output_dir}")

# 显示图表
plt.show() 