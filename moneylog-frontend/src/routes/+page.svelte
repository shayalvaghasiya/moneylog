<!-- dashboard -->

<script>
	import { onMount } from 'svelte';
	import { auth } from '$lib/authStore';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';

	let transactions = [];
	let loading = true;
	let error = null;

	async function fetchTransactions(token) {
		try {
			const res = await fetch('http://localhost:8000/api/transactions/', {
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (!res.ok) throw new Error('Failed to fetch data');
			const data = await res.json();
			transactions = data.results;
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		const { token } = get(auth);

		if (!token) {
			goto('/login', { replaceState: true });
			return;
		}

		fetchTransactions(token);
	});
</script>

<h1>MoneyLog</h1>

{#if loading}
	<p>Loading...</p>
{:else if error}
	<p style="color: red">Error: {error}</p>
{:else}
	<ul>
		{#each transactions as tx}
			<li>{tx.category_name} — ₹{tx.amount}</li>
		{/each}
	</ul>
{/if}
