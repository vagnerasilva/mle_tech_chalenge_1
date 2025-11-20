from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def no_logged_in(request: Request):
    """Rota raiz para primeiro acesso e primeiras instruções
    """
    html = """
    <html>
        <head>
            <title>Books to Scrap - API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f5f5f5;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    text-align: left;
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background: #333;
                    color: white;
                }
                tr:hover {
                    background: #e9e9e9;
                }
                .method {
                    font-weight: bold;
                    color: #1e88e5;
                }
            </style>
        </head>
        <body>
            <h1>📚 Bem vindo ao Books to Scrap API</h1>
            <p>Para logar acesse a rota /login/</p>
        </body>
    </html>
    """

    return HTMLResponse(content=html)
