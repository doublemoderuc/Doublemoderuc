from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, TimeoutException
from itertools import product
import pandas as pd
# from time import sleep
# from random import uniform


def get_articles(n_years=10, largest_index=30):
    # 生成所有的文章号
    years = [str(year) for year in range(2020 - n_years, 2021)]
    months = ['0' + str(month) for month in range(1, 10)] + [str(month) for month in range(10, 13)]
    indexes = ['0' + str(index) for index in range(10)] + [str(index) for index in range(10, largest_index + 1)]

    articles_ = []
    for month, index in product(months[8:], indexes):
        articles_.append(str(2020 - n_years) + month + '0' + index)
    for year, month, index in product(years[1:-1], months, indexes):
        articles_.append(year + month + '0' + index)
    for month, index in product(months[:8], indexes):
        articles_.append('2020' + month + '0' + index)

    return articles_


def get_article_info(article_):
    global driver, wait  # 将driver设为全局变量并在此引入，可以避免多次开关浏览器
    driver.get('https://kns8.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFD&filename=TJYJ' + article_)

    # 若作者为空则跳过文章
    authors = driver.find_elements_by_css_selector('#authorpart a')
    if not authors:
        return pd.DataFrame()

    # 若摘要含有"<正>"则跳过文章（通常为本期导读）
    try:
        abstract = driver.find_element_by_css_selector('#ChDivSummary').text
    except NoSuchElementException:
        return pd.DataFrame()
    if '<正>' in abstract:
        return pd.DataFrame()

    # 如有，删除作者的右上角数字
    try:
        authors = [author.text[:-len(author.find_element_by_css_selector('sup').text)] for author in authors]
    except NoSuchElementException:
        authors = [author.text for author in authors]
    authors = '; '.join(authors)

    # 获取标题
    try:
        title = driver.find_element_by_css_selector('h1').text
    except NoSuchElementException:
        title = None

    # 获取地址
    departments = driver.find_elements_by_css_selector('a.author')
    if not departments:
        departments = driver.find_elements_by_css_selector('#authorpart+ h3 span')
    departments = [department.text for department in departments]
    if departments and departments[0][1] == '.':
        departments = [department[3:] for department in departments]
    departments = '; '.join(departments)

    # 获取期刊名
    try:
        journal_name = driver.find_element_by_css_selector('.top-tip a:nth-child(1)').text
    except NoSuchElementException:
        journal_name = None

    # 获取发表时间
    try:
        publish_time = driver.find_element_by_css_selector('.top-tip a+ a').text
    except NoSuchElementException:
        publish_time = None

    # 获取页码
    try:
        pages = driver.find_element_by_css_selector('.total-inform span:nth-child(2)').text.replace('页码：', '')
    except NoSuchElementException:
        pages = None

    # 获取页数
    try:
        n_page = driver.find_element_by_css_selector('.total-inform span:nth-child(3)').text
        n_page = int(n_page.replace('页数：', ''))
    except NoSuchElementException:
        n_page = None

    # 获取关键词
    keywords = driver.find_elements_by_css_selector('.keywords a')
    keywords = '; '.join([keyword.text.replace(';', '') for keyword in keywords])

    # 获取基金资助
    funds = driver.find_elements_by_css_selector('.funds a')
    funds = '; '.join([fund.text.replace('；', '') for fund in funds])

    # 获取DOI
    try:
        DOI = driver.find_element_by_css_selector('.top-space:nth-child(1) p').text
    except NoSuchElementException:
        DOI = None

    # 获取专辑
    try:
        album = driver.find_element_by_css_selector('.top-space:nth-child(2) p').text
    except NoSuchElementException:
        album = None

    # 获取专题
    try:
        theme = driver.find_element_by_css_selector('.top-space:nth-child(3) p').text
    except NoSuchElementException:
        theme = None

    # 获取分类号
    try:
        category = driver.find_element_by_css_selector('.top-space:nth-child(4) p').text
    except NoSuchElementException:
        category = None

    # 获取下载数
    try:
        n_download = driver.find_element_by_css_selector('#DownLoadParts span:nth-child(1)').text
        n_download = int(n_download.replace('下载：', ''))
    except NoSuchElementException:
        n_download = None

    # 获取被引数
    while True:
        try:
            n_cited = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#rc3'))).text
            n_cited = int(n_cited[1:-1])
            break
        except TimeoutException:
            driver.refresh()
        except (NoSuchElementException, ValueError):
            n_cited = None
            break

    # 获取引用数
    while True:
        try:
            n_cite = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#rc1'))).text
            n_cite = int(n_cite[1:-1])
            break
        except TimeoutException:
            driver.refresh()
        except (NoSuchElementException, ValueError):
            n_cite = None
            break

    # 获取参考文献
    references = []
    if n_cite and n_cite > 0:
        while True:
            try:
                driver.switch_to.frame('frame1')
                essay_boxes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'essayBox')))
                for i in range(len(essay_boxes)):
                    while True:
                        additional_references = essay_boxes[i].find_elements_by_css_selector('li')
                        additional_references = [
                            additional_reference.text[4:] for additional_reference in additional_references
                        ]
                        references.extend(additional_references)

                        try:
                            next_page = essay_boxes[i].find_element_by_link_text('下一页')
                            driver.execute_script("arguments[0].click();", next_page)
                            essay_boxes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'essayBox')))
                        except NoSuchElementException:
                            break
                break
            except TimeoutException:
                driver.refresh()
            except NoSuchFrameException:
                break
    references = ';; '.join(references)

    # 生成字典
    article_info_ = {
        '标题': title,
        '作者': authors,
        '地址': departments,
        '期刊名': journal_name,
        '发表时间': publish_time,
        '页码': pages,
        '页数': n_page,
        '摘要': abstract,
        '关键词': keywords,
        '基金资助': funds,
        'DOI': DOI,
        '专辑': album,
        '专题': theme,
        '分类号': category,
        '下载数': n_download,
        '被引数': n_cited,
        '引用数': n_cite,
        '参考文献': references
    }

    # 由字典生成数据框
    article_info_ = pd.DataFrame(article_info_, index=[article_])

    # 防止网页爬取速度过快
    # sleep(uniform(1, 10))

    return article_info_


if __name__ == '__main__':
    articles = get_articles()

    article_infos = pd.DataFrame()
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    for article in articles:
        article_info = get_article_info(article)
        article_infos = article_infos.append(article_info)
    driver.quit()

    article_infos.to_csv('tjyj.csv', index=False, encoding='utf_8_sig')
