<!-- login page -->

<script>
	import { goto } from '$app/navigation';
	import { login } from '$lib/authStore';

	let username = '';
	let password = '';
	let error = '';
	let isLoading = false;
	const BASE_URL = 'http://localhost:8000';

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

<form class="max-w-sm mx-auto" on:submit|preventDefault={handle_login}>
  <div class="mb-5">
    <label for="username" class="block mb-2.5 text-sm font-medium text-heading">Your Username</label>
    <input type="username" id="username" class="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" bind:value={username} required disabled={isLoading}/>
  </div>
  <div class="mb-5">
    <label for="password" class="block mb-2.5 text-sm font-medium text-heading">Your password</label>
    <input type="password" id="password" class="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body" bind:value={password} required disabled={isLoading} placeholder="••••••••"/>
  </div>
  <button type="submit" class="text-white bg-brand box-border border border-transparent hover:bg-brand-strong focus:ring-4 focus:ring-brand-medium shadow-xs font-medium leading-5 rounded-base text-sm px-4 py-2.5 focus:outline-none">Submit</button>
</form>
