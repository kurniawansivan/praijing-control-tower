<script lang="ts">
	import { onMount } from 'svelte';
	let status_text = 'loading...';

	onMount(async () => {
		try {
			const response = await fetch('http://localhost:8000/health');
			const data = await response.json();
			status_text = `status: ${data.status}`;
		} catch {
			status_text = 'status: unreachable';
		}
	});
</script>

<div class="mx-auto max-w-screen-lg space-y-6 px-4 py-8 sm:px-6">
	<h1 class="text-xl font-semibold tracking-tight md:text-2xl">Praijing Control Tower</h1>

	<div class="rounded-xl border border-neutral-200 p-5">
		<p class="text-sm text-neutral-600">Backend health</p>
		<span
			class="mt-2 inline-flex items-center gap-2 rounded-lg border px-3 py-1"
			class:!border-green-300={status_text === 'status: ok'}
			class:!border-red-300={status_text !== 'status: ok'}
		>
			{status_text}
		</span>
	</div>
</div>
