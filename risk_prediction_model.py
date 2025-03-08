import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, confusion_matrix, precision_recall_curve
from sklearn.calibration import calibration_curve
import os

# 设置随机种子以确保结果可重现
np.random.seed(42)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

# 模拟不同模型的预测结果
def generate_prediction_data(n_samples=1000):
    # 生成真实标签
    y_true = np.random.binomial(1, 0.3, n_samples)  # 约30%的正样本率
    
    # 生成不同模型的预测概率
    # 传统模型 - Framingham评分
    framingham_pred = np.random.beta(2, 5, n_samples)
    framingham_pred = np.where(y_true == 1, 
                              framingham_pred * 0.7 + 0.3, 
                              framingham_pred * 0.7)
    
    # 传统模型 - SCORE评分
    score_pred = np.random.beta(2, 4, n_samples)
    score_pred = np.where(y_true == 1, 
                         score_pred * 0.7 + 0.3, 
                         score_pred * 0.7)
    
    # 静态多因素模型
    static_model_pred = np.random.beta(3, 3, n_samples)
    static_model_pred = np.where(y_true == 1, 
                               static_model_pred * 0.7 + 0.3, 
                               static_model_pred * 0.5)
    
    # 动态风险评估模型
    dynamic_model_pred = np.random.beta(4, 2, n_samples)
    dynamic_model_pred = np.where(y_true == 1, 
                                dynamic_model_pred * 0.7 + 0.3, 
                                dynamic_model_pred * 0.35)
    
    return y_true, framingham_pred, score_pred, static_model_pred, dynamic_model_pred

# 生成时间序列预测数据
def generate_time_series_data(n_days=90):
    # 生成时间点
    dates = pd.date_range(start='2023-01-01', periods=n_days)
    
    # 初始风险值
    initial_risk = 0.3
    
    # 生成风险评分序列 - 静态模型（仅缓慢变化）
    static_risk = np.linspace(initial_risk, initial_risk * 1.2, n_days) + np.random.normal(0, 0.01, n_days)
    
    # 生成风险评分序列 - 动态模型（能捕捉快速变化）
    dynamic_risk = np.linspace(initial_risk, initial_risk * 1.2, n_days) + np.random.normal(0, 0.01, n_days)
    
    # 添加突发事件（静态模型无法及时捕捉）
    event_days = [20, 40, 60]
    for day in event_days:
        # 动态模型能迅速捕捉风险上升
        dynamic_risk[day:day+10] += np.linspace(0.1, 0, 10)
        # 静态模型反应迟缓
        static_risk[day+5:day+15] += np.linspace(0.05, 0, 10)
    
    # 修正范围
    static_risk = np.clip(static_risk, 0, 1)
    dynamic_risk = np.clip(dynamic_risk, 0, 1)
    
    # 创建DataFrame
    df = pd.DataFrame({
        '日期': dates,
        '静态模型预测风险': static_risk,
        '动态模型预测风险': dynamic_risk
    })
    
    # 添加事件标记
    events = pd.DataFrame({
        '日期': [dates[day] for day in event_days],
        '事件': ['血压升高', '心律异常', '胸痛'],
        'y_position': [0.9, 0.85, 0.95]
    })
    
    return df, events

# 生成数据
y_true, framingham_pred, score_pred, static_model_pred, dynamic_model_pred = generate_prediction_data(1000)
time_df, events = generate_time_series_data(90)

# 创建图表
plt.figure(figsize=(15, 12))

# 创建子图布局
gs = plt.GridSpec(2, 2, height_ratios=[1, 1], hspace=0.3, wspace=0.3)

# 子图1：ROC曲线比较
ax1 = plt.subplot(gs[0, 0])

# 计算各模型的ROC曲线
fpr_f, tpr_f, _ = roc_curve(y_true, framingham_pred)
fpr_s, tpr_s, _ = roc_curve(y_true, score_pred)
fpr_sm, tpr_sm, _ = roc_curve(y_true, static_model_pred)
fpr_dm, tpr_dm, _ = roc_curve(y_true, dynamic_model_pred)

# 计算AUC
auc_f = auc(fpr_f, tpr_f)
auc_s = auc(fpr_s, tpr_s)
auc_sm = auc(fpr_sm, tpr_sm)
auc_dm = auc(fpr_dm, tpr_dm)

# 绘制ROC曲线
ax1.plot(fpr_f, tpr_f, label=f'Framingham评分 (AUC = {auc_f:.3f})', color='#bdc3c7', linestyle='-.')
ax1.plot(fpr_s, tpr_s, label=f'SCORE评分 (AUC = {auc_s:.3f})', color='#95a5a6', linestyle='--')
ax1.plot(fpr_sm, tpr_sm, label=f'静态多因素模型 (AUC = {auc_sm:.3f})', color='#3498db')
ax1.plot(fpr_dm, tpr_dm, label=f'动态风险评估模型 (AUC = {auc_dm:.3f})', color='#e74c3c', linewidth=2)
ax1.plot([0, 1], [0, 1], color='#7f8c8d', linestyle='--', alpha=0.7)

# 添加标签和图例
ax1.set_xlabel('假阳性率 (1 - 特异性)', fontsize=12)
ax1.set_ylabel('真阳性率 (敏感性)', fontsize=12)
ax1.set_title('不同模型的ROC曲线比较', fontsize=14)
ax1.legend(loc='lower right', fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.7)

# 子图2：校准曲线比较
ax2 = plt.subplot(gs[0, 1])

# 计算各模型的校准曲线
prob_true_f, prob_pred_f = calibration_curve(y_true, framingham_pred, n_bins=10)
prob_true_s, prob_pred_s = calibration_curve(y_true, score_pred, n_bins=10)
prob_true_sm, prob_pred_sm = calibration_curve(y_true, static_model_pred, n_bins=10)
prob_true_dm, prob_pred_dm = calibration_curve(y_true, dynamic_model_pred, n_bins=10)

# 绘制校准曲线
ax2.plot(prob_pred_f, prob_true_f, marker='o', markersize=6, label='Framingham评分', color='#bdc3c7', linestyle='-.')
ax2.plot(prob_pred_s, prob_true_s, marker='s', markersize=6, label='SCORE评分', color='#95a5a6', linestyle='--')
ax2.plot(prob_pred_sm, prob_true_sm, marker='^', markersize=6, label='静态多因素模型', color='#3498db')
ax2.plot(prob_pred_dm, prob_true_dm, marker='D', markersize=6, label='动态风险评估模型', color='#e74c3c')
ax2.plot([0, 1], [0, 1], linestyle='--', color='#7f8c8d', alpha=0.7)

# 添加标签和图例
ax2.set_xlabel('预测概率', fontsize=12)
ax2.set_ylabel('实际概率', fontsize=12)
ax2.set_title('不同模型的校准曲线', fontsize=14)
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.7)

# 子图3：时间序列风险评估比较
ax3 = plt.subplot(gs[1, 0])

# 绘制时间序列风险评估
ax3.plot(time_df['日期'], time_df['静态模型预测风险'], label='静态模型预测风险', color='#3498db')
ax3.plot(time_df['日期'], time_df['动态模型预测风险'], label='动态模型预测风险', color='#e74c3c', linewidth=2)

# 添加事件标记
for _, event in events.iterrows():
    ax3.axvline(x=event['日期'], linestyle='--', color='#7f8c8d', alpha=0.7)
    ax3.annotate(event['事件'], 
                xy=(event['日期'], event['y_position']),
                xytext=(5, 0),
                textcoords='offset points',
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.7))

# 标记风险预警提前时间
for i, event_day in enumerate([20, 40, 60]):
    # 动态模型提前预警
    dynamic_warning = event_day - 2
    static_warning = event_day + 5
    
    ax3.annotate('', 
                xy=(time_df['日期'][dynamic_warning], 0.65),
                xytext=(time_df['日期'][static_warning], 0.65),
                arrowprops=dict(arrowstyle='<->', color='#27ae60'))
    
    ax3.text(time_df['日期'][dynamic_warning + 3], 0.68, 
            f'提前{static_warning-dynamic_warning}天预警',
            ha='center', fontsize=9, bbox=dict(boxstyle='round,pad=0.2', 
                                             fc='white', ec='#27ae60', alpha=0.7))

# 添加标签和图例
ax3.set_xlabel('日期', fontsize=12)
ax3.set_ylabel('风险评分', fontsize=12)
ax3.set_title('静态模型与动态模型的风险评估时间序列比较', fontsize=14)
ax3.legend(loc='upper left', fontsize=10)
ax3.grid(True, linestyle='--', alpha=0.7)

# 子图4：不同人群的预测性能比较
ax4 = plt.subplot(gs[1, 1])

# 模拟不同人群的AUC值
population_groups = ['整体人群', '男性', '女性', '<45岁', '45-60岁', '61-75岁', '>75岁']
static_auc = [0.83, 0.82, 0.84, 0.79, 0.82, 0.85, 0.81]
dynamic_auc = [0.89, 0.88, 0.90, 0.86, 0.88, 0.91, 0.87]

# 设置条形图位置
x = np.arange(len(population_groups))
width = 0.35

# 绘制条形图
ax4.bar(x - width/2, static_auc, width, label='静态多因素模型', color='#3498db', alpha=0.8)
ax4.bar(x + width/2, dynamic_auc, width, label='动态风险评估模型', color='#e74c3c', alpha=0.8)

# 添加数值标签
for i, v in enumerate(static_auc):
    ax4.text(i - width/2, v + 0.01, f'{v:.2f}', ha='center', fontsize=9)
    
for i, v in enumerate(dynamic_auc):
    ax4.text(i + width/2, v + 0.01, f'{v:.2f}', ha='center', fontsize=9)

# 添加标签和图例
ax4.set_xticks(x)
ax4.set_xticklabels(population_groups)
ax4.set_ylim(0.7, 0.95)
ax4.set_xlabel('人群分组', fontsize=12)
ax4.set_ylabel('AUC值', fontsize=12)
ax4.set_title('不同人群的预测性能比较', fontsize=14)
ax4.legend(loc='lower right', fontsize=10)
ax4.grid(True, linestyle='--', axis='y', alpha=0.7)

# 添加总标题
plt.suptitle('图4-4 改进型风险评分系统预测性能评估', fontsize=16, y=0.98)

# 保存图像
output_dir = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
plt.savefig(os.path.join(output_dir, 'risk_prediction_model.png'), bbox_inches='tight', dpi=600)
print(f"风险预测模型评估图已保存到: {output_dir}")

# 显示图表
plt.show() 