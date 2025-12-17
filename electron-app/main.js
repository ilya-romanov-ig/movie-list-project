const { app, BrowserWindow, Menu, session, dialog } = require('electron')
const path = require('path')
const { exec } = require('child_process')
const net = require('net')

// Конфигурация портов из вашего docker-compose
const PORTS_CONFIG = {
  vite: 5173,      // Vue/Vite dev сервер
  fastapi: 8001,   // FastAPI бэкенд
  ml: 8002,        // ML сервис
  postgres: 5432   // PostgreSQL
}

let mainWindow

// Проверка доступности порта
function checkPort(port) {
  return new Promise((resolve) => {
    const socket = new net.Socket()
    socket.setTimeout(1500)
    
    socket.on('connect', () => {
      socket.destroy()
      resolve({ port, status: 'running', available: true })
    })
    
    socket.on('timeout', () => {
      socket.destroy()
      resolve({ port, status: 'timeout', available: false })
    })
    
    socket.on('error', () => {
      resolve({ port, status: 'error', available: false })
    })
    
    socket.connect(port, '127.0.0.1')
  })
}

// Проверка всех необходимых сервисов
async function checkAllServices() {
  const results = await Promise.all([
    checkPort(PORTS_CONFIG.vite),
    checkPort(PORTS_CONFIG.fastapi),
    checkPort(PORTS_CONFIG.ml)
  ])
  
  return {
    vite: results[0],
    fastapi: results[1],
    ml: results[2]
  }
}

// Создание окна приложения
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1600,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    icon: path.join(__dirname, 'assets/icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false, // Отключаем CORS для доступа к localhost
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    show: false,
    backgroundColor: '#1a1a1a',
    titleBarStyle: 'hiddenInset', // Для macOS
    frame: true
  })

  // Настройка CORS политик для Electron
  session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Access-Control-Allow-Origin': ['*'],
        'Access-Control-Allow-Methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        'Access-Control-Allow-Headers': ['Content-Type', 'Authorization', 'X-Requested-With'],
        'Access-Control-Allow-Credentials': ['true']
      }
    })
  })

  // Функция загрузки приложения
  async function loadApplication() {
    try {
      const services = await checkAllServices()
      
      if (!services.vite.available) {
        // Vite сервер не запущен, спрашиваем пользователя
        const { response } = await dialog.showMessageBox(mainWindow, {
          type: 'question',
          buttons: ['Запустить Docker', 'Выйти'],
          defaultId: 0,
          title: 'Vite сервер не найден',
          message: 'Vue dev сервер (порт 5173) не запущен.',
          detail: 'Хотите запустить Docker сервисы автоматически?'
        })
        
        if (response === 0) {
          await startDockerServices()
          // Ждем запуска сервисов
          await new Promise(resolve => setTimeout(resolve, 5000))
          mainWindow.loadURL(`http://localhost:${PORTS_CONFIG.vite}`)
        } else {
          app.quit()
        }
      } else {
        // Vite сервер запущен, загружаем приложение
        const viteUrl = `http://localhost:${PORTS_CONFIG.vite}`
        console.log('🚀 Загружаем Vue приложение:', viteUrl)
        mainWindow.loadURL(viteUrl)
        
        // Проверяем остальные сервисы
        if (!services.fastapi.available) {
          showServiceWarning('FastAPI бэкенд', PORTS_CONFIG.fastapi)
        }
        if (!services.ml.available) {
          showServiceWarning('ML сервис', PORTS_CONFIG.ml)
        }
      }
    } catch (error) {
      console.error('Ошибка при загрузке:', error)
      mainWindow.loadFile(path.join(__dirname, 'error.html'))
    }
  }

  // Запуск Docker сервисов
  async function startDockerServices() {
    return new Promise((resolve, reject) => {
      const dockerPath = path.join(__dirname, '../docker-services')
      
      exec(`cd "${dockerPath}" && docker-compose up -d frontend backend movie-recommender db`, 
        (error, stdout, stderr) => {
          if (error) {
            dialog.showErrorBox('Ошибка Docker', `Не удалось запустить Docker сервисы:\n${stderr}`)
            reject(error)
          } else {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Docker сервисы',
              message: 'Сервисы запускаются...',
              detail: 'Пожалуйста, подождите 10-15 секунд.'
            })
            resolve()
          }
        }
      )
    })
  }

  // Показать предупреждение о сервисе
  function showServiceWarning(serviceName, port) {
    mainWindow.webContents.executeJavaScript(`
      if (!window.serviceWarnings) {
        window.serviceWarnings = []
      }
      window.serviceWarnings.push('${serviceName} (порт ${port})')
      
      // Показываем уведомление
      const notification = new Notification('Внимание', {
        body: '${serviceName} недоступен. Некоторые функции могут не работать.',
        icon: 'assets/icon.png'
      })
      
      // Добавляем в UI
      if (document.getElementById('service-warnings')) {
        const div = document.createElement('div');
        div.className = 'service-warning';
        div.textContent = '⚠️ ${serviceName} (порт ${port}) недоступен';
        document.getElementById('service-warnings').appendChild(div);
      }
    `)
  }

  // События окна
  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
    
    // DevTools только в режиме разработки
    if (process.env.NODE_ENV === 'development') {
      mainWindow.webContents.openDevTools({ mode: 'detach' })
    }
    
    // Загружаем приложение после показа окна
    setTimeout(loadApplication, 100)
  })

  mainWindow.on('closed', () => {
    mainWindow = null
  })

  // Показываем окно загрузки
  mainWindow.loadFile(path.join(__dirname, 'loading.html'))

  // Создаем меню
  createMenu()
}

// Создание меню приложения
function createMenu() {
  const template = [
    {
      label: 'Приложение',
      submenu: [
        {
          label: 'Перезагрузить',
          accelerator: 'CmdOrCtrl+R',
          click: () => mainWindow.reload()
        },
        {
          label: 'Перезагрузить полностью',
          accelerator: 'CmdOrCtrl+Shift+R',
          click: () => {
            mainWindow.webContents.reloadIgnoringCache()
          }
        },
        { type: 'separator' },
        {
          label: 'Управление Docker',
          submenu: [
            {
              label: 'Запустить все сервисы',
              click: async () => {
                await startDockerServices()
                mainWindow.reload()
              }
            },
            {
              label: 'Остановить все сервисы',
              click: () => {
                const dockerPath = path.join(__dirname, '../docker-services')
                exec(`cd "${dockerPath}" && docker-compose down`, (error) => {
                  if (error) console.error('Ошибка остановки Docker:', error)
                })
              }
            },
            {
              label: 'Перезапустить бэкенд',
              click: () => {
                const dockerPath = path.join(__dirname, '../docker-services')
                exec(`cd "${dockerPath}" && docker-compose restart backend`, (error) => {
                  if (error) console.error('Ошибка:', error)
                })
              }
            }
          ]
        },
        { type: 'separator' },
        { role: 'quit' }
      ]
    },
    {
      label: 'Вид',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Сервисы',
      submenu: [
        {
          label: 'Проверить соединение',
          click: async () => {
            const services = await checkAllServices()
            
            let message = 'Статус сервисов:\n\n'
            message += `• Vue (Vite): ${services.vite.available ? '✅' : '❌'} порт ${PORTS_CONFIG.vite}\n`
            message += `• FastAPI: ${services.fastapi.available ? '✅' : '❌'} порт ${PORTS_CONFIG.fastapi}\n`
            message += `• ML сервис: ${services.ml.available ? '✅' : '❌'} порт ${PORTS_CONFIG.ml}`
            
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Статус сервисов',
              message: message
            })
          }
        },
        {
          label: 'Открыть API документацию',
          click: () => {
            const { shell } = require('electron')
            shell.openExternal(`http://localhost:${PORTS_CONFIG.fastapi}/docs`)
          }
        },
        {
          label: 'Открыть Vite сервер',
          click: () => {
            const { shell } = require('electron')
            shell.openExternal(`http://localhost:${PORTS_CONFIG.vite}`)
          }
        }
      ]
    },
    {
      label: 'Помощь',
      submenu: [
        {
          label: 'Порты приложения',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Порты приложения',
              message: 'Конфигурация портов:',
              detail: `Vue/Vite dev сервер: порт ${PORTS_CONFIG.vite}\nFastAPI бэкенд: порт ${PORTS_CONFIG.fastapi}\nML сервис: порт ${PORTS_CONFIG.ml}\nPostgreSQL: порт ${PORTS_CONFIG.postgres}`
            })
          }
        },
        {
          label: 'Docker команды',
          click: () => {
            const commands = `# Запуск всех сервисов
cd docker-services
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f backend
docker-compose logs -f frontend

# Пересборка
docker-compose build --no-cache`

            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Полезные Docker команды',
              message: commands,
              buttons: ['OK', 'Скопировать'],
              defaultId: 0
            }).then(({ response }) => {
              if (response === 1) {
                require('electron').clipboard.writeText(commands)
              }
            })
          }
        }
      ]
    }
  ]

  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)
}

// Инициализация приложения
app.whenReady().then(() => {
  console.log('🚀 Electron приложение запускается...')
  console.log('📊 Порты конфигурации:', PORTS_CONFIG)
  
  createWindow()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', () => {
  if (mainWindow === null) createWindow()
})

// Глобальные обработчики
process.on('uncaughtException', (error) => {
  console.error('Необработанная ошибка:', error)
  dialog.showErrorBox('Ошибка приложения', error.message)
})