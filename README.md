# CardioViz 🫀 - 心血管疾病数据分析与可视化平台

## 项目简介 📋

CardioViz 是一个专注于心血管疾病数据分析和可视化的全栈项目。通过前后端分离架构，结合数据挖掘和交互式可视化技术，为医疗专业人员提供直观的患者风险评估和治疗效果分析工具。

项目截屏：
![统运行截图](img/image.png)

## 功能特点 ✨

- 🔍 **风险预测分析**
  - 基于多维度健康指标的患者风险评估
  - 直观的风险分布可视化
  - 实时风险等级预警
  - 动态风险评分系统

- 📊 **数据可视化**
  - 交互式散点图展示患者分布
  - 动态时间序列分析
  - 症状-治疗-药物关联网络图
  - 治疗效果评估图表

- 🤖 **智能分析**
  - 多维度特征分析
  - 治疗效果追踪
  - 患者分组管理
  - 实时数据更新

- 📈 **实时监测**
  - 血压和心率时间序列分析
  - 患者状态动态跟踪
  - 治疗响应评估
  - 异常指标预警

## 技术栈 🛠️

### 后端
- **框架**: Flask
- **数据处理**: Python, NumPy, Pandas
- **API**: RESTful API
- **开发工具**: Flask-CORS

### 前端
- **框架**: Vue 3
- **状态管理**: Pinia
- **UI组件**: Element Plus
- **可视化**: ECharts
- **构建工具**: Vite
- **开发语言**: JavaScript/TypeScript

## 项目结构 📁

```
CardioViz/
├── backend/                # 后端目录
│   ├── app.py             # Flask应用主文件
│   └── requirements.txt   # Python依赖
├── frontend/              # 前端目录
│   ├── src/              # 源代码
│   │   ├── components/   # Vue组件
│   │   ├── stores/       # Pinia状态管理
│   │   ├── views/        # 页面视图
│   │   ├── router/       # 路由配置
│   │   ├── App.vue       # 根组件
│   │   └── main.js       # 入口文件
│   ├── package.json      # 前端依赖
│   └── vite.config.js    # Vite配置
└── README.md             # 项目文档
```

## 安装指南 📥

1. 克隆项目
```bash
git clone https://github.com/MilesSG/CardioViz.git
cd CardioViz
```

2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

3. 安装前端依赖
```bash
cd frontend
npm install
```

4. 启动后端服务
```bash
cd backend
python app.py
```

5. 启动前端服务
```bash
cd frontend
npm run dev
```

6. 访问应用
```
后端API: http://127.0.0.1:5000
前端页面: http://localhost:5173
```

## 数据说明 📊

模拟数据包含以下字段：
- 👤 **患者基本信息**
  - ID、年龄、性别
  - BMI、运动时间、吸烟史
- ❤️ **生理指标**
  - 血压（收缩压/舒张压）
  - 心率
  - 胆固醇
- 🏥 **健康状况**
  - 并发症（糖尿病等）
  - 风险等级评估
  - 运动情况
- 💊 **治疗信息**
  - 症状记录
  - 用药方案
  - 治疗方式
  - 随访记录
- 📈 **监测数据**
  - 实时生命体征
  - 治疗响应评估
  - 风险变化趋势

## 开发计划 🚀

- [ ] 优化数据生成算法
- [ ] 增加更多交互式图表
- [ ] 支持真实医疗数据导入
- [ ] 添加用户认证系统
- [ ] 优化前端性能
- [ ] 增加数据导出功能
- [ ] 完善错误处理机制
- [ ] 添加单元测试

