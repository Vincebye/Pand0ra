import asyncio
import random
import psutil
import os
import signal
import time
import subprocess
import gc
from pyppeteer import launcher, launch
import configparser
from multiprocessing import Process, Manager
from urllib.parse import urlparse
launcher.AUTOMATION_ARGS.remove("--enable-automation")

cfg = configparser.ConfigParser()
cfg.read('pand0ra.conf')


def Timer(func):
    def call_func(*args, **kwargs):
        begin_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        Run_time = end_time - begin_time
        print(str(func.__name__) + "函数运行时间为" + str(Run_time))
        return ret
    return call_func


class HttpData:
    http_data = []

    @classmethod
    def init(cls):
        cls.http_data.clear()

    @classmethod
    def save(cls, data):
        cls.http_data.append(data)

    @classmethod
    def get(cls):
        return cls.http_data


class Page:
    def __init__(self, page_url, chrome_browser):
        self.url = page_url
        self.browser = chrome_browser

    async def run(self):
        t = random.randint(1, 4)
        tt = random.randint(t, 10)
        await asyncio.sleep(tt)
        try:
            page = await self.browser.newPage()
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
            await page.goto(self.url, options={'timeout': 30000})
            await page.waitFor(selectorOrFunctionOrTimeout=1000)

            def get_src_js():
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

            def get_href_js():
                return """
                           function get_src_or_href_sec_auto(nodes) {
                               let result = [];
                               for (let node of nodes) {
                                   let href = node.getAttribute("href");
                                   if (href) {
                                       base = location.protocol + location.host;
                                       url=new URL(href, base).href;
                                       result.push(url)
                                   }
                               }
                               return result;
                           }
                       """

            links_src = await page.querySelectorAllEval("[src]", get_src_js())
            links_href = await page.querySelectorAllEval("[href]", get_href_js())
            links_src.extend(links_href)
            for i in links_src:
                HttpData.save(i)
            try:
                await page.close()
                return self.url
            except BaseException as err:
                return f'close_newpage:{err}'
        except BaseException as err:
            return f'newpage:{err}'


class Browser(Process):
    system = ''
    pid = 0

    def __init__(self, urls, return_list):
        Process.__init__(self)
        self.urls = urls
        self.return_list = return_list

    # 封装了kill（）方法杀死chrome主进程，让init 1进程接管其僵尸子进程处理僵尸进程
    def kill(self, name=''):
        if self.system == 'Windows':
            # win平台
            subprocess.Popen("taskkill /F /IM chrome.EXE", shell=True)
        else:
            # linux平台# 查看进程是否存在
            if self.pid > 0 and psutil.pid_exists(self.pid):
                # 查看进程状态是否是运行
                p = psutil.Process(self.pid)
                print('浏览器状态：%s' % p.status())
                if p.status() != psutil.STATUS_ZOMBIE:
                    try:
                        pgid = os.getpgid(self.pid)
                        # 强制结束
                        os.kill(self.pid, signal.SIGKILL)
                        # os.kill(pgid, signal.SIGKILL)
                        print("结束进程：%d" % self.pid)
                        print("父进程是：%d" % pgid)
                        print("浏览器状态：%d" % self.browser.process.wait())
                    except BaseException as err:
                        print("close: {0}".format(err))
                del p
            # 查看是否还有其他进程
            for proc in psutil.process_iter():
                if name in proc.name():
                    try:
                        pgid = os.getpgid(proc.pid)
                        os.kill(proc.pid, signal.SIGKILL)
                        print(
                            '已杀死pid:%d的进程pgid：%d名称：%s' %
                            (proc.pid, pgid, proc.name()))
                        del pgid
                    except BaseException as err:
                        print("kill: {0}".format(err))
        time.sleep(3)
    # 新建一个浏览器

    async def new_browser(self):
        try:
            self.browser = await launch(
                {
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
                    'dumpio': True,
                    'autoClose': True,
                    'handleSIGTERM': True,
                    'handleSIGHUP': True,
                }
            )
        except BaseException as err:
            print(f'launch:{err}')
        print('-----打开浏览器-----')

    async def open(self):
        await self.new_browser()
        self.pid = self.browser.process.pid
        try:
            tasks = [
                asyncio.ensure_future(
                    Page(
                        url,
                        self.browser).run()) for url in self.urls]
            for task in asyncio.as_completed(tasks):
                result = await task
                print(f'Task ret:{result}')
            del tasks[:]
        except BaseException as err:
            print(f'open:{err}')
        await self.browser.close()

    def run(self):
        HttpData.init()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.open())
        self.return_list.extend(HttpData.get())
        print('----关闭浏览器----')
        self.kill('chrom')


class Morequest:
    def __init__(self):
        self.visited = set()  # 爬取过的URL
        self.unvisit = set()  # 未爬取的URL

    def filter(self, url):
        if url.split('.')[-1] in cfg.get('spider', 'static').split(','):
            return False
        elif url.startswith('mail'):
            return False
        if urlparse(url).netloc != self.domain:
            return False
        else:
            return True
    @Timer
    def run(self):
        url = 'http://www.tit.edu.cn/'
        self.domain = urlparse(url).netloc
        self.unvisit.add(url)
        while len(self.unvisit) != 0:
            print(f'未爬取队列URL数目{len(self.unvisit)}')
            self.unvisit = self.unvisit - self.visited
            manager = Manager()
            return_list = manager.list()
            p = Browser(self.unvisit, return_list)
            p.start()
            p.join()
            if p.is_alive():
                p.terminate()
                print('强制关闭子进程')
            else:
                print('子进程已关闭')
            # 更新爬取过的List
            for j in self.unvisit:
                self.visited.add(j)
            for i in return_list:
                if i not in self.unvisit and self.filter(i):
                    self.unvisit.add(i)
            del p
            del return_list[:]
            gc.collect()
        print('最终结果')
        print(len(self.visited))
        print(self.visited)


te = Morequest()
te.run()
