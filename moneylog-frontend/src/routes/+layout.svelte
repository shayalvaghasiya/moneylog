<!-- base UI (shared accross all pages) -->

<script>
	import {auth} from "$lib/authStore";
	import {derived} from "svelte/store";
	import LogoutButton  from "$lib/LogoutButton.svelte";

	const isLoggedIn = derived(auth, ($auth) => !!$auth.token);
</script>

<nav>
	<a href="/">Home</a>

	{#if $isLoggedIn}
		<LogoutButton />
	{/if}
</nav>
<slot />
