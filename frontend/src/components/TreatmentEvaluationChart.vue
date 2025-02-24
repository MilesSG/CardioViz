<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>治疗效果实时评估</span>
        <el-button-group>
          <el-button size="small" @click="toggleAnimation">
            {{ isAnimating ? '暂停' : '播放' }}
          </el-button>
          <el-button size="small" @click="switchView">
            {{ currentView === 'treatment' ? '按风险等级' : '按治疗方案' }}
          </el-button>
        </el-button-group>
      </div>
    </template>
    <v-chart
      class="chart"
      :option="chartOption"
      :autoresize="true"
    />
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { usePatientStore } from '../stores/patient'
import { storeToRefs } from 'pinia'

use([
  CanvasRenderer,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent
])

const patientStore = usePatientStore()
const { patients } = storeToRefs(patientStore)
const isAnimating = ref(false)
const currentView = ref('treatment')
let animationTimer = null

const processData = (data) => {
  const result = {
    treatment: {},
    risk: {}
  }
  
  data.forEach(patient => {
    // 按治疗方案统计
    if (!result.treatment[patient.treatment]) {
      result.treatment[patient.treatment] = {
        '显著改善': 0,
        '部分改善': 0,
        '无明显改善': 0
      }
    }
    result.treatment[patient.treatment][patient.treatment_response]++
    
    // 按风险等级统计
    if (!result.risk[patient.risk_level]) {
      result.risk[patient.risk_level] = {
        '显著改善': 0,
        '部分改善': 0,
        '无明显改善': 0
      }
    }
    result.risk[patient.risk_level][patient.treatment_response]++
  })
  
  return result
}

const chartOption = computed(() => {
  const data = processData(patients.value)
  const currentData = data[currentView.value === 'treatment' ? 'treatment' : 'risk']
  const categories = Object.keys(currentData)
  const responses = ['显著改善', '部分改善', '无明显改善']
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: responses
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        interval: 0,
        rotate: 30
      }
    },
    yAxis: {
      type: 'value',
      name: '患者数量'
    },
    series: responses.map(response => ({
      name: response,
      type: 'bar',
      stack: 'total',
      label: {
        show: true,
        position: 'inside'
      },
      emphasis: {
        focus: 'series'
      },
      data: categories.map(cat => currentData[cat][response]),
      itemStyle: {
        color: response === '显著改善' ? '#67C23A' :
               response === '部分改善' ? '#E6A23C' : '#F56C6C'
      }
    }))
  }
})

const toggleAnimation = () => {
  isAnimating.value = !isAnimating.value
}

const switchView = () => {
  currentView.value = currentView.value === 'treatment' ? 'risk' : 'treatment'
}

onMounted(async () => {
  if (patients.value.length === 0) {
    await patientStore.fetchPatients()
  }
})

watch(isAnimating, (newValue) => {
  if (newValue) {
    animationTimer = setInterval(async () => {
      await patientStore.fetchPatients()
    }, 2000)
  } else {
    if (animationTimer) {
      clearInterval(animationTimer)
    }
  }
})
</script>

<style scoped>
.chart {
  height: 400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 