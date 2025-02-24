<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>症状-治疗-药物关联网络</span>
        <el-button size="small" @click="resetLayout">重置布局</el-button>
      </div>
    </template>
    <v-chart
      ref="chartRef"
      class="chart"
      :option="chartOption"
      :autoresize="true"
    />
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { GraphChart } from 'echarts/charts'
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
  GraphChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
])

const patientStore = usePatientStore()
const { patients } = storeToRefs(patientStore)
const chartRef = ref(null)
let updateTimer = null

const processNetworkData = (data) => {
  if (!data || !Array.isArray(data)) {
    console.error('Invalid data:', data)
    return { nodes: [], edges: [], categories: [] }
  }

  const nodes = new Map()
  const edges = new Map()
  const categories = ['症状', '治疗', '药物']
  
  try {
    // 收集所有节点和边
    data.forEach(patient => {
      // 添加症状节点
      patient.symptoms.forEach(symptom => {
        if (!nodes.has(symptom)) {
          nodes.set(symptom, { 
            name: symptom, 
            category: 0, 
            value: 1,
            symbolSize: 30  // 固定大小
          })
        } else {
          nodes.get(symptom).value++
        }
      })
      
      // 添加治疗节点
      if (!nodes.has(patient.treatment)) {
        nodes.set(patient.treatment, { 
          name: patient.treatment, 
          category: 1, 
          value: 1,
          symbolSize: 40  // 治疗节点稍大
        })
      } else {
        nodes.get(patient.treatment).value++
      }
      
      // 添加药物节点
      patient.medications.forEach(med => {
        if (!nodes.has(med)) {
          nodes.set(med, { 
            name: med, 
            category: 2, 
            value: 1,
            symbolSize: 35  // 药物节点大小适中
          })
        } else {
          nodes.get(med).value++
        }
      })
      
      // 添加边
      patient.symptoms.forEach(symptom => {
        const edgeKey = `${symptom}-${patient.treatment}`
        if (!edges.has(edgeKey)) {
          edges.set(edgeKey, {
            source: symptom,
            target: patient.treatment,
            value: 1,
            lineStyle: {
              width: 1,
              curveness: 0.2
            }
          })
        } else {
          edges.get(edgeKey).value++
          edges.get(edgeKey).lineStyle.width = Math.min(edges.get(edgeKey).value / 2, 5)
        }
      })
      
      patient.medications.forEach(med => {
        const edgeKey = `${patient.treatment}-${med}`
        if (!edges.has(edgeKey)) {
          edges.set(edgeKey, {
            source: patient.treatment,
            target: med,
            value: 1,
            lineStyle: {
              width: 1,
              curveness: 0.2
            }
          })
        } else {
          edges.get(edgeKey).value++
          edges.get(edgeKey).lineStyle.width = Math.min(edges.get(edgeKey).value / 2, 5)
        }
      })
    })
    
    console.log('Processed network data:', {
      nodes: Array.from(nodes.values()),
      edges: Array.from(edges.values())
    })
    
    return {
      nodes: Array.from(nodes.values()),
      edges: Array.from(edges.values()),
      categories: categories.map(name => ({ name }))
    }
  } catch (error) {
    console.error('Error processing network data:', error)
    return { nodes: [], edges: [], categories: [] }
  }
}

const chartOption = computed(() => {
  console.log('Updating network chart with patients:', patients.value)
  const { nodes, edges, categories } = processNetworkData(patients.value)
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        if (params.dataType === 'node') {
          return `${params.data.name}<br/>出现次数: ${params.data.value}`
        } else {
          return `${params.data.source} -> ${params.data.target}<br/>关联次数: ${params.data.value}`
        }
      }
    },
    legend: [{
      data: categories.map(cat => cat.name),
      selected: categories.reduce((acc, cat) => {
        acc[cat.name] = true
        return acc
      }, {})
    }],
    animationDurationUpdate: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [{
      type: 'graph',
      layout: 'force',
      data: nodes,
      links: edges,
      categories: categories,
      roam: true,
      draggable: true,
      label: {
        show: true,
        position: 'right',
        formatter: '{b}'
      },
      force: {
        repulsion: 100,
        gravity: 0.1,
        edgeLength: 100,
        layoutAnimation: true
      },
      itemStyle: {
        borderColor: '#fff',
        borderWidth: 1,
        shadowBlur: 10,
        shadowColor: 'rgba(0, 0, 0, 0.3)'
      },
      lineStyle: {
        color: 'source',
        curveness: 0.2
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: {
          width: 5
        }
      }
    }]
  }
})

const resetLayout = () => {
  if (chartRef.value) {
    const option = chartOption.value
    option.series[0].force = {
      repulsion: 100,
      gravity: 0.1,
      edgeLength: 100,
      layoutAnimation: true
    }
    chartRef.value.setOption(option)
  }
}

onMounted(async () => {
  if (patients.value.length === 0) {
    await patientStore.fetchPatients()
  }
  updateTimer = setInterval(async () => {
    await patientStore.fetchPatients()
  }, 2000)
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
</style> 