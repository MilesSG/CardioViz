from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json

app = Flask(__name__)
CORS(app)

def generate_patient_data(n_patients=1000):
    """生成模拟患者数据"""
    np.random.seed(42)
    data = []
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    
    treatments = ['标准药物治疗', '介入手术', '生活方式干预']
    symptoms = ['胸痛', '气短', '心悸', '头晕', '疲劳']
    medications = ['阿司匹林', '他汀类药物', 'β受体阻滞剂', 'ACE抑制剂']
    
    # 定义年龄分布
    age_weights = np.array([0.1, 0.15, 0.25, 0.3, 0.2])  # 偏向中老年
    age_ranges = [(18, 30), (31, 45), (46, 60), (61, 75), (76, 90)]
    
    for i in range(n_patients):
        # 使用加权随机选择年龄范围
        age_range_idx = np.random.choice(len(age_ranges), p=age_weights)
        age_min, age_max = age_ranges[age_range_idx]
        age = random.randint(age_min, age_max)
        
        # 根据年龄调整其他指标的概率
        is_elderly = age > 60
        has_comorbidity = random.random() < (0.3 if is_elderly else 0.15)
        
        # 生成更真实的血压数据
        if is_elderly or has_comorbidity:
            systolic_bp = random.randint(130, 180)
            diastolic_bp = random.randint(80, 110)
        else:
            systolic_bp = random.randint(90, 140)
            diastolic_bp = random.randint(60, 90)
        
        # 生成更真实的心率数据
        if is_elderly:
            heart_rate = random.randint(60, 90)
        else:
            heart_rate = random.randint(60, 100)
        
        # 生成更真实的胆固醇数据
        if is_elderly or has_comorbidity:
            cholesterol = random.randint(180, 300)
        else:
            cholesterol = random.randint(150, 240)
        
        patient = {
            'patient_id': f'P{str(i+1).zfill(4)}',
            'age': age,
            'gender': random.choice(['男', '女']),
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'heart_rate': heart_rate,
            'cholesterol': cholesterol,
            'smoking': random.choice(['是', '否']),
            'diabetes': random.choice(['是', '否']) if random.random() < (0.25 if is_elderly else 0.1) else '否',
            'bmi': round(random.uniform(18.5, 35.0), 1),
            'exercise_hours': random.randint(0, 14),
            'visit_date': random.choice(dates).strftime('%Y-%m-%d'),
            'symptoms': random.sample(symptoms, random.randint(1, 3)),
            'treatment': random.choice(treatments),
            'medications': random.sample(medications, random.randint(1, 3)),
            'treatment_response': random.choice(['显著改善', '部分改善', '无明显改善']),
            'follow_up_visits': random.randint(1, 5)
        }
        
        # 改进的风险评分系统
        risk_score = 0
        
        # 年龄风险
        if age > 75: risk_score += 4
        elif age > 65: risk_score += 3
        elif age > 55: risk_score += 2
        elif age > 45: risk_score += 1
        
        # 血压风险
        if systolic_bp >= 180: risk_score += 4
        elif systolic_bp >= 160: risk_score += 3
        elif systolic_bp >= 140: risk_score += 2
        
        if diastolic_bp >= 110: risk_score += 3
        elif diastolic_bp >= 90: risk_score += 2
        
        # 心率风险
        if heart_rate > 100 or heart_rate < 50: risk_score += 2
        elif heart_rate > 90 or heart_rate < 60: risk_score += 1
        
        # 胆固醇风险
        if cholesterol >= 280: risk_score += 3
        elif cholesterol >= 240: risk_score += 2
        elif cholesterol >= 200: risk_score += 1
        
        # 其他风险因素
        if patient['smoking'] == '是': risk_score += 3
        if patient['diabetes'] == '是': risk_score += 3
        if patient['bmi'] >= 30: risk_score += 2
        elif patient['bmi'] >= 25: risk_score += 1
        if patient['exercise_hours'] < 2: risk_score += 2
        elif patient['exercise_hours'] < 5: risk_score += 1
        
        # 症状相关风险
        if '胸痛' in patient['symptoms']: risk_score += 3
        if len(patient['symptoms']) >= 3: risk_score += 2
        elif len(patient['symptoms']) >= 2: risk_score += 1
        
        # 根据总分确定风险等级
        if risk_score <= 5:
            patient['risk_level'] = '低风险'
        elif risk_score <= 12:
            patient['risk_level'] = '中风险'
        else:
            patient['risk_level'] = '高风险'
            
        data.append(patient)
    
    return data

# 全局数据存储
patients_data = generate_patient_data()

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计数据"""
    total = len(patients_data)
    high_risk = len([p for p in patients_data if p['risk_level'] == '高风险'])
    return jsonify({
        'total_patients': total,
        'high_risk_patients': high_risk,
        'high_risk_percentage': round((high_risk / total) * 100, 1)
    })

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """获取患者数据"""
    # 更新部分患者数据以模拟实时变化
    for i in range(random.randint(5, 10)):
        idx = random.randint(0, len(patients_data) - 1)
        patients_data[idx]['systolic_bp'] = random.randint(90, 180)
        patients_data[idx]['heart_rate'] = random.randint(60, 100)
        
        # 重新计算风险等级
        risk_score = 0
        if patients_data[idx]['age'] > 60: risk_score += 2
        if patients_data[idx]['systolic_bp'] > 140: risk_score += 2
        if patients_data[idx]['diastolic_bp'] > 90: risk_score += 1
        if patients_data[idx]['heart_rate'] > 90: risk_score += 1
        if patients_data[idx]['cholesterol'] > 200: risk_score += 2
        if patients_data[idx]['smoking'] == '是': risk_score += 2
        if patients_data[idx]['diabetes'] == '是': risk_score += 2
        if patients_data[idx]['bmi'] > 30: risk_score += 1
        if patients_data[idx]['exercise_hours'] < 3: risk_score += 1
        if len(patients_data[idx]['symptoms']) > 2: risk_score += 2
        
        if risk_score <= 4:
            patients_data[idx]['risk_level'] = '低风险'
        elif risk_score <= 8:
            patients_data[idx]['risk_level'] = '中风险'
        else:
            patients_data[idx]['risk_level'] = '高风险'
    
    return jsonify(patients_data)

@app.route('/api/patient/<patient_id>/vitals', methods=['GET'])
def get_patient_vitals(patient_id):
    """获取患者实时生命体征"""
    patient = next((p for p in patients_data if p['patient_id'] == patient_id), None)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # 生成最近6小时的模拟数据
    current_time = datetime.now()
    times = [(current_time - timedelta(minutes=i*10)).strftime('%H:%M') for i in range(6)]
    vitals = {
        'times': times,
        'systolic_bp': [
            random.randint(
                max(90, patient['systolic_bp'] - 20),
                min(180, patient['systolic_bp'] + 20)
            ) for _ in range(6)
        ],
        'heart_rate': [
            random.randint(
                max(60, patient['heart_rate'] - 10),
                min(100, patient['heart_rate'] + 10)
            ) for _ in range(6)
        ]
    }
    return jsonify(vitals)

@app.route('/api/treatments/analysis', methods=['GET'])
def get_treatment_analysis():
    """获取治疗效果分析"""
    analysis = {
        'treatments': {},
        'responses': ['显著改善', '部分改善', '无明显改善'],
        'data': []
    }
    
    # 统计每种治疗方案的效果
    for treatment in ['标准药物治疗', '介入手术', '生活方式干预']:
        treatment_data = {
            'name': treatment,
            'children': []
        }
        
        response_counts = {
            '显著改善': 0,
            '部分改善': 0,
            '无明显改善': 0
        }
        
        for patient in patients_data:
            if patient['treatment'] == treatment:
                response_counts[patient['treatment_response']] += 1
        
        for response, count in response_counts.items():
            treatment_data['children'].append({
                'name': response,
                'value': count
            })
        
        analysis['data'].append(treatment_data)
    
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 