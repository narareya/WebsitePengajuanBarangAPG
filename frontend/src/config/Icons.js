import { h } from 'vue'

const icon = (paths) => (props) =>
  h(
    'svg',
    { ...props, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 1.8, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' },
    paths.map((d) => h('path', { d }))
  )

export const iconMap = {
    home: icon(['M3 12l9-9 9 9', 'M5 10v10a1 1 0 001 1h4v-6h4v6h4a1 1 0 001-1V10']),
    users: icon(['M17 20a4 4 0 00-8 0', 'M9 4a3 3 0 100 6 3 3 0 000-6z', 'M20 20a4 4 0 00-3-3.87', 'M17 4a3 3 0 010 6']),
    folder: icon(['M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V7z']),
    calendar: icon(['M8 2v4', 'M16 2v4', 'M3 9h18', 'M4 5h16a1 1 0 011 1v13a1 1 0 01-1 1H4a1 1 0 01-1-1V6a1 1 0 011-1z']),
    document: icon(['M14 2H6a1 1 0 00-1 1v18a1 1 0 001 1h12a1 1 0 001-1V7z', 'M14 2v5h5']),
    chart: icon(['M12 2a10 10 0 100 20 10 10 0 000-20z', 'M12 2v10l7 4']),
    'check-circle': icon(['M22 11.08V12a10 10 0 11-5.93-9.14', 'M22 4L12 14.01l-3-3']),
    box: icon(['M21 8L12 3 3 8l9 5 9-5z', 'M3 8v8l9 5 9-5V8', 'M12 13v8']),
  }