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

<div class="flex min-h-screen flex-col items-center justify-center bg-black bg-cover bg-center bg-no-repeat px-6 py-8 mx-auto lg:py-0" style="background-image: url('/images/bg.png');">
	<div class="w-full rounded-lg shadow border md:mt-0 sm:max-w-md xl:p-0 bg-gray-900/50 backdrop-blur-md border-gray-700">
		<div class="p-6 space-y-4 md:space-y-6 sm:p-8">
			<h1 class="text-xl font-bold leading-tight tracking-tight md:text-2xl text-white">
				Sign in to your account
			</h1>
			<form class="space-y-4 md:space-y-6" on:submit|preventDefault={handle_login}>
				<div>
					<label for="username" class="block mb-2 text-sm font-medium text-white">Your Username</label>
					<input type="text" id="username" class="rounded-lg block w-full p-2.5 bg-gray-800/50 border border-gray-600 placeholder-gray-400 text-white focus:ring-emerald-500 focus:border-emerald-500" placeholder="username" bind:value={username} required disabled={isLoading} />
				</div>
				<div>
					<label for="password" class="block mb-2 text-sm font-medium text-white">Password</label>
					<input type="password" id="password" placeholder="••••••••" class="rounded-lg block w-full p-2.5 bg-gray-800/50 border border-gray-600 placeholder-gray-400 text-white focus:ring-emerald-500 focus:border-emerald-500" bind:value={password} required disabled={isLoading} />
				</div>
				{#if error}
					<p class="text-sm text-red-500">{error}</p>
				{/if}
				<button type="submit" class="w-full text-white bg-emerald-600 hover:bg-emerald-700 focus:ring-4 focus:outline-none focus:ring-emerald-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center disabled:opacity-50" disabled={isLoading}>{isLoading ? 'Logging in...' : 'Sign in'}</button>
			</form>
		</div>
	</div>
</div>
