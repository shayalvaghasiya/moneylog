<!-- dashboard -->

<script>
	import { onMount } from 'svelte';
	import { auth } from '$lib/authStore';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';
	import { getDashboard } from '$lib/api';

	const BASE_URL = 'http://localhost:8000';
	let loading = true;
	let dashboard;

	onMount(async () => {
		const { token } = get(auth);

		if (!token) {
			goto('/login');
			return;
		}

		dashboard = await getDashboard();
		loading = false;
	});
</script>

<h1>MoneyLog</h1>

{#if loading}
	<p>Loading dashboard…</p>
{:else}
	<h2>Total Balance: ₹{dashboard.total_balance}</h2>

	<h3>Accounts</h3>
	<ul>
		{#each dashboard.accounts as acc}
			<li>{acc.name}: ₹{acc.balance}</li>
		{/each}
	</ul>

	<h3>Monthly Spend</h3>
	<ul>
		{#each dashboard.monthly_spend as item}
			<li>{item.category}: ₹{item.total}</li>
		{/each}
	</ul>
{/if}
