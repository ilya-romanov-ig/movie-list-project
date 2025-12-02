<template>
  <PageWrapper>
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card elevation="4" class="pa-6 rounded-lg">
          <!-- Заголовок -->
          <div class="text-center mb-6">
            <v-icon color="green-darken-3" size="64" class="mb-2">
              mdi-account-plus
            </v-icon>
            <h1 class="text-h4 font-weight-bold mb-2 text-white">Регистрация</h1>
            <p class="text-body-1 text-grey">Создайте новый аккаунт</p>
          </div>

          <!-- Форма регистрации -->
          <v-form @submit.prevent="handleRegister">
            <div class="d-flex gap-3 mb-4">
              <v-text-field
                v-model="firstName"
                label="Имя"
                variant="outlined"
                prepend-inner-icon="mdi-account"
                :rules="nameRules"
                required
                bg-color="grey-darken-3"
              ></v-text-field>

              <v-text-field
                v-model="lastName"
                label="Фамилия"
                variant="outlined"
                :rules="nameRules"
                required
                bg-color="grey-darken-3"
              ></v-text-field>
            </div>

            <v-text-field
              v-model="email"
              label="Email"
              type="email"
              variant="outlined"
              prepend-inner-icon="mdi-email"
              :rules="emailRules"
              class="mb-4"
              required
              bg-color="grey-darken-3"
            ></v-text-field>

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
              class="mb-4"
              bg-color="grey-darken-3"
            ></v-text-field>

            <v-text-field
              v-model="confirmPassword"
              label="Подтверждение пароля"
              :type="showConfirmPassword ? 'text' : 'password'"
              variant="outlined"
              prepend-inner-icon="mdi-lock-check"
              :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
              :rules="confirmPasswordRules"
              required
              @click:append-inner="showConfirmPassword = !showConfirmPassword"
              class="mb-6"
              bg-color="grey-darken-3"
            ></v-text-field>

            <!-- Соглашение -->
            <v-checkbox
              v-model="agreeTerms"
              :rules="[v => !!v || 'Необходимо согласиться с условиями']"
              required
              class="mb-6"
              hide-details
              color="green-darken-3"
            >
              <template v-slot:label>
                <span class="text-white">
                  Я согласен с 
                  <a href="#" class="text-green-darken-3 text-decoration-none">
                    условиями использования
                  </a>
                </span>
              </template>
            </v-checkbox>

            <!-- Кнопка регистрации -->
            <v-btn
              type="submit"
              color="green-darken-3"
              size="large"
              block
              :loading="loading"
              class="mb-4"
            >
              <v-icon start>mdi-account-plus</v-icon>
              Зарегистрироваться
            </v-btn>

            <!-- Ссылка на вход -->
            <div class="text-center">
              <span class="text-grey mr-2">Уже есть аккаунт?</span>
              <router-link 
                to="/login" 
                class="text-green-darken-3 font-weight-bold text-decoration-none"
              >
                Войти
              </router-link>
            </div>

            <!-- Разделитель -->
            <v-divider class="my-6" color="grey-darken-2"></v-divider>

            <!-- Быстрая регистрация -->
            <div class="text-center">
              <p class="text-grey mb-4">Или зарегистрируйтесь через</p>
              <div class="d-flex justify-center gap-3">
                <v-btn
                  icon
                  variant="outlined"
                  size="large"
                  color="grey-lighten-1"
                  @click="registerWithGoogle"
                >
                  <v-icon>mdi-google</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="outlined"
                  size="large"
                  color="grey-lighten-1"
                  @click="registerWithFacebook"
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'

const router = useRouter()

// Данные формы
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const agreeTerms = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)

// Правила валидации
const nameRules = [
  value => !!value || 'Обязательное поле',
  value => value.length >= 2 || 'Минимум 2 символа',
]

const emailRules = [
  value => !!value || 'Email обязателен',
  value => /.+@.+\..+/.test(value) || 'Введите корректный email',
]

const passwordRules = [
  value => !!value || 'Пароль обязателен',
  value => value.length >= 8 || 'Минимум 8 символов',
  value => /[A-Z]/.test(value) || 'Хотя бы одна заглавная буква',
  value => /\d/.test(value) || 'Хотя бы одна цифра',
]

const confirmPasswordRules = computed(() => [
  value => !!value || 'Подтвердите пароль',
  value => value === password.value || 'Пароли не совпадают',
])

// Обработка регистрации
const handleRegister = async () => {
  if (!firstName.value || !lastName.value || !email.value || 
      !password.value || !confirmPassword.value || !agreeTerms.value) {
    return
  }

  loading.value = true

  try {
    console.log('Регистрация:', {
      firstName: firstName.value,
      lastName: lastName.value,
      email: email.value,
      password: password.value,
    })

    await new Promise(resolve => setTimeout(resolve, 1500))

    localStorage.setItem('authToken', 'fake-token-123')
    router.push('/')
    
  } catch (error) {
    console.error('Ошибка регистрации:', error)
  } finally {
    loading.value = false
  }
}

// Альтернативные способы регистрации
const registerWithGoogle = () => {
  console.log('Регистрация через Google')
}

const registerWithFacebook = () => {
  console.log('Регистрация через Facebook')
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

/* Адаптивность для полей имени и фамилии */
@media (max-width: 600px) {
  .d-flex.gap-3 {
    flex-direction: column;
    gap: 16px;
  }
}

/* Стили для тёмной темы */
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