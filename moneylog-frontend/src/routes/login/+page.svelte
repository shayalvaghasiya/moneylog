<script>
  import { goto } from "$app/navigation";
  import { setToken } from "$lib/auth";

  let username = "";
  let password = "";
  let error = "";

  async function login() {
    error = "";

    const res = await fetch("http://localhost:8000/api/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) {
      error = "Invalid username or password";
      return;
    }

    const data = await res.json();
    setToken(data.access);
    goto("/");
  }
</script>

<h1>Login</h1>

<form on:submit|preventDefault={login}>
  <div>
    <!-- svelte-ignore a11y_label_has_associated_control -->
    <label>Username</label>
    <input bind:value={username} />
  </div>

  <div>
    <!-- svelte-ignore a11y_label_has_associated_control -->
    <label>Password</label>
    <input type="password" bind:value={password} />
  </div>

  <button type="submit">Login</button>

  {#if error}
    <p style="color: red;">{error}</p>
  {/if}
</form>
