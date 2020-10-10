import os
from app import app
from app.routes import router
import uvicorn

app.include_router(router)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run('app:app', host='0.0.0.0', port=port, debug=True)
