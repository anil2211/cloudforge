from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {
        'message': 'CloudForge Platform Running'
    }

@app.get('/health')
def health():
    return {
        'status': 'healthy'
    }