import asyncio
from pyppeteer import launch


class MoRequest:
    def __init__(self):
        self.launch_options = {
            "args": [
                "--disable-gpu",
                "--disable-web-security",
                "--disable-xss-auditor",  # 关闭 XSS Auditor
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--allow-running-insecure-content",  # 允许不安全内容
                "--disable-webgl",
                "--disable-popup-blocking"
            ],
            "ignoreHTTPSErrors": True,  # 忽略证书错误
            "headless": True,  # 显示界面
        }

    async def request(self, url):
        browser = await launch(self.launch_options)
        context = await browser.createIncognitoBrowserContext()  # 隐身模式
        page = await context.newPage()
        tasks = [
            # 设置UA
            # asyncio.ensure_future(page.setUserAgent("...")),
            # 注入初始 hook 代码，具体内容之后介绍
            # asyncio.ensure_future(page.evaluateOnNewDocument("...")),
            # 开启请求拦截
            asyncio.ensure_future(page.setRequestInterception(False)),
            # 启用JS，不开的话无法执行JS
            asyncio.ensure_future(page.setJavaScriptEnabled(True)),
            # 关闭缓存
            asyncio.ensure_future(page.setCacheEnabled(False)),
            # 设置窗口大小
            asyncio.ensure_future(page.setViewport(
                {"width": 1920, "height": 1080}))
        ]
        await asyncio.wait(tasks)
        await page.goto(url)

        def get_src_or_href_js():
            return """
                function get_src_or_href_sec_auto(nodes) {
                    let result = [];
                    for (let node of nodes) {
                        let src = node.getAttribute("src");
                        if (src) {
                            base = location.protocol + location.host;
                            url=new URL(src, base).href;
                            result.push(url)
                        }
                    }
                    return result;
                }
            """

        links = await page.querySelectorAllEval("[src]", get_src_or_href_js())

        content = await page.content()
        await browser.close()
        return content,links

async def main():
    test = MoRequest()
    content,links = await test.request('https://blog.fundebug.com/')

asyncio.run(main())
# 检测请求URL
# async def request_check(req):
#     if req.resourceType in ['image', 'media', 'eventsource', 'websocket']:
#         await req.abort()
#     else:
#         crawled.append(req.url)
#         await req.continue_()
#page.on('request', lambda req: asyncio.ensure_future(request_check(req)))
