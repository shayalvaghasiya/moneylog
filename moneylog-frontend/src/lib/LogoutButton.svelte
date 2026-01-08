<script>
  import { logout } from "$lib/authStore";
  import { goto, replaceState } from "$app/navigation";

  function handle_logout() {
    logout();
    goto("/login", {replaceState: true});
  }
</script>

<button on:click={handle_logout}>
  Logout
</button>
