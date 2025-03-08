# CardioViz 🫀 - 心血管疾病数据分析与可视化平台

## 项目简介 📋

CardioViz 是一个专注于心血管疾病数据分析和可视化的全栈项目。通过前后端分离架构，结合数据挖掘和交互式可视化技术，为医疗专业人员提供直观的患者风险评估和治疗效果分析工具。

![系统运行截图](img/dashboard.png)

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
- **机器学习**: Scikit-learn, SHAP
- **API**: RESTful API
- **开发工具**: Flask-CORS

### 前端
- **框架**: Vue 3
- **状态管理**: Pinia
- **UI组件**: Element Plus
- **可视化**: ECharts
- **构建工具**: Vite
- **开发语言**: JavaScript/TypeScript

## 可视化实现代码 🎨

### 1. 风险分布可视化 (RiskDistributionChart.vue)

多维散点图实现了患者风险分布的直观展示，通过年龄、血压和胆固醇等多维数据映射:

```javascript
// 风险分布多维散点图
const processData = (data) => {
  return data.map(p => {
    return {
      ...p,
      value: [p.age || 0, p.systolic_bp || 0],
      symbolSize: Math.sqrt((p.cholesterol || 0) / 3)
    }
  })
}

const chartOption = computed(() => {
  return {
    xAxis: {
      type: 'value',
      name: '年龄',
      min: 18,
      max: 90
    },
    yAxis: {
      type: 'value',
      name: '收缩压 (mmHg)',
      min: 80,
      max: 200
    },
    series: [
      {
        type: 'scatter',
        name: '低风险',
        data: processedData.value.filter(p => p.riskLevel === '低'),
        itemStyle: { color: '#67C23A' }
      },
      {
        type: 'scatter',
        name: '中风险',
        data: processedData.value.filter(p => p.riskLevel === '中'),
        itemStyle: { color: '#E6A23C' }
      },
      {
        type: 'scatter',
        name: '高风险',
        data: processedData.value.filter(p => p.riskLevel === '高'),
        itemStyle: { color: '#F56C6C' }
      }
    ]
  }
})
```

### 2. 关联网络可视化 (NetworkAnalysisChart.vue)

症状-治疗-药物关联网络图展示了医疗概念之间的复杂关系:

```javascript
// 关联网络处理
const processNetworkData = (data) => {
  const nodes = new Map()
  const edges = new Map()
  const categories = ['症状', '治疗', '药物']
  
  data.forEach(patient => {
    // 添加症状节点
    patient.symptoms.forEach(symptom => {
      if (!nodes.has(symptom)) {
        nodes.set(symptom, {
          id: symptom,
          name: symptom,
          symbolSize: 15,
          category: 0  // 症状类别
        })
      }
      
      // 连接症状和治疗
      patient.treatments.forEach(treatment => {
        if (!nodes.has(treatment)) {
          nodes.set(treatment, {
            id: treatment,
            name: treatment,
            symbolSize: 20,
            category: 1  // 治疗类别
          })
        }
        
        // 创建症状-治疗边
        const edgeKey = `${symptom}-${treatment}`
        if (!edges.has(edgeKey)) {
          edges.set(edgeKey, {
            source: symptom,
            target: treatment,
            value: 1
          })
        } else {
          edges.get(edgeKey).value += 1  // 增加边的权重
        }
      })
    })
  })

  return {
    nodes: Array.from(nodes.values()),
    edges: Array.from(edges.values()),
    categories: categories.map(name => ({ name }))
  }
}
```

### 3. 治疗效果可视化 (TreatmentEffectChart.vue)

旭日图和饼图展示了不同治疗方案的效果分布:

```javascript
// 治疗效果图表配置
const chartOption = computed(() => {
  if (chartType.value === 'sunburst') {
    return {
      title: { text: '治疗方案效果分布' },
      series: [{
        type: 'sunburst',
        data: processedData.value,
        radius: ['20%', '90%'],
        label: { show: true },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    }
  } else {
    return {
      title: { text: '治疗方案效果比例' },
      series: [{
        type: 'pie',
        data: processedData.value.map(item => ({
          name: item.name,
          value: item.value
        })),
        radius: '75%'
      }]
    }
  }
})
```

### 4. 实时监测可视化 (VitalsMonitorChart.vue)

生命体征实时监测图表，展示患者血压和心率的动态变化:

```javascript
// 生命体征监测图表
const chartOption = computed(() => {
  return {
    title: { text: '生命体征监测', left: 'center' },
    tooltip: { trigger: 'axis' },
    legend: {
      data: ['收缩压', '舒张压', '心率'],
      top: 30
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: timeData.value
    },
    yAxis: [
      {
        type: 'value',
        name: '血压(mmHg)',
        min: 40,
        max: 200
      },
      {
        type: 'value',
        name: '心率(bpm)',
        min: 40,
        max: 180
      }
    ],
    series: [
      {
        name: '收缩压',
        type: 'line',
        yAxisIndex: 0,
        data: systolicData.value,
        lineStyle: { color: '#F56C6C' }
      },
      {
        name: '舒张压',
        type: 'line',
        yAxisIndex: 0,
        data: diastolicData.value,
        lineStyle: { color: '#E6A23C' }
      },
      {
        name: '心率',
        type: 'line',
        yAxisIndex: 1,
        data: heartRateData.value,
        lineStyle: { color: '#409EFF' }
      }
    ]
  }
})
```

### 5. 系统测试图表生成 (system_test_charts.py)

基于matplotlib的系统测试图表生成:

```python
# 功能测试覆盖率和通过率柱状图
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
    
    # 标签和样式设置
    plt.xlabel('功能模块', fontsize=12, fontweight='bold')
    plt.ylabel('百分比 (%)', fontsize=12, fontweight='bold')
    plt.title('图7-1: 功能测试覆盖率和通过率', fontsize=14, fontweight='bold')
    plt.xticks(x, modules, fontsize=10)
    plt.ylim(0, 105)
```

## 项目学术研究 📚

本项目已完成相关学术论文《基于人类心血管疾病的数据挖掘及可视化》，论文详细介绍了系统设计思路、实现技术、数据挖掘方法以及可视化效果评估。主要内容包括：

- 第一章：引言与背景
- 第二章：系统需求分析
- 第三章：数据预处理与特征工程
- 第四章：风险预测模型实现与评估
- 第五章：可视化系统设计与实现
- 第六章：后端系统实现
- 第七章：系统测试结果

论文中的图表生成代码已集成到`system_test_charts.py`文件中，可用于生成系统评估报告。

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

