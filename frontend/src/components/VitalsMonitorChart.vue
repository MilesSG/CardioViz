<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>实时生命体征监测</span>
        <div class="controls">
          <el-select
            v-model="selectedPatientId"
            placeholder="选择患者"
            size="small"
            style="width: 150px; margin-right: 10px"
          >
            <el-option
              v-for="patient in patients"
              :key="patient.patient_id"
              :label="patient.patient_id"
              :value="patient.patient_id"
            />
          </el-select>
          <el-switch
            v-model="isRealtime"
            active-text="实时监测"
            inactive-text="历史数据"
            size="small"
          />
        </div>
      </div>
    </template>
    <div class="chart-container">
      <v-chart
        class="chart"
        :option="chartOption"
        :autoresize="true"
      />
      <div class="vital-cards">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '10px' }">
              <div class="vital-info">
                <div class="vital-label">收缩压</div>
                <div class="vital-value" :class="getBPClass(currentVitals.systolic_bp)">
                  {{ currentVitals.systolic_bp }} <span class="unit">mmHg</span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '10px' }">
              <div class="vital-info">
                <div class="vital-label">心率</div>
                <div class="vital-value" :class="getHRClass(currentVitals.heart_rate)">
                  {{ currentVitals.heart_rate }} <span class="unit">bpm</span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '10px' }">
              <div class="vital-info">
                <div class="vital-label">状态</div>
                <div class="vital-value" :class="getStatusClass()">
                  {{ getStatusText() }}
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  ToolboxComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { usePatientStore } from '../stores/patient'
import { storeToRefs } from 'pinia'
import dayjs from 'dayjs'

use([
  CanvasRenderer,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  ToolboxComponent
])

const patientStore = usePatientStore()
const { patients } = storeToRefs(patientStore)
const selectedPatientId = ref('')
const isRealtime = ref(true)
const vitalsData = ref({
  times: [],
  systolic_bp: [],
  heart_rate: []
})
const currentVitals = ref({
  systolic_bp: 0,
  heart_rate: 0
})
let updateTimer = null

const chartOption = computed(() => ({
  animation: true,
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
  legend: {
    data: ['收缩压', '心率']
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      restore: {},
      saveAsImage: {}
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: vitalsData.value.times,
    axisLabel: {
      formatter: (value) => dayjs(value).format('HH:mm:ss')
    }
  },
  yAxis: [
    {
      name: '收缩压 (mmHg)',
      type: 'value',
      position: 'left'
    },
    {
      name: '心率 (bpm)',
      type: 'value',
      position: 'right'
    }
  ],
  series: [
    {
      name: '收缩压',
      type: 'line',
      yAxisIndex: 0,
      data: vitalsData.value.systolic_bp,
      itemStyle: {
        color: '#F56C6C'
      },
      lineStyle: {
        width: 2
      },
      showSymbol: false,
      emphasis: {
        focus: 'series'
      }
    },
    {
      name: '心率',
      type: 'line',
      yAxisIndex: 1,
      data: vitalsData.value.heart_rate,
      itemStyle: {
        color: '#409EFF'
      },
      lineStyle: {
        width: 2
      },
      showSymbol: false,
      emphasis: {
        focus: 'series'
      }
    }
  ]
}))

const initializePatient = async () => {
  if (patients.value && patients.value.length > 0 && !selectedPatientId.value) {
    selectedPatientId.value = patients.value[0].patient_id
    await updateVitals()
  }
}

const updateVitals = async () => {
  if (!selectedPatientId.value) {
    console.log('No patient selected')
    return
  }
  
  try {
    console.log('Fetching vitals for patient:', selectedPatientId.value)
    const data = await patientStore.fetchPatientVitals(selectedPatientId.value)
    console.log('Received vitals data:', data)
    
    if (data && data.times && data.systolic_bp && data.heart_rate) {
      vitalsData.value = {
        times: data.times.map(t => dayjs().format('YYYY-MM-DD ') + t),
        systolic_bp: data.systolic_bp,
        heart_rate: data.heart_rate
      }
      
      if (data.systolic_bp.length > 0 && data.heart_rate.length > 0) {
        currentVitals.value = {
          systolic_bp: data.systolic_bp[data.systolic_bp.length - 1],
          heart_rate: data.heart_rate[data.heart_rate.length - 1]
        }
      }
    }
  } catch (error) {
    console.error('Error updating vitals:', error)
  }
}

const getBPClass = (value) => {
  if (value > 140) return 'danger'
  if (value > 120) return 'warning'
  return 'normal'
}

const getHRClass = (value) => {
  if (value > 100 || value < 60) return 'danger'
  if (value > 90 || value < 65) return 'warning'
  return 'normal'
}

const getStatusClass = () => {
  const bpStatus = getBPClass(currentVitals.value.systolic_bp)
  const hrStatus = getHRClass(currentVitals.value.heart_rate)
  return bpStatus === 'danger' || hrStatus === 'danger' ? 'danger' :
         bpStatus === 'warning' || hrStatus === 'warning' ? 'warning' : 'normal'
}

const getStatusText = () => {
  const statusClass = getStatusClass()
  return statusClass === 'danger' ? '需要关注' :
         statusClass === 'warning' ? '需要监测' : '状态正常'
}

watch(selectedPatientId, (newId) => {
  console.log('Selected patient changed:', newId)
  if (newId) {
    updateVitals()
  }
})

watch(isRealtime, (newValue) => {
  console.log('Realtime mode changed:', newValue)
  if (newValue && selectedPatientId.value) {
    updateVitals()
  }
})

watch(patients, async (newPatients) => {
  if (newPatients && newPatients.length > 0) {
    await initializePatient()
  }
})

onMounted(async () => {
  console.log('Vitals monitor component mounted')
  await patientStore.fetchPatients()
  await initializePatient()
  updateTimer = setInterval(async () => {
    if (isRealtime.value) {
      await updateVitals()
    }
  }, 2000)
})

onUnmounted(() => {
  console.log('Vitals monitor component unmounted')
  if (updateTimer) {
    clearInterval(updateTimer)
  }
})
</script>

<style scoped lang="scss">
.chart-container {
  position: relative;
}

.chart {
  height: 300px;
}

.vital-cards {
  margin-top: 20px;
}

.vital-info {
  text-align: center;
  
  .vital-label {
    font-size: 14px;
    color: #909399;
    margin-bottom: 5px;
  }
  
  .vital-value {
    font-size: 24px;
    font-weight: bold;
    
    &.normal { color: #67C23A; }
    &.warning { color: #E6A23C; }
    &.danger { color: #F56C6C; }
    
    .unit {
      font-size: 12px;
      color: #909399;
    }
  }
}

.controls {
  display: flex;
  align-items: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 