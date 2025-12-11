import { inject } from "vue";

export const API_KEY = Symbol("APIClient");

export function useApi() {
  const api = inject(API_KEY);
  if (!api) throw new Error("APIClient не найден. Убедись, что плагин установлен.");
  return api;
}
