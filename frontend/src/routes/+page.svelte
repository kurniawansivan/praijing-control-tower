<script lang="ts">
	import { onMount } from 'svelte';
	let preview: Array<any> = [];
	let error_text = '';

	onMount(async () => {
		try {
			const res = await fetch('http://localhost:8000/schedule/preview');
			preview = await res.json();
		} catch {
			error_text = 'Cannot reach backend';
		}
	});
</script>

<div class="mx-auto max-w-screen-lg space-y-6 px-4 py-8 sm:px-6">
	<h1 class="text-xl font-semibold tracking-tight md:text-2xl">Praijing Control Tower</h1>

	{#if error_text}
		<p class="text-red-600">{error_text}</p>
	{/if}

	<div class="rounded-xl border border-neutral-200 p-5">
		<p class="mb-3 text-sm text-neutral-600">Schedule Preview</p>
		{#if preview.length === 0}
			<p class="text-neutral-500">No items yet.</p>
		{:else}
			<div class="overflow-x-auto">
				<table class="min-w-full text-sm">
					<thead class="text-left text-neutral-600">
						<tr>
							<th class="py-2 pr-4">Due date</th>
							<th class="py-2 pr-4">Priority</th>
							<th class="py-2 pr-4">SKU</th>
							<th class="py-2 pr-4">Quantity</th>
							<th class="py-2">Order ID</th>
						</tr>
					</thead>
					<tbody>
						{#each preview as row}
							<tr class="border-t">
								<td class="py-2 pr-4">{row.due_date}</td>
								<td class="py-2 pr-4 capitalize">{row.priority}</td>
								<td class="py-2 pr-4">{row.product_sku}</td>
								<td class="py-2 pr-4">{row.quantity}</td>
								<td class="py-2">{row.order_id}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>
</div>
