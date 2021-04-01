import time

import argparse
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from queries import get_issues_query

app = FastAPI()


@app.get("/projects")
async def get_projects():
    """

    :return:
    """


@app.get("/issues")
async def get_issues(ct:str):
    """

    :return:
    """
    timestamp = time.mktime(time.strptime(ct, "%Y%m%d"))

    created_after = time.strftime("%Y-%m-%d",  time.localtime(timestamp))
    return HTMLResponse(get_issues_query(created_after))


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
