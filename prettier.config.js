/**
 * @see https://prettier.io/docs/configuration
 * @type {import("prettier").Config}
 */
export default {
	useTabs: true,
	singleQuote: true,
	printWidth: 100,
	trailingComma: 'all',
	semi: false,
	arrowParens: 'avoid',
	plugins: ['prettier-plugin-svelte'],
	overrides: [
		{
			files: '*.svelte',
			options: {
				parser: 'svelte',
			},
		},
	],
}
