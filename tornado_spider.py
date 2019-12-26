from urllib.parse import urljoin

from bs4 import BeautifulSoup
from tornado import gen, httpclient, ioloop, queues

base_url = "http://www.tornadoweb.org/en/stable"
concurrency = 3


# 获取url
async def get_url_links(url):
    response = await httpclient.AsyncHTTPClient().fetch("http://www.tornadoweb.org/en/stable")
    html = response.body.decode("utf8")
    soup = BeautifulSoup(html)
    # bs4不需要协程，cpu型，非io
    # urljoin：拼接url， url+相对路径
    links = [urljoin(base_url, a.get("href")) for a in soup.find_all("a", href=True)]
    return links


async def main():
    # 已经抓取过的url，存入set
    seen_set = set()
    # tornado提供的队列，非阻塞的queue，可以自动调用协程
    q = queues.Queue()

    async def fetch_url(current_url):
        # 抓取url的协程
        # 生产者
        if current_url in seen_set:
            return

        print("获取： {}".format(current_url))
        seen_set.add(current_url)
        next_urls = await get_url_links(current_url)
        for new_url in next_urls:
            # python3 加入 字符串 startswith， 以...开头的判断，返回bool
            if new_url.startswith(base_url):
                # 放入队列
                await q.put(new_url)

    async def worker():
        # 消费者
        async for url in q:
            # 从q中获取add的url
            if url is None:
                # 队列中为空时return，结束消费
                return
            try:
                await  fetch_url(url)
            except Exception as e:
                print(e)
            finally:
                # q中消费了一个
                q.task_done()

    # 放入初始url到队列， 从base_url开始抓取
    await q.put(base_url)

    # 启动协程
    workers = gen.multi([worker() for _ in range(concurrency)])
    await q.join()

    for _ in range(concurrency):
        await q.put(None)

    await workers

if __name__ == "__main__":
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)






