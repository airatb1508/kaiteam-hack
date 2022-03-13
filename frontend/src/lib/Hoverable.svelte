<script>
	import { fade } from 'svelte/transition'
	import { scale } from 'svelte/transition'
	import { quintOut } from 'svelte/easing'

    export let line

	let hovering = false

	const enter = () => {
		hovering = true
        console.log("hover")
	}
	const leave = () => (hovering = false)
</script>

<span
    class="note"
    style="position: absolute; left: 0px; top: {line.start_point[0] * 17}pt; color: {line.type == "warning" ? "orange" : "red"}"
    on:mouseenter={enter}
    on:mouseleave={leave}
>
    {line.type == "warning" ? "!!" : "❌"}
    {#if hovering}
    <div in:scale={{duration: 150, easing: quintOut, opacity: 0}}
        class="hover"
    >
        <div in:fade={{duration: 150}}>
            {line.name}
        </div>
    </div>
{/if}

</span>


<span
    style=
        "height: 17pt;
        width: {7.79 * (line.end_point[1] - line.start_point[1])}pt;
        background-color: { line.type == "warning" ? "#ff04" : "#f004"};
        position: absolute;
        display: block;
        top: {line.start_point[0] * 17}pt;
        left: calc(30px + {line.start_point[1] * 7.79}pt);
        z-index: 1;
        border-radius: 4px"
    >
</span>


<style>
    .hover {
        position: absolute;
        left: 30px;
        top: 17pt;
        background: #333;
        z-index: 1000;
    }
</style>