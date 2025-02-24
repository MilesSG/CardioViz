<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>治疗效果分析</span>
        <el-button-group>
          <el-button size="small" @click="toggleAnimation">
            {{ isAnimating ? '暂停' : '播放' }}
          </el-button>
          <el-button size="small" @click="switchChartType">
            切换图表
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
import {
  SunburstChart,
  PieChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { usePatientStore } from '../stores/patient'
import { storeToRefs } from 'pinia'

use([
  CanvasRenderer,
  SunburstChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
])

const patientStore = usePatientStore()
const { treatmentAnalysis } = storeToRefs(patientStore)
const isAnimating = ref(false)
const chartType = ref('sunburst')
let animationTimer = null

const processData = (data) => {
  console.log('Processing treatment data:', data)
  if (!data || !data.data) {
    console.error('Invalid treatment data:', data)
    return []
  }
  
  if (chartType.value === 'sunburst') {
    console.log('Returning sunburst data:', data.data)
    return data.data.map(item => ({
      name: item.name,
      children: item.children.map(child => ({
        name: child.name,
        value: child.value
      }))
    }))
  } else {
    const pieData = data.data.map(treatment => ({
      name: treatment.name,
      value: treatment.children.reduce((sum, child) => sum + child.value, 0),
      itemStyle: {
        color: treatment.name === '标准药物治疗' ? '#409EFF' :
               treatment.name === '介入手术' ? '#67C23A' : '#E6A23C'
      }
    }))
    console.log('Returning pie data:', pieData)
    return pieData
  }
}

const chartOption = computed(() => {
  console.log('Updating chart with treatment analysis:', treatmentAnalysis.value)
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    series: [
      {
        type: chartType.value,
        data: processData(treatmentAnalysis.value),
        radius: chartType.value === 'pie' ? ['50%', '70%'] : ['0', '95%'],
        itemStyle: {
          borderRadius: 5,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {c}'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '14',
            fontWeight: 'bold'
          }
        },
        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: function (idx) {
          return Math.random() * 200
        }
      }
    ]
  }
})

const toggleAnimation = () => {
  isAnimating.value = !isAnimating.value
}

const switchChartType = () => {
  chartType.value = chartType.value === 'sunburst' ? 'pie' : 'sunburst'
}

onMounted(async () => {
  console.log('Treatment chart component mounted')
  await patientStore.fetchTreatmentAnalysis()
  console.log('Initial treatment data fetched')
})

watch(isAnimating, (newValue) => {
  if (newValue) {
    animationTimer = setInterval(async () => {
      await patientStore.fetchTreatmentAnalysis()
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