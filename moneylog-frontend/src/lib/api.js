import { auth } from "$lib/authStore";
import { get } from "svelte/store";

const BASE_URL = "http://localhost:8000";

async function request(path, options = {}) {
  const { token } = get(auth);

  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...(options.headers || {})
    }
  });

  if (res.status === 401) {
    throw new Error("Unauthorized");
  }

  return res.json();
}

export function getDashboard() {
  return request("/api/dashboard/");
}

export function getTransactions(params = "") {
  return request(`/api/transactions/${params}`);
}
