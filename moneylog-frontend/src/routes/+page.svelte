<!-- dashboard -->

<script>
	import { onMount } from 'svelte';
	import { auth, logout } from '$lib/authStore';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';
	import { getDashboard } from '$lib/api';

	const BASE_URL = 'http://localhost:8000';
	let loading = true;
	let error = null;
	let dashboard;

	onMount(async () => {
		const { token } = get(auth);

		if (!token) {
			goto('/login');
			return;
		}

		try {
			dashboard = await getDashboard();
		} catch (e) {
			console.error(e);
			if (e.status === 401) {
				logout();
				goto('/login');
				return;
			}
			error = 'Failed to load dashboard data.';
		} finally {
			loading = false;
		}
	});
</script>

<h1>MoneyLog</h1>

{#if loading}
	<p>Loading dashboard…</p>
{:else if error}
	<p style="color: red">{error}</p>
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
