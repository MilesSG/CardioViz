import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import App from './App.vue'

// Import ECharts
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import {
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  GraphChart,
  SunburstChart
} from 'echarts/charts'
import {
  TitleComponent,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  ToolboxComponent,
  DatasetComponent
} from 'echarts/components'

// Register ECharts components
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  GraphChart,
  SunburstChart,
  TitleComponent,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  ToolboxComponent,
  DatasetComponent
])

const app = createApp(App)

// Register global components
app.component('v-chart', ECharts)

// Use plugins
app.use(createPinia())
app.use(ElementPlus)
app.use(router)

// Mount app
app.mount('#app') 