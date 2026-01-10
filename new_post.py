import time
import os
import asyncio
import aiohttp
from tqdm import tqdm
from googletrans import Translator

urls=['translate.google.ac', 'translate.google.ad', 'translate.google.ae',
                        'translate.google.al', 'translate.google.am', 'translate.google.as',
                        'translate.google.at', 'translate.google.az', 'translate.google.ba',
                        'translate.google.be', 'translate.google.bf', 'translate.google.bg',
                        'translate.google.bi', 'translate.google.bj', 'translate.google.bs',
                        'translate.google.bt', 'translate.google.by', 'translate.google.ca',
                        'translate.google.cat', 'translate.google.cc', 'translate.google.cd',
                        'translate.google.cf', 'translate.google.cg', 'translate.google.ch',
                        'translate.google.ci', 'translate.google.cl', 'translate.google.cm',
                        'translate.google.cn', 'translate.google.co.ao', 'translate.google.co.bw',
                        'translate.google.co.ck', 'translate.google.co.cr', 'translate.google.co.id',
                        'translate.google.co.il', 'translate.google.co.in', 'translate.google.co.jp',
                        'translate.google.co.ke', 'translate.google.co.kr', 'translate.google.co.ls',
                        'translate.google.co.ma', 'translate.google.co.mz', 'translate.google.co.nz',
                        'translate.google.co.th', 'translate.google.co.tz', 'translate.google.co.ug',
                        'translate.google.co.uk', 'translate.google.co.uz', 'translate.google.co.ve',
                        'translate.google.co.vi', 'translate.google.co.za', 'translate.google.co.zm',
                        'translate.google.co.zw', 'translate.google.com.af', 'translate.google.com.ag',
                        'translate.google.com.ai', 'translate.google.com.ar', 'translate.google.com.au',
                        'translate.google.com.bd', 'translate.google.com.bh', 'translate.google.com.bn',
                        'translate.google.com.bo', 'translate.google.com.br', 'translate.google.com.bz',
                        'translate.google.com.co', 'translate.google.com.cu', 'translate.google.com.cy',
                        'translate.google.com.do', 'translate.google.com.ec', 'translate.google.com.eg',
                        'translate.google.com.et', 'translate.google.com.fj', 'translate.google.com.gh',
                        'translate.google.com.gi', 'translate.google.com.gt', 'translate.google.com.hk',
                        'translate.google.com.jm', 'translate.google.com.kh', 'translate.google.com.kw',
                        'translate.google.com.lb', 'translate.google.com.ly', 'translate.google.com.mm',
                        'translate.google.com.mt', 'translate.google.com.mx', 'translate.google.com.my',
                        'translate.google.com.na', 'translate.google.com.ng', 'translate.google.com.ni',
                        'translate.google.com.np', 'translate.google.com.om', 'translate.google.com.pa',
                        'translate.google.com.pe', 'translate.google.com.pg', 'translate.google.com.ph',
                        'translate.google.com.pk', 'translate.google.com.pr', 'translate.google.com.py',
                        'translate.google.com.qa', 'translate.google.com.sa', 'translate.google.com.sb',
                        'translate.google.com.sg', 'translate.google.com.sl', 'translate.google.com.sv',
                        'translate.google.com.tj', 'translate.google.com.tr', 'translate.google.com.tw',
                        'translate.google.com.ua', 'translate.google.com.uy', 'translate.google.com.vc',
                        'translate.google.com.vn', 'translate.google.com', 'translate.google.cv',
                        'translate.google.cz', 'translate.google.de', 'translate.google.dj',
                        'translate.google.dk', 'translate.google.dm', 'translate.google.dz',
                        'translate.google.ee', 'translate.google.es', 'translate.google.eu',
                        'translate.google.fi', 'translate.google.fm', 'translate.google.fr',
                        'translate.google.ga', 'translate.google.ge', 'translate.google.gf',
                        'translate.google.gg', 'translate.google.gl', 'translate.google.gm',
                        'translate.google.gp', 'translate.google.gr', 'translate.google.gy',
                        'translate.google.hn', 'translate.google.hr', 'translate.google.ht',
                        'translate.google.hu', 'translate.google.ie', 'translate.google.im',
                        'translate.google.io', 'translate.google.iq', 'translate.google.is',
                        'translate.google.it', 'translate.google.je', 'translate.google.jo',
                        'translate.google.kg', 'translate.google.ki', 'translate.google.kz',
                        'translate.google.la', 'translate.google.li', 'translate.google.lk',
                        'translate.google.lt', 'translate.google.lu', 'translate.google.lv',
                        'translate.google.md', 'translate.google.me', 'translate.google.mg',
                        'translate.google.mk', 'translate.google.ml', 'translate.google.mn',
                        'translate.google.ms', 'translate.google.mu', 'translate.google.mv',
                        'translate.google.mw', 'translate.google.ne', 'translate.google.nf',
                        'translate.google.nl', 'translate.google.no', 'translate.google.nr',
                        'translate.google.nu', 'translate.google.pl', 'translate.google.pn',
                        'translate.google.ps', 'translate.google.pt', 'translate.google.ro',
                        'translate.google.rs', 'translate.google.ru', 'translate.google.rw',
                        'translate.google.sc', 'translate.google.se', 'translate.google.sh',
                        'translate.google.si', 'translate.google.sk', 'translate.google.sm',
                        'translate.google.sn', 'translate.google.so', 'translate.google.sr',
                        'translate.google.st', 'translate.google.td', 'translate.google.tg',
                        'translate.google.tk', 'translate.google.tl', 'translate.google.tm',
                        'translate.google.tn', 'translate.google.to', 'translate.google.tt',
                        'translate.google.us', 'translate.google.vg', 'translate.google.vu',
                        'translate.google.ws']

translator = Translator(service_urls=urls)

# 预加载中文字符范围
chinese_chars = set(chr(i) for i in range(0x4e00, 0x9fff + 1))

def is_chinese(text):
    return all(char in chinese_chars for char in text)

async def fetch_translation(session, text, src='en', dest='zh-cn'):
    retries = 5
    for attempt in range(retries):
        try:
            translated = await translator.translate(text, src=src, dest=dest).text
            if not translated or not is_chinese(translated):
                raise ValueError("Empty or invalid translation result")
            return translated
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"Translation failed after {retries} attempts: {e}")
                return text  # Fallback to the original text
    return text

async def translate_batch_async(batch, session):
    src, trans = batch.strip().split('\t', 1) if '\t' in batch else batch.strip().split(' ', 1)
    if not is_chinese(trans):
        translated = await fetch_translation(session, trans)
        return [f"{src}\t{translated}\n"]
    return [batch]

async def process_file_async(input_file, output_file):
    async with aiohttp.ClientSession() as session:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(output_file, 'w', encoding='utf-8') as output_f:
            tasks = []
            for line in lines:
                tasks.append(translate_batch_async(line, session))

            # 批量翻译所有行
            results = await asyncio.gather(*tasks)
            for result in results:
                output_f.writelines(result)

# 输入和输出目录
input_dir = r'F:\PythonProject\tranlate\output'
output_dir = r'F:\PythonProject\tranlate\filiter'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith("-en.txt"):
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, f"filtered_{filename}")

        if not os.path.isfile(input_file):
            continue

        print(f"Processing file: {input_file}")

        start_time = time.time()
        # 清空或创建输出文件
        open(output_file, 'w', encoding='utf-8').close()

        # 异步处理翻译任务
        asyncio.run(process_file_async(input_file, output_file))

        end_time = time.time()
        print(f"Translation completed for {filename} in {end_time - start_time:.2f} seconds.")
