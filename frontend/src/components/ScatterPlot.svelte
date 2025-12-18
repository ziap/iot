<script lang="ts">
	let {
		data1 = [],
		data2 = [],
		time = [],
	} = $props<{
		data1?: number[]
		data2?: number[]
		time?: string[]
	}>()

	const WIDTH = 700
	const HEIGHT = 300
	const PADDING = 30

	const allValues = $derived([...data1, ...data2].filter((v): v is number => Number.isFinite(v)))

	const yMin = $derived(allValues.length ? Math.min(...allValues) - 5 : 0)
	const yMax = $derived(allValues.length ? Math.max(...allValues) + 5 : 50)

	const yScale = $derived.by(() => {
		const range = HEIGHT - PADDING * 2
		const domain = yMax - yMin
		if (domain === 0) {
			return (value: number) => HEIGHT / 2
		}
		return (value: number) => PADDING + (1 - (value - yMin) / domain) * range
	})

	const xScale = $derived.by(() => {
		return (index: number, len: number) => {
			const step = (WIDTH - PADDING * 2) / Math.max(1, len - 1)
			return PADDING + step * index
		}
	})
</script>

<svg width="100%" height="auto" viewBox={`0 0 ${WIDTH} ${HEIGHT}`}>
	<line
		x1={PADDING}
		y1={HEIGHT - PADDING + 1}
		x2={WIDTH - PADDING}
		y2={HEIGHT - PADDING + 1}
		stroke="#333"
	/>
	<line x1={PADDING} y1={PADDING} x2={PADDING} y2={HEIGHT - PADDING} stroke="#333" />

	{#each [0, 1, 2, 3, 4] as i}
		{@const val = yMin + (i / 4) * (yMax - yMin)}
		<text x={PADDING - 6} y={yScale(val) + 4} text-anchor="end" fill="#444" font-size="12"
			>{val.toFixed(0)}</text
		>
		<line
			x1={PADDING}
			x2={WIDTH - PADDING}
			y1={yScale(val)}
			y2={yScale(val)}
			stroke="#ddd"
			stroke-dasharray="4 4"
		/>
	{/each}

	{#each time as t, i}
		<text
			x={xScale(i, time.length)}
			y={HEIGHT - PADDING + 18}
			text-anchor="middle"
			font-size="11"
			opacity={i % 2 === 0 ? 1 : 0}
			fill="#666">{t}</text
		>
	{/each}

	{#each data1 as v, i}
		<circle class="point" cx={xScale(i, data1.length)} cy={yScale(v)} r="3" fill="red">
			<title>{v}</title>
		</circle>
	{/each}

	{#each data2 as v, i}
		<circle class="point" cx={xScale(i, data2.length)} cy={yScale(v)} r="3" fill="blue">
			<title>{v}</title>
		</circle>
	{/each}
</svg>

<style>
	.point:hover {
		r: 7;
		transition: 0.15s;
	}
</style>
