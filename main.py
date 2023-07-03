import uvicorn
from keplergl import KeplerGl
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import map.shared as shared

# ---- API ENTRYPOINT ----
# Load shared data and config

shared.load_data()
demo_portugal = shared.data

# Pass the layers in the config to the KeplerGl constructor
kepler_map = KeplerGl(config=shared.config, data={"rowek3uu": demo_portugal})
# kepler_html = kepler_map._repr_html_()
kepler_html = kepler_map._repr_html_().decode("utf-8")  # Decode the byte string

app = FastAPI()


@app.get("/")
async def index():
    modified_html = f"""
        <html>
            <head><title>Evolução Demográfica PT</title></head>
            
            <body>
                {kepler_html}
            </body>
        </html>
    """
    return HTMLResponse(content=modified_html, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8889, reload=True)


# Indice de envelhecimento - 2040
# Responsabilidade Nossa - articular com PP e queremos que seja alojado l'a.
