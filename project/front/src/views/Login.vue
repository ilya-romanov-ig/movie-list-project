<template>
  <PageWrapper>
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card elevation="4" class="pa-6 rounded-lg">
          <div class="text-center mb-6">
            <v-icon color="green-darken-3" size="64" class="mb-2">
              mdi-login
            </v-icon>
            <h1 class="text-h4 font-weight-bold mb-2 text-white">Вход в систему</h1>
            <p class="text-body-1 text-grey">Введите свои данные для входа</p>
          </div>

          <v-form @submit.prevent="handleLogin">
            <v-text-field
              v-model="email"
              label="Email"
              type="email"
              variant="outlined"
              prepend-inner-icon="mdi-email"
              :rules="emailRules"
              :error-messages="error"
              class="mb-4"
              required
              autofocus
              bg-color="grey-darken-3"
            />

            <v-text-field
              v-model="password"
              label="Пароль"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
              prepend-inner-icon="mdi-lock"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              :rules="passwordRules"
              required
              @click:append-inner="showPassword = !showPassword"
              class="mb-2"
              bg-color="grey-darken-3"
            />

            <div class="d-flex justify-space-between align-center mb-6">
              <v-checkbox
                v-model="rememberMe"
                label="Запомнить меня"
                density="compact"
                hide-details
                color="green-darken-3"
              />
              
              <a href="#" class="text-green-darken-3 text-decoration-none">
                Забыли пароль?
              </a>
            </div>

            <v-btn
              type="submit"
              color="green-darken-3"
              size="large"
              block
              :loading="loading"
              class="mb-4"
            >
              <v-icon start>mdi-login</v-icon>
              Войти
            </v-btn>

            <div class="text-center">
              <span class="text-grey mr-2">Нет аккаунта?</span>
              <router-link 
                to="/register" 
                class="text-green-darken-3 font-weight-bold text-decoration-none"
              >
                Зарегистрироваться
              </router-link>
            </div>

            <v-divider class="my-6" color="grey-darken-2" />

            <div class="text-center">
              <p class="text-grey mb-4">Или войдите через</p>
              <div class="d-flex justify-center gap-3">
                <v-btn
                  icon
                  variant="outlined"
                  size="large"
                  color="grey-lighten-1"
                  @click="loginWithGoogle"
                >
                  <v-icon>mdi-google</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="outlined"
                  size="large"
                  color="grey-lighten-1"
                  @click="loginWithFacebook"
                >
                  <v-icon>mdi-facebook</v-icon>
                </v-btn>
              </div>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </PageWrapper>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { login, loading, error } = useAuth()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)

const emailRules = [
  value => !!value || 'Email обязателен',
  value => /.+@.+\..+/.test(value) || 'Введите корректный email',
]

const passwordRules = [
  value => !!value || 'Пароль обязателен',
  value => value.length >= 6 || 'Пароль должен быть не менее 6 символов',
]

const handleLogin = async () => {
  if (!email.value || !password.value) {
    return
  }

  try {
    await login(email.value, password.value, rememberMe.value)
  } catch (err) {
    console.error('Ошибка входа:', err)
  }
}

const loginWithGoogle = () => {
  console.log('Вход через Google')
}

const loginWithFacebook = () => {
  console.log('Вход через Facebook')
}
</script>

<style scoped>
.fill-height {
  min-height: calc(100vh - 64px);
}

.rounded-lg {
  border-radius: 16px;
}

.gap-3 {
  gap: 12px;
}

:deep(.v-card) {
  background-color: #1e1e1e !important;
}

:deep(.v-field__outline) {
  color: rgba(255, 255, 255, 0.2) !important;
}

:deep(.v-field--variant-outlined .v-field__outline__start),
:deep(.v-field--variant-outlined .v-field__outline__notch),
:deep(.v-field--variant-outlined .v-field__outline__end) {
  border-color: rgba(255, 255, 255, 0.2) !important;
}

:deep(.v-field--focused .v-field__outline) {
  color: #4CAF50 !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-field__append-inner) .v-icon {
  color: rgba(255, 255, 255, 0.7) !important;
}
</style>