<script>
  import { clearToken } from "$lib/auth";
  import { goto } from "$app/navigation";

  function logout() {
    clearToken();
    goto("/login");
  }
</script>

<button on:click={logout}>
  Logout
</button>
