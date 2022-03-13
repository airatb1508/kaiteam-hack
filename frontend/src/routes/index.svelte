<script>
	import Prism from 'prismjs';
	import Hoverable from "$lib/Hoverable.svelte";

	let input;
	let form;

	let data = [];

	function update() {
		let text = input.value;
		let result_element = document.querySelector("#highlighting-content");

		if(text[text.length-1] == "\n") {
			text += " ";
		}
		result_element.innerHTML = text.replace(new RegExp("&", "g"), "&amp;").replace(new RegExp("<", "g"), "&lt;");
		Prism.highlightElement(result_element);
		submit();
	}

	function sync_scroll() {
		let element = input;
		/* Scroll result to scroll coords of event - sync with textarea */
		let result_element = document.querySelector("#highlighting");
		// Get and set x and y
		result_element.scrollTop = element.scrollTop;
		result_element.scrollLeft = element.scrollLeft;
	}

	function check_tab(event) {
		let element = input;
		let code = element.value;
		if(event.key == "Tab") {
			/* Tab key pressed */
			event.preventDefault(); // stop normal
			let before_tab = code.slice(0, element.selectionStart); // text before tab
			let after_tab = code.slice(element.selectionEnd, element.value.length); // text after tab
			let cursor_pos = element.selectionEnd + 4; // where cursor moves after tab - moving forward by 1 char to after tab
			element.value = before_tab + "    " + after_tab; // add tab char
			// move cursor
			element.selectionStart = cursor_pos;
			element.selectionEnd = cursor_pos;
			update(); // Update text to include indent
		}
	}

	function submit() {
		let formData = new FormData(form);

		fetch("http://localhost:5000/analyze", {
			method: 'POST',
			body: formData
		})
		.then(res => res.json())
		.then(json => data = json)
	}
</script>

<h1>Realtime Static JS Analyzer</h1>

<form bind:this={form}>
	<div>
		<textarea
			placeholder="Enter Source Code Here"
			id="editing"
			spellcheck="false"
			name="code"
			bind:this={input}
			on:input={() => {update(); sync_scroll();}}
			on:scroll={sync_scroll}
			on:keydown={check_tab}
		></textarea>
		<pre id="highlighting" aria-hidden="true" class="language-js" tabindex="0">
			<code class="language-js" id="highlighting-content"></code>
			<u id="underline">
				{#each data as line}
					<Hoverable line={line}/>
				{/each}
			</u>
		</pre>
	</div>
</form>


<style>
	pre code {
		position: absolute;
		left: 30px;
	}

	u {
		display: block;
		text-decoration: none;
		position: absolute;
		left: 0px;
		top: 0px;
		z-index: 2;
	}

	div {
		position: relative;
		background-color: black;
		height: 80vh;
		width: 100%;
		overflow: auto;
	}
</style>
