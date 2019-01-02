from lxml import etree
from selenium import webdriver
import time
from PIL import Image
import hashlib
import requests


# 构建浏览器
browser = webdriver.Chrome('C:/Users/20744/Downloads/chromedriver_win32/chromedriver.exe')

while True:

    # browser.get("http://jwgl.zisu.edu.cn/login.jsp")
    browser.get("http://www.gdjw.zjut.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t=1544528996713")
    #账号
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/form/div[1]/div/input').clear()
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/form/div[1]/div/input').send_keys("201607500107")

    #密码
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/form/div[2]/div/input[2]').clear()
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/form/div[2]/div/input[2]').send_keys("fgy1656411505")


    # 截屏验证码
    def Intercept_Verification_Code(Browser, Pic_Name, xpath):
        # 截取浏览器全图
        Browser.get_screenshot_as_file(Pic_Name)
        # 获取验证码元素位置
        element = Browser.find_element_by_xpath(xpath)
        left = int(element.location['x'])
        top = int(element.location['y'])
        right = int(element.location['x'] + element.size['width'])
        bottom = int(element.location['y'] + element.size['height'])
        # 通过Image库截取
        im = Image.open(Pic_Name)
        im = im.crop((left, top, right, bottom))
        im.save(Pic_Name)


    # 识别验证码
    class RClient(object):
        def __init__(self, username, password, soft_id, soft_key):
            self.username = username
            self.password = hashlib.md5(password.encode(encoding='utf-8')).hexdigest()
            self.soft_id = soft_id
            self.soft_key = soft_key
            self.base_params = {
                'username': self.username,
                'password': self.password,
                'softid': self.soft_id,
                'softkey': self.soft_key,
            }
            self.headers = {
                'Connection': 'Keep-Alive',
                'Expect': '100-continue',
                'User-Agent': 'ben',
            }

        def rk_create(self, im, im_type, timeout=60):
            """
            im: 图片字节
            im_type: 题目类型
            """
            params = {
                'typeid': im_type,
                'timeout': timeout,
            }
            params.update(self.base_params)
            files = {'image': ('a.jpg', im)}
            r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
            return r.json()

        def rk_report_error(self, im_id):
            """
            im_id:报错题目的ID
            """
            params = {
                'id': im_id,
            }
            params.update(self.base_params)
            r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
            return r.json()


    #验证码储存
    Intercept_Verification_Code(browser, "D:/验证码.png", '//*[@id="yzmPic"]')

    # 登录若快
    Username = 'Orz_TvT'
    Password = 'zx123456ZX'
    rc = RClient(Username, Password, "81790", "0ddf5e900d854c17a66d7c1d8b7ecf55")

    with open("D:/验证码.png", 'rb') as m:im = m.read()
    result = rc.rk_create(im, 3040)
    print("识别结果:", result["Result"])

    #验证码
    browser.find_element_by_xpath('//*[@id="yzm"]').clear()
    browser.find_element_by_xpath('//*[@id="yzm"]').send_keys(result["Result"])

    #登陆
    browser.find_element_by_xpath('//*[@id="dl"]').click()

    #休息下
    time.sleep(3)

    # 定位当前页面
    print(browser.current_url)
    u = browser.current_url
    u1 = "http://www.gdjw.zjut.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t=1544528996713"

    #如果页面没变
    if u == u1 :
        print("未能正确登陆 重新载入")
        continue

    #打开信息查询
    browser.find_element_by_xpath('//nav[@id="cdNav"]/ul/li[4]/a/b').click()

    #查询个人信息
    browser.find_element_by_xpath('//nav[@id="cdNav"]/ul/li[4]/ul/li[1]/a').click()
    browser.switch_to.default_content()

    #定位当前页面句柄
    all_handles = browser.window_handles

    #测试打印内容
    print(all_handles)

    # 切到标签2
    browser.switch_to.window(all_handles[1])

    # 爬取
    print("进行爬取")
    html = etree.HTML(browser.page_source)
    LIST_div = html.xpath('/html/body/div/div/div/form/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/div/div')
    基本信息_列表 = html.xpath(
    '/html/body/div/div/div/form/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/div/div/div/label/text()')

    for 基本信息, div in zip(基本信息_列表, LIST_div):
        content = div.xpath('.//p/text()')
    # print(content)
    for div in content:
        div.replace("\n\t\xa0", '')
        print(基本信息.strip(), div.strip())

    # print("===============================")

    #切换到第二页
    browser.find_element_by_xpath('//*[@id="tab_xsxxgl"]/li[2]/a').click()

    #休息下
    time.sleep(3)

    # 爬取
    print("进行爬取")
    html = etree.HTML(browser.page_source)
    LIST_div = html.xpath('/html/body/div[1]/div/div/form/div/div[2]/div/div/div/div/div[2]/div[2]/div')
    基本信息_列表 = html.xpath('/html/body/div[1]/div/div/form/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/label/text()')

    for 基本信息, div in zip(基本信息_列表, LIST_div):
        content = div.xpath('.//p/text()')
    # print(content)
    for div in content:
        div.replace("\n\t\xa0", '')
        print(基本信息.strip(), div.strip())

    # print("===============================")

    # 爬取完毕关闭
    browser.close()

    #定位当前句柄
    all_handles = browser.window_handles

    #打印测试当前句柄
    print(all_handles)

    #切换第一页
    browser.switch_to.window(all_handles[0])

    #打开信息查询
    browser.find_element_by_xpath('//nav[@id="cdNav"]/ul/li[4]/a/b').click()

    #查询学生课表
    browser.find_element_by_xpath('//nav[@id="cdNav"]/ul/li[4]/ul/li[2]/a').click()

    #定位当前句柄
    all_handles = browser.window_handles

    #打印测试当前句柄
    print(all_handles)

    # 切到课程
    browser.switch_to.window(all_handles[1])

    #打开学期
    browser.find_element_by_xpath('//div[@id="xqm1_chosen"]').click()

    #选择第一学期
    browser.find_element_by_xpath('//div[@id="xqm1_chosen"]/div/ul/li[2]').click()

    #查询
    browser.find_element_by_xpath('//*[@id="search_go1"]').click()

    #休息下
    time.sleep(3)

    # 爬取课表时间
    print("进行爬取")
    count = 0
    html=etree.HTML(browser.page_source)
    LIST_tr=html.xpath('/html/body/div[1]/div/div/div[2]/div/table/tbody/tr')
    for tr in LIST_tr:
        content=tr.xpath('.//span/text()')
    for tr in content:
        tr.replace("\n\t\xa0",'')
        print(tr.strip())

    # 爬取课表内容
    print("进行爬取")
    count = 0
    html=etree.HTML(browser.page_source)
    LIST_tr=html.xpath('/html/body/div[1]/div/div/div[2]/div/table/tbody/tr[3]/td')
    for tr in LIST_tr:
        content=tr.xpath('.//font/text()')
    for tr in content:
        tr.replace("\n\t\xa0",'')
        print(tr.strip())

    # 爬取完毕关闭
    browser.close()

    #定位当前句柄
    all_handles = browser.window_handles

    #打印测试当前句柄
    print(all_handles)

    #切换第一页
    browser.switch_to.window(all_handles[0])

    # 单击头像
    browser.find_element_by_xpath('/html/body/div[1]/div/ul/li[2]/a').click()

    #休息下
    time.sleep(3)

    #点击注销
    browser.find_element_by_xpath('//*[@id="exit"]').click()

    #获取弹窗
    Alert=browser.switch_to.alert

    #点击确认
    Alert.accept()

    print("该学生信息已爬取，10秒后开始下一位")
    time.sleep(10)
    continue

# （课表鬼才写法 未完成的算法）
# # 爬取
# print("进行爬取")
# count = 0
# html=etree.HTML(browser.page_source)
# LIST_tr=html.xpath('/html/body/div[1]/div/div/div[2]/div/table/tbody/tr')
# LTST_td12=html.xpath('/html/body/div[1]/div/div/div[2]/div/table/tbody/tr[3]/td[3]')
# for tr in LIST_tr:
#     content=tr.xpath('.//span/text()')
# #     content=tr.xpath('.//font/text()')
#     #print(content)
#     for tr in content:
#         count = count+1
#         #课表第一行星期
#         if 2 < count and count < 12:
#             tr.replace("\n\t\xa0",'')
#             print(tr.strip(),"\t\t\t",end="")
#             if count == 11:
#                 print("\t")
#         #课表上午第一节课
#         elif 12 <= count and count < 14:
#             #print(count)
#             tr.replace("\n\t\xa0",'')
#             print(tr.strip(),"\t",end="")
#             if count == 13:
#                 #开始遍一二节课程
#                 #顶一个计数器
#                 ke=0
#                 for td12 in LTST_td12:
#                     content12=td12.xpath('.//font/text()')
#                     for td12 in content12:
#                         ke = ke+1
#                         if 1 == ke :
#                             td12.replace("\n\t\xa0",'')
#                             print(td12.strip())
#                         elif 1 < ke :
#                             td12.replace("\n\t\xa0",'')
#                             print("\t\t",td12.strip())
#                 print("\n")
#         #课表上午第二三四节课
#         elif 14 <= count and count < 17:
#             tr.replace("\n\t\xa0",'')
#             print("\t",tr.strip())
#         #课表中午第五节课
#         elif 17  <= count and count < 19:
#             tr.replace("\n\t\xa0",'')
#             print(tr.strip(),"\t",end="")
#             if count == 18:
#                 print("\n")
#         #课表下午第六节课
#         elif 19  <= count and count < 21:
#             tr.replace("\n\t\xa0",'')
#             print(tr.strip(),"\t",end="")
#             if count == 20:
#                 print("\n")
#          #课表下午第七八九节课
#         elif 21  <= count and count < 24:
#             print("\t",tr.strip())
#          #课表晚上第十节课
#         elif 24  <= count and count < 26:
#             tr.replace("\n\t\xa0",'')
#             print(tr.strip(),"\t",end="")
#             if count == 25:
#                 print("\n")
#         #课表晚上剩余课
#         elif 26  <= count and count < 28:
#             print("\t",tr.strip())
#     #print("===============================")
