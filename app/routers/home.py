from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Rota acessada após o login, contendo informações sobre as rotas da api
    """
    routes = []
    for route in request.app.routes:
        if hasattr(route, "methods"):
            for method in route.methods:
                if method not in ["HEAD", "OPTIONS"]:
                    if '/api/' in route.path:
                        routes.append({
                            "path": route.path,
                            "method": method
                        })

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
            <p>Veja a lista de todas as rotas disponíveis:</p>

            <table>
                <tr>
                    <th>Método</th>
                    <th>Path</th>
                </tr>
    """

    for r in routes:
        html += f"""
            <tr>
                <td class='method'>{r["method"]}</td>
                <td>{r["path"]}</td>
            </tr>
        """

    html += """
            </table>
        </body>
    </html>
    """

    return HTMLResponse(content=html)
