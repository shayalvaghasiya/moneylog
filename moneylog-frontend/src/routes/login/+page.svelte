<!-- login page -->

<script>
	import { goto } from '$app/navigation';
	import { login } from '$lib/authStore';

	let username = '';
	let password = '';
	let error = '';
	let isLoading = false;
	BASE_URL = 'http://localhost:8000';

	async function handle_login() {
		if (isLoading) return;
		isLoading = true;
		error = '';

		try {
			const res = await fetch(`${BASE_URL}/api/token/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ username, password })
			});

			if (!res.ok) {
				error = 'Invalid username or password';
				return;
			}

			const data = await res.json();
			login(data.access);
			await Promise.resolve();
			goto('/', { replaceState: true });
		} catch (e) {
			error = 'Unable to connect to server.';
		} finally {
			isLoading = false;
		}
	}
</script>

<h1>Login</h1>

<form on:submit|preventDefault={handle_login}>
	<label>
		Username <input placeholder="Username" bind:value={username} disabled={isLoading} />
	</label>
	<label>
		Password <input
			type="password"
			placeholder="Password"
			bind:value={password}
			disabled={isLoading}
		/>
	</label>
	<button disabled={isLoading}>{isLoading ? 'Logging in...' : 'Login'}</button>
</form>

{#if error}
	<p style="color:red">{error}</p>
{/if}
