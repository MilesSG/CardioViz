# CardioViz 🫀 - 心血管疾病数据分析与可视化平台

## 项目简介 📋

CardioViz 是一个专注于心血管疾病数据分析和可视化的Python项目。通过数据挖掘和交互式可视化技术，为医疗专业人员提供直观的患者风险评估和治疗效果分析工具。

![CardioViz Dashboard](/img/image.png)

## 功能特点 ✨

- 🔍 **风险预测分析**
  - 基于多维度健康指标的患者风险评估
  - 直观的风险分布可视化
  - 实时风险等级预警

- 📊 **数据可视化**
  - 交互式散点图展示患者分布
  - 动态时间序列分析
  - 症状-治疗-药物关联网络图
  - 治疗效果评估图表

- 🤖 **智能分析**
  - K-means聚类分析
  - 多维度特征分析
  - 治疗效果追踪
  - 患者分组管理

- 📈 **实时监测**
  - 血压和心率时间序列分析
  - 患者状态动态跟踪
  - 治疗响应评估

## 技术栈 🛠️

- **数据处理**: Python, NumPy, Pandas
- **机器学习**: Scikit-learn
- **可视化**: Plotly, Dash
- **网络分析**: NetworkX
- **UI框架**: Dash Bootstrap Components

## 安装指南 📥

1. 克隆项目
```bash
git clone https://github.com/MilesSG/CardioViz.git
cd CardioViz
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
python main.py
```

4. 在浏览器中访问
```
http://127.0.0.1:8050
```

## 项目结构 📁

```
CardioViz/
├── main.py           # 主程序文件
├── requirements.txt  # 项目依赖
├── data.json        # 生成的模拟数据
├── screenshot.png   # 项目截图
└── README.md        # 项目文档
```

## 数据说明 📊

模拟数据包含以下字段：
- 👤 患者基本信息（ID、年龄、性别）
- ❤️ 生理指标（血压、心率、胆固醇）
- 🏥 健康状况（BMI、运动时间、吸烟史）
- 💊 治疗信息（症状、用药、治疗方案）
- 📈 监测数据（血压和心率时间序列）

## 开发计划 🚀

- [ ] 添加更多机器学习模型
- [ ] 优化数据预处理流程
- [ ] 增加更多交互式图表
- [ ] 支持真实医疗数据导入
- [ ] 添加用户认证系统

## 贡献指南 🤝

欢迎提交问题和改进建议！请遵循以下步骤：
1. Fork 项目
2. 创建新分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证 📄

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式 📧

项目维护者: MilesSG
GitHub: [@MilesSG](https://github.com/MilesSG) 