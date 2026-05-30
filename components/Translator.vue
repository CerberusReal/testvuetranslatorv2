<template>
  <div class="translator card p-4 shadow">
    <h2 class="mb-4 text-center fw-bold">Мини-Переводчик</h2>

    <div class="d-flex gap-2 mb-3">
      <select v-model="sourceLang" class="form-select w-50">
        <option value="" disabled selected>-- Из какого языка --</option>
        <option value="Russian">Русский</option>
        <option value="English">Английский</option>
        <option value="Spanish">Испанский</option>
        <option value="Polish">Польский</option>
        <option value="German">Немецкий</option>
        <option value="French">Французский</option>
        <option value="Korean">Корейский</option>
        <option value="Japanese">Японский</option>
      </select>
      <select v-model="outputLang" class="form-select w-50">
        <option value="" disabled selected>-- На какой язык --</option>
        <option value="Russian">Русский</option>
        <option value="English">Английский</option>
        <option value="Spanish">Испанский</option>
        <option value="Polish">Польский</option>
        <option value="German">Немецкий</option>
        <option value="French">Французский</option>
        <option value="Korean">Корейский</option>
        <option value="Japanese">Японский</option>
      </select>
    </div>

    <div class="mb-3">
    <textarea
      v-model="inputText"
      placeholder="Введи сюда текст для перевода..."
      rows="5"
      class="form-control"
    ></textarea>
</div>
    <button
      @click="translate" 
      :disabled="loading" 
      :class="loading ? 'btn btn-info' : 'btn btn-primary'"
      class="w-100 mb-4 rounded-3"
    >
      <span v-if="loading">Переводим, подожди...</span>
      <span v-else>Перевести</span>
    </button>

    <div v-if="translation" class="alert alert-success" role="alert">
      <strong>Перевод:</strong>
      <p class="mb-0 mt-2">{{ translation }}</p>
    </div>
    
    <p v-if="error" class="alert alert-danger" role="alert">{{ error }}</p>
    <footer class="text-muted">© FireDestik (and a lil' bit of AI), 2026</footer>
  </div>
</template>

<script setup>
// дальше код от ИИ (axios), потому что, видимо, он нужен для работы ИИ в переводчике, весь код выше написан мной с помощью bootstrap.
// Импортируем только ref, никаких сложных штук вроде computed нам пока не надо
import { ref } from 'vue'
import axios from 'axios'

// Создаем простые реактивные переменные (коробки для данных)
const inputText = ref('')   // текст пользователя
const sourceLang = ref('')  // исходный язык
const outputLang = ref('')  // целевой язык
const translation = ref('') // готовый перевод от ИИ
const loading = ref(false)  // Флаг загрузки: true (перевод идет) или false (сервер молчит)
const error = ref('')       // Текст ошибки, если всё сломается

async function translate() {
  // проверяем, заполнил ли пользователь все поля
  // если текст пустой или языки не выбраны, то ругаюсь
  if (inputText.value.trim() === '' || sourceLang.value === '' || outputLang.value === '') {
    error.value = 'Эй, заполни все поля: введи текст и выбери оба языка!'
    return
  }

  // Шаг 2: Включаем режим загрузки и очищаем старые результаты
  loading.value = true
  error.value = ''
  translation.value = ''

  // Шаг 3: Пробуем отправить данные на наш Python-сервер
  try {
    const response = await axios.post('http://localhost:8000/translate', {
      text: inputText.value,
      source_lang: sourceLang.value,
      output_lang: outputLang.value
    })

    // Если сервер вернул ответ, записываем перевод в нашу переменную
    translation.value = response.data.translation

  } catch (err) {
    // Если сервер выключен или случилась какая-то беда
    error.value = 'Что-то пошло не так. Проверь, запущен ли твой server.py!'
    console.error(err) // Выводим полную ошибку в консоль браузера для отладки
  } finally {
    // Этот блок выполнится В ЛЮБОМ СЛУЧАЕ (и при успехе, и при ошибке)
    // Выключаем режим загрузки, чтобы кнопка снова стала активной
    loading.value = false
  }
}
</script>

<style scoped>
.translator {
  width: 100%;
  max-width: 550px;
  font-family: "Open Sans", sans-serif;
}
</style>