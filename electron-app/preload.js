const { contextBridge, ipcRenderer } = require('electron')

// Безопасный API для renderer процесса
contextBridge.exposeInMainWorld('electronAPI', {
  // Информация о приложении
  getAppInfo: () => ({
    version: require('./package.json').version,
    platform: process.platform,
    isDev: process.env.NODE_ENV === 'development',
    ports: {
      vite: 5173,
      fastapi: 8001,
      ml: 8002
    }
  }),
  
  // Docker управление
  startDockerServices: () => ipcRenderer.invoke('start-docker-services'),
  stopDockerServices: () => ipcRenderer.invoke('stop-docker-services'),
  checkServices: () => ipcRenderer.invoke('check-services'),
  
  // Системные функции
  openExternal: (url) => ipcRenderer.invoke('open-external', url),
  showNotification: (title, body) => ipcRenderer.invoke('show-notification', { title, body }),
  
  // Файловая система
  selectDirectory: () => ipcRenderer.invoke('select-directory'),
  
  // Логирование
  log: (level, message) => ipcRenderer.invoke('log', { level, message })
})
