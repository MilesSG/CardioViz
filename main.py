import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import random
from datetime import datetime, timedelta
import networkx as nx
import time
from collections import deque

def generate_patient_data(n_patients=1000):
    """生成更丰富的模拟患者数据"""
    np.random.seed(42)
    data = []
    
    # 生成更真实的时间分布
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    
    # 定义治疗方案
    treatments = ['标准药物治疗', '介入手术', '生活方式干预']
    symptoms = ['胸痛', '气短', '心悸', '头晕', '疲劳']
    medications = ['阿司匹林', '他汀类药物', 'β受体阻滞剂', 'ACE抑制剂']
    
    for i in range(n_patients):
        # 基本信息
        age = random.randint(18, 90)
        gender = random.choice(['男', '女'])
        systolic_bp = random.randint(90, 180)
        diastolic_bp = random.randint(60, 120)
        heart_rate = random.randint(60, 100)
        cholesterol = random.randint(100, 300)
        smoking = random.choice(['是', '否'])
        diabetes = random.choice(['是', '否'])
        bmi = round(random.uniform(18.5, 35.0), 1)
        exercise_hours = random.randint(0, 14)
        visit_date = random.choice(dates).strftime('%Y-%m-%d')
        
        # 症状和治疗
        patient_symptoms = random.sample(symptoms, random.randint(1, 3))
        treatment = random.choice(treatments)
        patient_medications = random.sample(medications, random.randint(1, 3))
        
        # 治疗效果评估
        treatment_response = random.choice(['显著改善', '部分改善', '无明显改善'])
        follow_up_visits = random.randint(1, 5)
        
        # 时间序列数据（模拟6个月的监测数据）
        bp_history = []
        hr_history = []
        for _ in range(6):
            bp_history.append(random.randint(systolic_bp-20, systolic_bp+20))
            hr_history.append(random.randint(heart_rate-10, heart_rate+10))
        
        patient = {
            'patient_id': f'P{str(i+1).zfill(4)}',
            'age': age,
            'gender': gender,
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'heart_rate': heart_rate,
            'cholesterol': cholesterol,
            'smoking': smoking,
            'diabetes': diabetes,
            'bmi': bmi,
            'exercise_hours': exercise_hours,
            'visit_date': visit_date,
            'symptoms': patient_symptoms,
            'treatment': treatment,
            'medications': patient_medications,
            'treatment_response': treatment_response,
            'follow_up_visits': follow_up_visits,
            'bp_history': bp_history,
            'hr_history': hr_history
        }
        
        # 风险评分系统
        risk_score = 0
        if age > 60: risk_score += 2
        if systolic_bp > 140: risk_score += 2
        if diastolic_bp > 90: risk_score += 1
        if heart_rate > 90: risk_score += 1
        if cholesterol > 200: risk_score += 2
        if smoking == '是': risk_score += 2
        if diabetes == '是': risk_score += 2
        if bmi > 30: risk_score += 1
        if exercise_hours < 3: risk_score += 1
        if len(patient_symptoms) > 2: risk_score += 2
        
        if risk_score <= 4:
            patient['risk_level'] = '低'
        elif risk_score <= 8:
            patient['risk_level'] = '中'
        else:
            patient['risk_level'] = '高'
            
        data.append(patient)
    
    return data

def create_network_graph(df):
    """创建关联网络图"""
    G = nx.Graph()
    
    # 添加症状节点
    all_symptoms = set()
    for symptoms in df['symptoms']:
        all_symptoms.update(symptoms)
    for symptom in all_symptoms:
        G.add_node(symptom, node_type='symptom')
    
    # 添加治疗节点
    treatments = df['treatment'].unique()
    for treatment in treatments:
        G.add_node(treatment, node_type='treatment')
    
    # 添加药物节点
    all_medications = set()
    for meds in df['medications']:
        all_medications.update(meds)
    for med in all_medications:
        G.add_node(med, node_type='medication')
    
    # 创建边连接
    for _, row in df.iterrows():
        # 症状与治疗的关联
        for symptom in row['symptoms']:
            G.add_edge(symptom, row['treatment'])
        
        # 治疗与药物的关联
        for med in row['medications']:
            G.add_edge(row['treatment'], med)
    
    # 转换为plotly可用的格式
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        if G.nodes[node]['node_type'] == 'symptom':
            node_color.append('red')
        elif G.nodes[node]['node_type'] == 'treatment':
            node_color.append('blue')
        else:
            node_color.append('green')
    
    return edge_x, edge_y, node_x, node_y, node_text, node_color

def generate_real_time_data(base_data, window_size=50):
    """生成实时数据"""
    while True:
        # 随机选择一部分数据进行更新
        sample_size = random.randint(5, 10)
        sample_indices = random.sample(range(len(base_data)), sample_size)
        
        for idx in sample_indices:
            base_data[idx]['systolic_bp'] = random.randint(90, 180)
            base_data[idx]['heart_rate'] = random.randint(60, 100)
            
            # 更新风险评分
            risk_score = 0
            if base_data[idx]['age'] > 60: risk_score += 2
            if base_data[idx]['systolic_bp'] > 140: risk_score += 2
            if base_data[idx]['diastolic_bp'] > 90: risk_score += 1
            if base_data[idx]['heart_rate'] > 90: risk_score += 1
            if base_data[idx]['cholesterol'] > 200: risk_score += 2
            if base_data[idx]['smoking'] == '是': risk_score += 2
            if base_data[idx]['diabetes'] == '是': risk_score += 2
            if base_data[idx]['bmi'] > 30: risk_score += 1
            if base_data[idx]['exercise_hours'] < 3: risk_score += 1
            
            if risk_score <= 4:
                base_data[idx]['risk_level'] = '低'
            elif risk_score <= 8:
                base_data[idx]['risk_level'] = '中'
            else:
                base_data[idx]['risk_level'] = '高'
        
        yield pd.DataFrame(base_data)
        time.sleep(2)  # 每2秒更新一次

def create_dashboard(df):
    """创建更丰富的交互式数据可视化仪表板"""
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    # 初始统计数据
    total_patients = len(df)
    high_risk_count = len(df[df['risk_level'] == '高'])
    high_risk_percentage = round((high_risk_count / total_patients) * 100, 1)
    
    # 创建关联网络图数据
    edge_x, edge_y, node_x, node_y, node_text, node_color = create_network_graph(df)
    
    # 存储实时数据
    app.real_time_data = deque(maxlen=50)
    for i in range(6):
        app.real_time_data.append({
            'timestamp': datetime.now() - timedelta(minutes=5-i),
            'systolic_bp': df.iloc[0]['systolic_bp'],
            'heart_rate': df.iloc[0]['heart_rate']
        })
    
    app.layout = dbc.Container([
        # 顶部标题和统计信息
        dbc.Row([
            dbc.Col(
                html.H1("CardioViz - 心血管疾病数据分析与可视化",
                        className="text-center my-4 text-primary"),
                width=12
            )
        ]),
        
        # 统计卡片行（添加动画效果）
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("总患者数", className="card-title text-center"),
                        html.H2(id='total-patients', className="text-center text-primary animate__animated animate__fadeIn")
                    ])
                ], className="mb-4 shadow"),
                width=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("高风险患者", className="card-title text-center"),
                        html.H2(id='high-risk-patients', className="text-center text-danger animate__animated animate__fadeIn")
                    ])
                ], className="mb-4 shadow"),
                width=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("高风险比例", className="card-title text-center"),
                        html.H2(id='risk-percentage', className="text-center text-warning animate__animated animate__fadeIn")
                    ])
                ], className="mb-4 shadow"),
                width=4
            )
        ]),
        
        html.Hr(),
        
        # 控制面板
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("数据更新控制"),
                    dbc.CardBody([
                        dbc.Switch(
                            id='auto-update-switch',
                            label='自动更新数据',
                            value=True,
                            className="mb-2"
                        ),
                        dbc.Select(
                            id='update-interval-select',
                            options=[
                                {'label': '快速 (1秒)', 'value': '1000'},
                                {'label': '正常 (2秒)', 'value': '2000'},
                                {'label': '慢速 (5秒)', 'value': '5000'}
                            ],
                            value='2000',
                            className="mb-2"
                        )
                    ])
                ], className="mb-4 shadow")
            ], width=12)
        ]),
        
        # 第一行：风险预测和治疗效果
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("实时风险分布"),
                    dbc.CardBody([
                        dcc.Graph(id='risk-prediction'),
                        dcc.Interval(
                            id='risk-update-interval',
                            interval=2000,
                            n_intervals=0
                        )
                    ])
                ], className="mb-4 shadow")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("治疗效果分析"),
                    dbc.CardBody([
                        dcc.Graph(id='treatment-effect'),
                        dcc.Interval(
                            id='treatment-update-interval',
                            interval=2000,
                            n_intervals=0
                        )
                    ])
                ], className="mb-4 shadow")
            ], width=6)
        ]),
        
        html.Hr(),
        
        # 第二行：关联网络和实时监测
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("症状-治疗-药物关联网络"),
                    dbc.CardBody([
                        dcc.Graph(id='network-graph'),
                        dcc.Interval(
                            id='network-update-interval',
                            interval=5000,
                            n_intervals=0
                        )
                    ])
                ], className="mb-4 shadow")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("实时生命体征监测"),
                    dbc.CardBody([
                        dcc.Graph(id='vitals-monitor'),
                        dcc.Interval(
                            id='vitals-update-interval',
                            interval=1000,
                            n_intervals=0
                        ),
                        html.Div([
                            dcc.Dropdown(
                                id='patient-selector',
                                options=[{'label': f"患者 {pid}", 'value': i} 
                                        for i, pid in enumerate(df['patient_id'])],
                                value=0,
                                className="mt-3"
                            )
                        ])
                    ])
                ], className="mb-4 shadow")
            ], width=6)
        ]),
        
        html.Hr(),
        
        # 第三行：治疗效果评估
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("治疗效果实时评估"),
                    dbc.CardBody([
                        dcc.Graph(id='treatment-evaluation'),
                        dcc.Interval(
                            id='evaluation-update-interval',
                            interval=3000,
                            n_intervals=0
                        )
                    ])
                ], className="mb-4 shadow")
            ], width=12)
        ])
        
    ], fluid=True, className="px-4 py-3")
    
    # 回调函数：更新时间间隔
    @app.callback(
        [Output('risk-update-interval', 'interval'),
         Output('treatment-update-interval', 'interval'),
         Output('network-update-interval', 'interval'),
         Output('vitals-update-interval', 'interval'),
         Output('evaluation-update-interval', 'interval')],
        [Input('update-interval-select', 'value'),
         Input('auto-update-switch', 'value')]
    )
    def update_interval(interval_value, auto_update):
        if not auto_update:
            return [None] * 5
        return [int(interval_value)] * 5
    
    # 回调函数：更新统计数据
    @app.callback(
        [Output('total-patients', 'children'),
         Output('high-risk-patients', 'children'),
         Output('risk-percentage', 'children')],
        [Input('risk-update-interval', 'n_intervals')]
    )
    def update_stats(n):
        total = len(df)
        high_risk = len(df[df['risk_level'] == '高'])
        percentage = round((high_risk / total) * 100, 1)
        return f"{total}", f"{high_risk}", f"{percentage}%"
    
    # 回调函数：更新风险预测图
    @app.callback(
        Output('risk-prediction', 'figure'),
        [Input('risk-update-interval', 'n_intervals')]
    )
    def update_risk_prediction(n):
        return px.scatter(
            df,
            x='age',
            y='systolic_bp',
            color='risk_level',
            size='cholesterol',
            hover_data=['patient_id', 'gender', 'diabetes'],
            title='实时患者风险分布',
            labels={'age': '年龄', 'systolic_bp': '收缩压 (mmHg)'},
            color_discrete_map={'低': 'green', '中': 'yellow', '高': 'red'},
            animation_frame='risk_level'
        ).update_layout(transition_duration=500)
    
    # 回调函数：更新治疗效果图
    @app.callback(
        Output('treatment-effect', 'figure'),
        [Input('treatment-update-interval', 'n_intervals')]
    )
    def update_treatment_effect(n):
        return px.sunburst(
            df,
            path=['treatment', 'treatment_response', 'risk_level'],
            title='实时治疗方案效果分析',
            color='risk_level',
            color_discrete_map={'低': 'green', '中': 'yellow', '高': 'red'}
        ).update_layout(transition_duration=500)
    
    # 回调函数：更新生命体征监测
    @app.callback(
        Output('vitals-monitor', 'figure'),
        [Input('vitals-update-interval', 'n_intervals'),
         Input('patient-selector', 'value')]
    )
    def update_vitals(n, patient_index):
        # 添加新的测量值
        app.real_time_data.append({
            'timestamp': datetime.now(),
            'systolic_bp': random.randint(90, 180),
            'heart_rate': random.randint(60, 100)
        })
        
        df_vitals = pd.DataFrame(app.real_time_data)
        
        return {
            'data': [
                go.Scatter(
                    x=df_vitals['timestamp'],
                    y=df_vitals['systolic_bp'],
                    name='收缩压',
                    line=dict(color='red')
                ),
                go.Scatter(
                    x=df_vitals['timestamp'],
                    y=df_vitals['heart_rate'],
                    name='心率',
                    line=dict(color='blue')
                )
            ],
            'layout': go.Layout(
                title=f'患者 {df.iloc[patient_index]["patient_id"]} 实时监测数据',
                xaxis=dict(title='时间'),
                yaxis=dict(title='测量值'),
                hovermode='x unified',
                transition_duration=500
            )
        }
    
    # 回调函数：更新治疗评估
    @app.callback(
        Output('treatment-evaluation', 'figure'),
        [Input('evaluation-update-interval', 'n_intervals')]
    )
    def update_treatment_evaluation(n):
        return px.bar(
            df.groupby(['treatment', 'treatment_response']).size().reset_index(name='count'),
            x='treatment',
            y='count',
            color='treatment_response',
            title='实时治疗效果评估',
            barmode='group',
            animation_frame='treatment_response'
        ).update_layout(
            transition_duration=500,
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [{
                    'label': '播放',
                    'method': 'animate',
                    'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}]
                }]
            }]
        )
    
    return app

def save_data(data, filename='data.json'):
    """将数据保存为JSON文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(filename='data.json'):
    """从JSON文件加载数据"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def perform_clustering(df):
    """执行K-means聚类分析"""
    features = ['age', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'cholesterol', 'bmi', 'exercise_hours']
    X = df[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    
    return df

def main():
    """主函数"""
    # 生成初始数据
    data = generate_patient_data()
    
    # 保存数据
    save_data(data)
    
    # 加载数据到DataFrame
    df = pd.DataFrame(data)
    
    # 执行聚类分析
    df = perform_clustering(df)
    
    # 创建并运行仪表板
    app = create_dashboard(df)
    app.run_server(debug=True)

if __name__ == '__main__':
    main() 