import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// const myCustomLightTheme = {
//   dark: false,
//   colors: {
//     primary: '#1867C0',
//     secondary: '#5CBBF6',
//   }
// }

const vuetify = createVuetify({
    components,
    directives,
})

export default vuetify