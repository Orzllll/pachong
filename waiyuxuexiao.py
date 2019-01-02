from lxml import etree
from selenium import webdriver
import time
from PIL import Image
import hashlib
import requests

while True:
  # 构建浏览器
  browser = webdriver.Chrome('C:/Users/20744/Downloads/chromedriver_win32/chromedriver.exe')

  # browser.get("http://jwgl.zisu.edu.cn/login.jsp")
  browser.get("http://jwgl.zisu.edu.cn/login.jsp")
  #账号
  browser.find_element_by_xpath('//table[@class="font-b"]/tbody/tr[1]/td[2]/input[1]').clear()
  browser.find_element_by_xpath('//table[@class="font-b"]/tbody/tr[1]/td[2]/input[1]').send_keys("17070501031")

  #密码
  browser.find_element_by_xpath('//table[@class="font-b"]/tbody/tr[2]/td[2]/input[1]').clear()
  browser.find_element_by_xpath('//table[@class="font-b"]/tbody/tr[2]/td[2]/input[1]').send_keys("17070501031")

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

  Intercept_Verification_Code(browser, "D:/验证码.png", '//*[@id="vchart"]')

  # 登录若快
  Username = 'Orz_TvT'
  Password = 'zx123456ZX'
  rc = RClient(Username, Password, "81790", "0ddf5e900d854c17a66d7c1d8b7ecf55")

  with open("D:/验证码.png", 'rb') as m:
      im = m.read()
      result = rc.rk_create(im, 3040)
      print("识别结果:", result["Result"])

  #验证码
  browser.find_element_by_xpath('//table[@class="font-b"]/tbody/tr[3]/td[2]/input[1]').clear()
  browser.find_element_by_xpath('//table[@class="font-b"]/tbody/tr[3]/td[2]/input[1]').send_keys(result["Result"])

  browser.find_element_by_xpath('//*[@id="btnSure"]').click()

  time.sleep(3)

  # 定位当前页面
  print(browser.current_url)
  u = browser.current_url
  u1 = "http://jwgl.zisu.edu.cn/login.jsp"

  # 如果页面没变
  if u == u1:
      print("未能正确登陆 重新载入")
      browser.quit()
      continue
  try:
    browser.switch_to.frame(browser.find_element_by_xpath('/html/frameset/frame[2]'))
  except:
      print("页面出错 重新载入")
      browser.quit()
      continue
  else:
   browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="op_frame"]/frame[3]'))
  # browser.switch_to.default_content()
  browser.find_element_by_xpath('//*[@id="divCoHome"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tbody/tr/td/a').click()
  browser.switch_to.default_content()

  browser.switch_to.frame(browser.find_element_by_xpath('/html/frameset/frame[2]'))
  browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="op_frame"]/frame[3]'))
  html=etree.HTML(browser.page_source)
  LIST_tr = html.xpath('/html/body/table[5]/tbody/tr/td/table/tbody/tr')

  if len(LIST_tr)>0:
      LIST_tr = html.xpath('/html/body/table[4]/tbody/tr/td/table/tbody/tr')
      #
      # 检查一下长度是否正常
      if len(LIST_tr) > 0:
          for tr in LIST_tr:
              content = tr.xpath('td/text()')
              # print(content)
              for td in content:
                  print(td.strip())
                  # td.replace("\n\t\xa",'')
              # print("===============================")
          # browser.refresh()
          # browser.switch_to.frame(browser.find_element_by_xpath('/html/frameset/frame[2]'))
          # browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="op_frame"]/frame[3]'))
          # # browser.switch_to.default_content()
          # browser.find_element_by_xpath('//*[@id="divCoHome"]/table/tbody/tr/td[1]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tbody/tr/td/a').click()
          # browser.switch_to.default_content()
          # browser.switch_to.frame(browser.find_element_by_xpath('/html/frameset/frame[2]'))
          # browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="op_frame"]/frame[1]'))
          # browser.find_element_by_xpath('/html/body/form/table/tbody/tr/td/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/a').click()
          # browser.switch_to.default_content()
          # browser.switch_to.frame(browser.find_element_by_xpath('/html/frameset/frame[2]'))
          # browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="op_frame"]/frame[3]'))
          # html = etree.HTML(browser.page_source)
          # LIST_tr = html.xpath('/html/body/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr')
          #
          # if len(LIST_tr)>0:
          #     LIST_tr = html.xpath('/html/body/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr')
          #     for tr in LIST_tr:
          #         content = tr.xpath('td/text()')
          #         # print(content)
          #         for td in content:
          #             # print(td.strip())
          #             td.replace("\n\t\xa0",'')
          #             print(content)
          #         # print("===============================")
          # else:
          #   print("未刷新出内容,10秒后,程序将重启...")
          #   # browser.quit()
      else:
          print("未刷新出内容,10秒后,程序将重启...")
          browser.quit()
      # browser.refresh()
  else:
      print("未刷新出内容,10秒后,程序将重启...")
      browser.quit()
      time.sleep(10)
      continue

  browser.refresh()

  browser.switch_to.frame(browser.find_element_by_xpath('/html/frameset/frame[2]'))
  browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="op_frame"]/frame[3]'))
  # browser.switch_to.default_content()
  browser.find_element_by_xpath('//*[@id="divCoHome"]/table/tbody/tr/td[1]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td/table[2]/tbody/tr/td/a').click()
  browser.switch_to.default_content()
  browser.switch_to.frame(browser.find_element_by_xpath('/html/frameset/frame[2]'))
  browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="op_frame"]/frame[1]'))
  browser.find_element_by_xpath('/html/body/form/table/tbody/tr/td/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/a').click()
  browser.switch_to.default_content()
  browser.switch_to.frame(browser.find_element_by_xpath('/html/frameset/frame[2]'))
  browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="op_frame"]/frame[3]'))
  html = etree.HTML(browser.page_source)
  LIST_tr = html.xpath('/html/body/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr')

  if len(LIST_tr)>0:
      LIST_tr = html.xpath('/html/body/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr')
      for tr in LIST_tr:
          content = tr.xpath('td/text()')
          # print(content)
          for td in content:
              # print(td.strip())
              td.replace("\n\t\xa0",'')
              print(td.strip())
              # print(content)
          print("===============================")
  else:
      print("未刷新出内容,10秒后,程序将重启...")
      browser.quit()
      continue
  browser.quit()
  print("该学生信息已爬取，10秒后开始下一位")
  time.sleep(10)