from fastapi import FastAPI

app = FastAPI(title='GitHub AI Genius API', version='1.0.0')


@app.get('/health')
def health():
    return {'ok': True, 'service': 'github-ai-genius'}
