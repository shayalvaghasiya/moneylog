<!-- base UI (shared across all pages) -->

<script>
	import {auth} from "$lib/authStore";
	import {derived} from "svelte/store";
	import LogoutButton  from "$lib/LogoutButton.svelte";

	const isLoggedIn = derived(auth, ($auth) => !!$auth?.token);
</script>

<nav>
	<a href="/">Home</a>
	<a href="/transactions">Transactions</a>
	{#if $isLoggedIn}
		<LogoutButton />
	{/if}
</nav>
<slot />
