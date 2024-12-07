import 'htmx.org'
import { themeChange } from 'theme-change'
import '@fortawesome/fontawesome-free/css/all.min.css'
import 'vite/modulepreload-polyfill'
import './css/style.css'
import Chart from 'chart.js/auto'

themeChange(false)

window.Chart = Chart
