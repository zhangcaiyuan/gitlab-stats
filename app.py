import time

import argparse
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from monitor import get_issues_html, get_issues_list

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/projects")
async def get_projects():
    """

    :return:
    """


@app.get("/issues", response_class=HTMLResponse)
async def get_issues(request: Request, ct: str):
    print(ct)
    timestamp = time.mktime(time.strptime(ct, "%Y%m%d"))
    print(timestamp)
    created_after = time.strftime("%Y-%m-%d", time.localtime(timestamp))

    # issues = get_issues_html(created_after)
    # return HTMLResponse(issues)
    issues = get_issues_list(created_after)
    return templates.TemplateResponse("issues.html", {"request": request, "issues": issues})


@app.get("/milestones")
async def get_milestones():
    """

    :return:
    """


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="gitlab stats")

    parser.add_argument("--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port for HTTP server (default: 80)")

    args = parser.parse_args()

    # 启动http服务，任务preview、start时调用
    uvicorn.run(app, host=args.host, port=args.port)
