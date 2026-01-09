<script>
  import { onMount } from "svelte";
  import { getTransactions } from "$lib/api";
  import { auth } from "$lib/authStore";
  import { get } from "svelte/store";
  import { goto } from "$app/navigation";

  let data;
  let page = 1;
  let loading = true;

  async function load(pageNumber) {
    loading = true;
    data = await getTransactions(pageNumber);
    page = pageNumber;
    loading = false;
  }

  onMount(() => {
    const { token } = get(auth);
    if (!token) {
      goto("/login");
      return;
    }
    load(1);
  });
</script>

<h1>Transactions</h1>

{#if loading}
  <p>Loading…</p>
{:else}
  <ul>
    {#each data.results as tx}
      <li>
        {tx.category_name} — ₹{tx.amount}
      </li>
    {/each}
  </ul>

  <div style="margin-top: 1rem;">
    <button
      on:click={() => load(page - 1)}
      disabled={!data.previous}
    >
      Previous
    </button>

    <span> Page {page} </span>

    <button
      on:click={() => load(page + 1)}
      disabled={!data.next}
    >
      Next
    </button>
  </div>
{/if}
