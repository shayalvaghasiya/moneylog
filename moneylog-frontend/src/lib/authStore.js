import { writable } from "svelte/store";
import { browser } from "$app/environment";

export const auth = writable({
  token: null,
  ready: false
});

if (browser) {
  const token = localStorage.getItem("access_token");
  auth.set({ token, ready: true });
}

export function login(token) {
  if (browser) {
    localStorage.setItem("access_token", token);
  }
  auth.set({ token, ready: true });
}

export function logout() {
  if (browser) {
    localStorage.removeItem("access_token");
  }
  auth.set({ token: null, ready: true });
}
