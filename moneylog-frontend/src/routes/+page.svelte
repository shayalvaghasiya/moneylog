<script>
  import { onMount } from "svelte";
  import { getToken, isLoggedIn } from "$lib/auth";
  import { goto } from "$app/navigation";

  let transactions = [];

  onMount(async () => {
    if (!isLoggedIn()) {
      goto("/login");
      return;
    }

    const res = await fetch(
      "http://localhost:8000/api/transactions/",
      {
        headers: {
          Authorization: `Bearer ${getToken()}`
        }
      }
    );

    const data = await res.json();
    transactions = data.results;
  });
</script>

<h1>MoneyLog</h1>

<ul>
  {#each transactions as tx}
    <li>{tx.category_name} — ₹{tx.amount}</li>
  {/each}
</ul>
