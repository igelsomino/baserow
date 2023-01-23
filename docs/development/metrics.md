## Metrics in Baserow

You should be wrapping 

### Using metrics in your local dev env 

1. Sign up at https://honeycomb.io.
2. Create your own environment inside of honeycomb, you will configure your local dev setup to send events here. 
3. Click on your green environment in the sidebar, click the config icon.
4. Switch to API keys and copy your API key.
5. Edit your local `.env` and set
6. `./dev.sh restart`

```bash
HONEYCOMB_API_KEY=YOUR_KEY
BASEROW_ENABLE_OTEL=true
```