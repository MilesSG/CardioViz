import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
from sklearn.inspection import permutation_importance
import shap
import os
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

# 设置随机种子以确保结果可重现
np.random.seed(42)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

# 生成模拟患者数据
def generate_patient_data(n_samples=1000):
    # 年龄
    age = np.random.normal(60, 15, n_samples)
    age = np.clip(age, 30, 90)
    
    # 收缩压 (SBP)
    sbp = np.random.normal(130, 20, n_samples)
    sbp = np.clip(sbp, 90, 200)
    
    # 舒张压 (DBP)
    dbp = np.random.normal(80, 15, n_samples)
    dbp = np.clip(dbp, 50, 120)
    
    # 总胆固醇 (TC)
    tc = np.random.normal(200, 40, n_samples)
    tc = np.clip(tc, 120, 300)
    
    # HDL胆固醇
    hdl = np.random.normal(50, 15, n_samples)
    hdl = np.clip(hdl, 20, 100)
    
    # LDL胆固醇
    ldl = np.random.normal(120, 35, n_samples)
    ldl = np.clip(ldl, 50, 250)
    
    # 空腹血糖
    fasting_glucose = np.random.normal(100, 25, n_samples)
    fasting_glucose = np.clip(fasting_glucose, 70, 200)
    
    # 糖化血红蛋白(HbA1c)
    hba1c = np.random.normal(5.7, 1.2, n_samples)
    hba1c = np.clip(hba1c, 4.0, 10.0)
    
    # BMI
    bmi = np.random.normal(26, 5, n_samples)
    bmi = np.clip(bmi, 18, 40)
    
    # 吸烟状态 (0=不吸烟, 1=吸烟)
    smoking = np.random.binomial(1, 0.3, n_samples)
    
    # 家族史 (0=无, 1=有)
    family_history = np.random.binomial(1, 0.25, n_samples)
    
    # 糖尿病 (0=无, 1=有)
    diabetes = np.random.binomial(1, 0.2, n_samples)
    
    # 心率
    heart_rate = np.random.normal(75, 10, n_samples)
    heart_rate = np.clip(heart_rate, 50, 110)
    
    # 既往心血管事件 (0=无, 1=有)
    previous_cvd = np.random.binomial(1, 0.15, n_samples)
    
    # 计算风险得分 (模拟实际风险因素的影响)
    risk_score = (
        0.035 * (age - 50) +
        0.022 * (sbp - 120) +
        0.018 * (dbp - 80) +
        0.016 * (tc - 180) +
        -0.025 * (hdl - 40) +
        0.017 * (ldl - 100) +
        0.019 * (fasting_glucose - 90) +
        0.24 * (hba1c - 5.5) +
        0.12 * (bmi - 25) +
        0.52 * smoking +
        0.35 * family_history +
        0.45 * diabetes +
        0.01 * (heart_rate - 70) +
        0.60 * previous_cvd
    )
    
    # 添加一些非线性关系和交互作用
    risk_score += 0.01 * (age - 50) * (sbp - 120)  # 年龄和血压的交互
    risk_score += 0.008 * (tc - 180) * (ldl - 100)  # 总胆固醇和LDL的交互
    risk_score += 0.15 * smoking * (sbp - 120)  # 吸烟和血压的交互
    
    # 添加一些随机噪声
    risk_score += np.random.normal(0, 0.5, n_samples)
    
    # 标准化风险分数到0-1范围
    risk_score = 1 / (1 + np.exp(-risk_score))  # Sigmoid函数
    
    # 转换为二元结果 (0=无事件, 1=有事件)
    # 使用概率阈值0.5
    outcome = (risk_score > 0.5).astype(int)
    
    # 创建DataFrame
    df = pd.DataFrame({
        '年龄': age,
        '收缩压': sbp,
        '舒张压': dbp,
        '总胆固醇': tc,
        'HDL胆固醇': hdl,
        'LDL胆固醇': ldl,
        '空腹血糖': fasting_glucose,
        'HbA1c': hba1c,
        'BMI指数': bmi,
        '吸烟': smoking,
        '家族史': family_history,
        '糖尿病': diabetes,
        '心率': heart_rate,
        '既往心血管事件': previous_cvd,
        '风险概率': risk_score,
        '心血管事件': outcome
    })
    
    return df

# 生成数据
df = generate_patient_data(1500)

# 划分特征和目标变量
features = [
    '年龄', '收缩压', '舒张压', '总胆固醇', 'HDL胆固醇', 'LDL胆固醇', 
    '空腹血糖', 'HbA1c', 'BMI指数', '吸烟', '家族史', '糖尿病', '心率', '既往心血管事件'
]
X = df[features]
y = df['心血管事件']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# 训练随机森林模型
rf = RandomForestClassifier(
    n_estimators=500, 
    max_depth=15,
    min_samples_leaf=5,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)

# 获取预测概率
y_proba_train = rf.predict_proba(X_train)[:, 1]
y_proba_test = rf.predict_proba(X_test)[:, 1]

# 计算ROC曲线
fpr, tpr, _ = roc_curve(y_test, y_proba_test)
roc_auc = auc(fpr, tpr)

# 计算PR曲线
precision, recall, _ = precision_recall_curve(y_test, y_proba_test)
average_precision = average_precision_score(y_test, y_proba_test)

# 获取特征重要性
feature_importance = rf.feature_importances_
sorted_idx = np.argsort(feature_importance)

# 计算置换特征重要性
perm_importance = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42)
perm_sorted_idx = np.argsort(perm_importance.importances_mean)

# 创建可视化图表
plt.figure(figsize=(16, 14))
gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])

# 使用随机森林的特征重要性代替SHAP值
# 子图1：特征重要性（基于随机森林的特征重要性）
ax1 = plt.subplot(gs[0, 0])
importance_df = pd.DataFrame({'特征': features, '重要性': feature_importance})
importance_df = importance_df.sort_values('重要性', ascending=False)

sns.barplot(
    x='重要性', 
    y='特征', 
    data=importance_df,
    palette='viridis',
    ax=ax1
)
ax1.set_title('随机森林特征重要性', fontsize=14)
ax1.set_xlabel('特征重要性', fontsize=12)
ax1.set_ylabel('')
ax1.tick_params(axis='y', labelsize=11)

# 添加标签
for i, v in enumerate(importance_df['重要性']):
    ax1.text(v + 0.01, i, f'{v:.3f}', va='center', fontsize=10)

# 子图2：特征重要性（基于排列特征重要性）
ax2 = plt.subplot(gs[0, 1])
perm_importance_df = pd.DataFrame({
    '特征': features,
    '重要性': perm_importance.importances_mean
})
perm_importance_df = perm_importance_df.sort_values('重要性', ascending=False)

sns.barplot(
    x='重要性',
    y='特征',
    data=perm_importance_df,
    palette='plasma',
    ax=ax2
)
ax2.set_title('基于排列的特征重要性', fontsize=14)
ax2.set_xlabel('特征重要性（平均准确率下降）', fontsize=12)
ax2.set_ylabel('')
ax2.tick_params(axis='y', labelsize=11)

# 添加标签
for i, v in enumerate(perm_importance_df['重要性']):
    ax2.text(v + 0.01, i, f'{v:.3f}', va='center', fontsize=10)

# 子图3：模型性能评估（ROC和PR曲线）
ax3 = plt.subplot(gs[1, 0])

# 绘制ROC曲线
ax3.plot(fpr, tpr, color='#2196F3', lw=2, label=f'ROC曲线 (AUC = {roc_auc:.3f})')
ax3.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')

# 绘制PR曲线（使用次坐标轴）
ax3_pr = ax3.twinx()
ax3_pr.plot(recall, precision, color='#FF5722', lw=2, label=f'PR曲线 (AP = {average_precision:.3f})')

# 设置坐标轴标签和标题
ax3.set_xlabel('假阳性率 (1-特异性)', fontsize=12)
ax3.set_ylabel('真阳性率 (灵敏度)', fontsize=12, color='#2196F3')
ax3_pr.set_ylabel('精确率', fontsize=12, color='#FF5722')
ax3.set_title('模型性能评估', fontsize=14)

# 设置坐标轴范围
ax3.set_xlim([0.0, 1.0])
ax3.set_ylim([0.0, 1.02])
ax3_pr.set_ylim([0.0, 1.02])

# 设置刻度标签颜色
ax3.tick_params(axis='y', colors='#2196F3')
ax3_pr.tick_params(axis='y', colors='#FF5722')

# 添加图例
lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3_pr.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + labels2, loc='lower right', fontsize=10)

# 添加性能指标文本
metrics_text = (
    f"测试集性能指标:\n"
    f"AUC = {roc_auc:.3f}\n"
    f"平均精确率 = {average_precision:.3f}\n"
    f"灵敏度@0.5 = {tpr[np.abs(fpr - 0.5).argmin()]:.3f}\n"
    f"特异性@0.5 = {1-fpr[np.abs(tpr - 0.5).argmin()]:.3f}"
)
ax3.text(0.05, 0.05, metrics_text, transform=ax3.transAxes, 
        bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'), fontsize=10)

# 子图4：特征重要性热图
ax4 = plt.subplot(gs[1, 1])

# 生成不同风险级别的患者预测
risk_levels = pd.cut(y_proba_test, bins=[0, 0.3, 0.7, 1.0], labels=['低风险', '中风险', '高风险'])
risk_groups = pd.DataFrame({
    '风险级别': risk_levels,
    '预测概率': y_proba_test
})

risk_group_counts = risk_groups['风险级别'].value_counts()
risk_group_percentages = risk_group_counts / len(risk_groups) * 100

# 特征在不同风险组之间的差异
feature_by_risk = pd.DataFrame()
for feature in features:
    for risk_level in ['低风险', '中风险', '高风险']:
        idx = risk_levels == risk_level
        feature_by_risk.loc[feature, risk_level] = X_test.loc[idx, feature].mean()

# 标准化数据用于热图
feature_by_risk_norm = (feature_by_risk - feature_by_risk.min(axis=1).values.reshape(-1, 1)) / \
                      (feature_by_risk.max(axis=1) - feature_by_risk.min(axis=1)).values.reshape(-1, 1)

# 按照特征重要性排序
top_features = importance_df['特征'][:10].values
feature_by_risk_norm = feature_by_risk_norm.loc[top_features]
feature_by_risk = feature_by_risk.loc[top_features]

# 绘制热图
sns.heatmap(feature_by_risk_norm, annot=feature_by_risk.round(1), fmt='.1f', 
           cmap='YlGnBu', linewidths=.5, ax=ax4)
ax4.set_title('不同风险级别的特征分布', fontsize=14)
ax4.set_xlabel('风险级别', fontsize=12)
ax4.set_ylabel('主要风险特征', fontsize=12)

# 设置整体标题
plt.suptitle('图4-4 随机森林模型特征重要性与性能分析', fontsize=16, y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.97])

# 保存图像
output_dir = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
plt.savefig(os.path.join(output_dir, 'rf_model_analysis.png'), bbox_inches='tight', dpi=600)
print(f"随机森林模型分析图已保存到: {output_dir}")

# 显示图表
plt.show() 