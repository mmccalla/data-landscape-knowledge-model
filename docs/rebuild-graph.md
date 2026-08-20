# Rebuild the standalone graph

[← README](../README.md)

[`graph.html`](../graph.html) contains D3 and the complete CSV projection inline, so it opens locally without a web server or network connection. Rebuild it after changing either CSV file:

```sh
npm install
npm run build
npm test
```

To refresh the README product hero ([`docs/images/product-graph.png`](images/product-graph.png)) after graph UI or product-scope changes:

```sh
node scripts/capture-readme-heroes.mjs
```
