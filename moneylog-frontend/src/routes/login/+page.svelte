<!-- login page -->

<script>
	import { goto } from '$app/navigation';
	import { login } from '$lib/authStore';

	let username = '';
	let password = '';
	let confirmPassword = '';
	let isRegister = false;
	let error = '';
	let isLoading = false;
	const BASE_URL = 'http://localhost:8000';

	async function handleSubmit() {
		if (isRegister) {
			await handle_register();
		} else {
			await handle_login();
		}
	}

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

	async function handle_register() {
		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}
		if (isLoading) return;
		isLoading = true;
		error = '';

		try {
			const res = await fetch(`${BASE_URL}/api/register/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ username, password })
			});

			if (!res.ok) {
				error = 'Registration failed';
				return;
			}

			isRegister = false;
			error = '';
			alert('Registration successful! Please log in.');
		} catch (e) {
			error = 'Unable to connect to server.';
		} finally {
			isLoading = false;
		}
	}
</script>

<div
	class="flex min-h-screen flex-col items-center justify-center bg-black bg-cover bg-center bg-no-repeat px-6 py-8 mx-auto lg:py-0"
	style="background-image: url('/images/bg.png');"
>
	<div
		class="w-full rounded-lg shadow border md:mt-0 sm:max-w-md xl:p-0 bg-gray-900/50 backdrop-blur-md border-gray-700"
	>
		<div class="p-6 space-y-4 md:space-y-6 sm:p-8">
			<h1 class="text-xl font-bold leading-tight tracking-tight md:text-2xl text-white">
				{isRegister ? 'Create an account' : 'Sign in to your account'}
			</h1>
			<form class="space-y-4 md:space-y-6" on:submit|preventDefault={handleSubmit}>
				<div>
					<label for="username" class="block mb-2 text-sm font-medium text-white"
						>Your Username</label
					>
					<input
						type="text"
						id="username"
						class="rounded-lg block w-full p-2.5 bg-gray-800/50 border border-gray-600 placeholder-gray-400 text-white focus:ring-emerald-500 focus:border-emerald-500"
						placeholder="username"
						bind:value={username}
						required
						disabled={isLoading}
					/>
				</div>
				<div>
					<label for="password" class="block mb-2 text-sm font-medium text-white">Password</label>
					<input
						type="password"
						id="password"
						placeholder="••••••••"
						class="rounded-lg block w-full p-2.5 bg-gray-800/50 border border-gray-600 placeholder-gray-400 text-white focus:ring-emerald-500 focus:border-emerald-500"
						bind:value={password}
						required
						disabled={isLoading}
					/>
				</div>
				{#if isRegister}
					<div>
						<label for="confirm-password" class="block mb-2 text-sm font-medium text-white"
							>Confirm Password</label
						>
						<input
							type="password"
							id="confirm-password"
							placeholder="••••••••"
							class="rounded-lg block w-full p-2.5 bg-gray-800/50 border border-gray-600 placeholder-gray-400 text-white focus:ring-emerald-500 focus:border-emerald-500"
							bind:value={confirmPassword}
							required
							disabled={isLoading}
						/>
					</div>
				{/if}
				{#if error}
					<p class="text-sm text-red-500">{error}</p>
				{/if}
				<button
					type="submit"
					class="w-full text-white bg-emerald-600 hover:bg-emerald-700 focus:ring-4 focus:outline-none focus:ring-emerald-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center disabled:opacity-50"
					disabled={isLoading}
				>
					{isLoading ? 'Processing...' : isRegister ? 'Sign up' : 'Sign in'}
				</button>
				<p class="text-sm font-light text-gray-400">
					{isRegister ? 'Already have an account?' : 'Don’t have an account yet?'}
					<button
						type="button"
						class="font-medium text-emerald-500 hover:underline"
						on:click={() => {
							isRegister = !isRegister;
							error = '';
						}}
					>
						{isRegister ? 'Sign in' : 'Sign up'}
					</button>
				</p>
			</form>
		</div>
	</div>
</div>
