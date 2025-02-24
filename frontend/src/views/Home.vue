<!-- Home.vue -->
<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <h1>CardioViz - 心血管疾病数据分析与可视化</h1>
    </el-header>
    
    <el-main class="app-main">
      <el-row :gutter="20" class="mb-4">
        <el-col :span="8">
          <el-card class="stat-card" :body-style="{ padding: '20px' }">
            <template #header>
              <div class="card-header">
                <span>总患者数</span>
              </div>
            </template>
            <div class="stat-value primary">{{ stats.totalPatients }}</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="stat-card" :body-style="{ padding: '20px' }">
            <template #header>
              <div class="card-header">
                <span>高风险患者</span>
              </div>
            </template>
            <div class="stat-value danger">{{ stats.highRiskPatients }}</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="stat-card" :body-style="{ padding: '20px' }">
            <template #header>
              <div class="card-header">
                <span>高风险比例</span>
              </div>
            </template>
            <div class="stat-value warning">{{ stats.highRiskPercentage }}%</div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mb-4">
        <el-col :span="24">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>数据更新控制</span>
              </div>
            </template>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-switch
                  v-model="autoUpdate"
                  active-text="自动更新"
                  inactive-text="手动更新"
                  @change="handleAutoUpdateChange"
                />
              </el-col>
              <el-col :span="12">
                <el-select
                  v-model="updateInterval"
                  placeholder="更新频率"
                  :disabled="!autoUpdate"
                  @change="handleIntervalChange"
                >
                  <el-option label="快速 (1秒)" value="1000" />
                  <el-option label="正常 (2秒)" value="2000" />
                  <el-option label="慢速 (5秒)" value="5000" />
                </el-select>
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mb-4">
        <el-col :span="12">
          <risk-distribution-chart />
        </el-col>
        <el-col :span="12">
          <treatment-effect-chart />
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mb-4">
        <el-col :span="12">
          <network-analysis-chart />
        </el-col>
        <el-col :span="12">
          <vitals-monitor-chart />
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="24">
          <treatment-evaluation-chart />
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { usePatientStore } from '../stores/patient'
import { storeToRefs } from 'pinia'
import RiskDistributionChart from '../components/RiskDistributionChart.vue'
import TreatmentEffectChart from '../components/TreatmentEffectChart.vue'
import NetworkAnalysisChart from '../components/NetworkAnalysisChart.vue'
import VitalsMonitorChart from '../components/VitalsMonitorChart.vue'
import TreatmentEvaluationChart from '../components/TreatmentEvaluationChart.vue'

const patientStore = usePatientStore()
const { stats } = storeToRefs(patientStore)
const autoUpdate = ref(true)
const updateInterval = ref('2000')
let updateTimer = null

const startAutoUpdate = () => {
  if (updateTimer) {
    clearInterval(updateTimer)
  }
  updateTimer = setInterval(async () => {
    await updateAllData()
  }, parseInt(updateInterval.value))
}

const stopAutoUpdate = () => {
  if (updateTimer) {
    clearInterval(updateTimer)
    updateTimer = null
  }
}

const handleAutoUpdateChange = (value) => {
  if (value) {
    startAutoUpdate()
  } else {
    stopAutoUpdate()
  }
}

const handleIntervalChange = () => {
  if (autoUpdate.value) {
    startAutoUpdate()
  }
}

const updateAllData = async () => {
  try {
    console.log('Updating all data...')
    await Promise.all([
      patientStore.fetchStats(),
      patientStore.fetchPatients(),
      patientStore.fetchTreatmentAnalysis()
    ])
  } catch (error) {
    console.error('Error updating data:', error)
  }
}

onMounted(async () => {
  await updateAllData()
  if (autoUpdate.value) {
    startAutoUpdate()
  }
})

onUnmounted(() => {
  stopAutoUpdate()
})
</script>

<style lang="scss">
.app-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.app-header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
  h1 {
    margin: 0;
    line-height: 60px;
    text-align: center;
    color: #409EFF;
  }
}

.app-main {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 20px;
}

.stat-card {
  .stat-value {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    
    &.primary { color: #409EFF; }
    &.danger { color: #F56C6C; }
    &.warning { color: #E6A23C; }
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 