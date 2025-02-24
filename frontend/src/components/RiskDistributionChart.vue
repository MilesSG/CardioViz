<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>患者风险分布</span>
        <el-button size="small" @click="resetZoom">重置</el-button>
      </div>
    </template>
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
    </div>
    <div v-else-if="error" class="error-container">
      {{ error }}
    </div>
    <v-chart
      v-else
      ref="chartRef"
      class="chart"
      :option="chartOption"
      :autoresize="true"
      @click="handlePointClick"
    />
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts/core'
import { usePatientStore } from '../stores/patient'
import { storeToRefs } from 'pinia'

const patientStore = usePatientStore()
const { patients } = storeToRefs(patientStore)
const chartRef = ref(null)
const loading = ref(true)
const error = ref(null)
let updateTimer = null

const processData = (data) => {
  if (!data || !Array.isArray(data)) {
    console.error('Invalid data:', data)
    return []
  }
  console.log('Processing data:', data)
  return data.map(p => {
    console.log('Processing patient:', p)
    return {
      ...p,
      value: [p.age || 0, p.systolic_bp || 0],
      symbolSize: Math.sqrt((p.cholesterol || 0) / 3)
    }
  })
}

const chartOption = computed(() => {
  return {
    title: {
      text: '患者风险分布图',
      subtext: '基于年龄和收缩压的风险分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        const data = params.data;
        return `
          <div style="padding: 8px">
            <div style="font-weight: bold; margin-bottom: 5px">患者信息</div>
            <div>ID: ${data.id}</div>
            <div>年龄: ${data.age}岁</div>
            <div>收缩压: ${data.systolic}mmHg</div>
            <div>舒张压: ${data.diastolic}mmHg</div>
            <div>心率: ${data.heartRate}次/分</div>
            <div>胆固醇: ${data.cholesterol}mg/dL</div>
            <div style="margin-top: 5px">风险等级: ${data.riskLevel}</div>
          </div>
        `;
      }
    },
    legend: {
      data: ['低风险', '中风险', '高风险'],
      top: 30,
      itemWidth: 14,
      itemHeight: 14,
      textStyle: {
        fontSize: 12
      }
    },
    grid: {
      left: '10%',
      right: '10%',
      top: 80,
      bottom: '12%'
    },
    xAxis: {
      type: 'value',
      name: '年龄',
      nameLocation: 'center',
      nameGap: 30,
      min: 18,
      max: 90,
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '收缩压 (mmHg)',
      nameLocation: 'center',
      nameGap: 45,
      min: 80,
      max: 200,
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: [
      {
        name: '低风险',
        type: 'scatter',
        itemStyle: {
          color: '#91cc75',
          opacity: 0.7
        },
        symbolSize: function(data) {
          return Math.sqrt(data[2]) * 3;  // 根据胆固醇值调整点的大小
        },
        data: patients.value
          .filter(p => p.risk_level === '低风险')
          .map(p => ({
            value: [p.age, p.systolic_bp, p.cholesterol],
            id: p.patient_id,
            age: p.age,
            systolic: p.systolic_bp,
            diastolic: p.diastolic_bp,
            heartRate: p.heart_rate,
            cholesterol: p.cholesterol,
            riskLevel: p.risk_level
          }))
      },
      {
        name: '中风险',
        type: 'scatter',
        itemStyle: {
          color: '#fac858',
          opacity: 0.7
        },
        symbolSize: function(data) {
          return Math.sqrt(data[2]) * 3;
        },
        data: patients.value
          .filter(p => p.risk_level === '中风险')
          .map(p => ({
            value: [p.age, p.systolic_bp, p.cholesterol],
            id: p.patient_id,
            age: p.age,
            systolic: p.systolic_bp,
            diastolic: p.diastolic_bp,
            heartRate: p.heart_rate,
            cholesterol: p.cholesterol,
            riskLevel: p.risk_level
          }))
      },
      {
        name: '高风险',
        type: 'scatter',
        itemStyle: {
          color: '#ee6666',
          opacity: 0.7
        },
        symbolSize: function(data) {
          return Math.sqrt(data[2]) * 3;
        },
        data: patients.value
          .filter(p => p.risk_level === '高风险')
          .map(p => ({
            value: [p.age, p.systolic_bp, p.cholesterol],
            id: p.patient_id,
            age: p.age,
            systolic: p.systolic_bp,
            diastolic: p.diastolic_bp,
            heartRate: p.heart_rate,
            cholesterol: p.cholesterol,
            riskLevel: p.risk_level
          }))
      }
    ]
  };
})

const resetZoom = () => {
  if (chartRef.value) {
    chartRef.value.setOption({
      xAxis: { min: 0, max: 100 },
      yAxis: { min: 80, max: 200 }
    })
  }
}

const handlePointClick = (params) => {
  if (params.data) {
    patientStore.setSelectedPatient(params.data)
  }
}

const updateData = async () => {
  try {
    loading.value = true
    error.value = null
    console.log('Fetching patient data...')
    await patientStore.fetchPatients()
    console.log('Patient data fetched:', patientStore.patients)
  } catch (err) {
    error.value = '获取数据失败：' + err.message
    console.error('Error updating data:', err)
  } finally {
    loading.value = false
  }
}

watch(patients, (newVal) => {
  console.log('Patients data updated:', newVal)
}, { deep: true })

onMounted(async () => {
  console.log('Component mounted')
  await updateData()
  console.log('Initial data update completed')
  updateTimer = setInterval(updateData, 2000)
})

onUnmounted(() => {
  if (updateTimer) {
    clearInterval(updateTimer)
  }
})
</script>

<style scoped>
.chart {
  height: 400px;
  background: linear-gradient(135deg, #f5f7fa 0%, #f8f9fb 100%);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loading-container {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #409EFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #F56C6C;
}
</style> 