import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib.font_manager import FontProperties
import os

# 解决中文显示问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
matplotlib.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 设置保存路径
save_path = r"D:\Thesis_Revision\ZY0347 本科 基于人类心血管疾病的数据挖掘及可视化 800\ZY0347 本科 数据科学与人工智能\版本一\配图"
os.makedirs(save_path, exist_ok=True)  # 确保目录存在

# 图7-1: 功能测试覆盖率和通过率柱状图
def create_test_coverage_chart():
    # 测试数据
    modules = ['风险分布', '治疗效果', '关联网络', '实时监测', '多视图联动', '整体结果']
    coverage_rates = [98, 95, 92, 97, 99, 96.2]
    pass_rates = [100, 97, 88, 98, 100, 96.2]

    # 创建图表
    plt.figure(figsize=(10, 6))
    x = np.arange(len(modules))
    width = 0.35

    # 绘制柱状图
    bars1 = plt.bar(x - width/2, coverage_rates, width, label='测试覆盖率 (%)', color='#3498db')
    bars2 = plt.bar(x + width/2, pass_rates, width, label='测试通过率 (%)', color='#2ecc71')

    # 添加标签和标题
    plt.xlabel('功能模块', fontsize=12, fontweight='bold')
    plt.ylabel('百分比 (%)', fontsize=12, fontweight='bold')
    plt.title('图7-1: 功能测试覆盖率和通过率', fontsize=14, fontweight='bold')
    plt.xticks(x, modules, fontsize=10)
    plt.ylim(0, 105)  # 设置y轴范围，留出空间显示数值

    # 在柱状图上添加数值标签
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height}%', ha='center', va='bottom', fontsize=9)

    add_labels(bars1)
    add_labels(bars2)

    # 添加图例
    plt.legend(loc='lower right')

    # 添加网格线使图表更易读
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 调整布局
    plt.tight_layout()

    # 保存图表
    file_path = os.path.join(save_path, '图7-1_功能测试覆盖率和通过率.png')
    plt.savefig(file_path, dpi=600)
    print(f"图7-1已保存至: {file_path}")
    
    plt.close()  # 关闭当前图形

# 图7-2: 响应时间随数据量变化折线图
def create_response_time_chart():
    # 测试数据
    data_volumes = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000]

    # 各组件响应时间（毫秒）
    risk_distribution_times = [0, 95, 148, 201, 263, 310, 368, 425]
    treatment_effect_times = [0, 82, 135, 180, 240, 290, 350, 410]
    network_analysis_times = [0, 120, 210, 330, 485, 680, 840, 1050]

    plt.figure(figsize=(10, 6))

    # 绘制折线图
    plt.plot(data_volumes, risk_distribution_times, marker='o', linewidth=2, 
            label='风险分布图', color='#3498db')
    plt.plot(data_volumes, treatment_effect_times, marker='s', linewidth=2, 
            label='治疗效果图', color='#2ecc71')
    plt.plot(data_volumes, network_analysis_times, marker='^', linewidth=2, 
            label='关联网络图', color='#e74c3c')

    # 添加标签和标题
    plt.xlabel('患者数据量', fontsize=12, fontweight='bold')
    plt.ylabel('响应时间（毫秒）', fontsize=12, fontweight='bold')
    plt.title('图7-2: 不同数据量下系统响应时间', fontsize=14, fontweight='bold')

    # 设置坐标轴范围
    plt.xlim(0, 7500)
    plt.ylim(0, 1100)

    # 添加网格线
    plt.grid(linestyle='--', alpha=0.7)

    # 添加图例
    plt.legend(loc='upper left')

    # 为关键点添加标注
    plt.annotate('性能临界点', xy=(5000, 680), xytext=(5200, 800),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))

    # 调整布局
    plt.tight_layout()

    # 保存图表
    file_path = os.path.join(save_path, '图7-2_响应时间随数据量变化.png')
    plt.savefig(file_path, dpi=600)
    print(f"图7-2已保存至: {file_path}")
    
    plt.close()  # 关闭当前图形

if __name__ == "__main__":
    create_test_coverage_chart()
    create_response_time_chart()
    print("所有图表生成完成。") 