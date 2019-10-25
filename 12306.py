# -*- coding: utf-8 -*-
"""
@original author: liuyw
@i am ：zhuang
"""
import requests
from lxml import etree
from splinter.browser import Browser
from time import sleep
import traceback
from selenium import webdriver
import time, sys
import datetime

class huoche(object):
	#用户名，密码

	username = input("请输入用户名：")
	passwd=input("请输入密码：")

	# 车次，选择第几趟，0则从上之下依次点击
	order = 0

	##席位
	xb = u"一等座"
	pz = u"儿童票"

	"""网址"""
	ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"#进入买票的界面
	login_url = "https://kyfw.12306.cn/otn/login/init"#登入界面
	initmy_url = "https://kyfw.12306.cn/otn/view/index.html"#登入以后进入的界面
	buy = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
	
	def __init__(self):
		# 起始/终点站
		self.starts = input("请输入起始站：")
		self.ends = input("请输入终点站：")

		# 时间格式2018-01-19
		self.dtime = input("请输入启程的时间(时间格式2018-01-19）：")

	def login(self):
		self.driver.get(self.login_url)
		self.driver.implicitly_wait(10)
		self.driver.find_element_by_id("username").send_keys(self.username)
		# sleep(1)
		self.driver.find_element_by_id("password").send_keys(self.passwd)
		print(u"等待验证码，自行输入...")
		while True:
			if self.driver.current_url != self.initmy_url:
				sleep(1)
			else:
				break

	def start_time(self):#根据我们输入的时间，对应在网页中点击相应的位置来选择时间
		in_year = self.dtime.split('-')[0]
		in_month=self.dtime.split('-')[1]
		day = self.dtime.split('-')[2]

		# 获取当前的月份
		now_date = datetime.datetime.now().strftime('%Y-%m-%d')
		now_month = now_date.split('-')[1]

		if in_month == now_month:
			month = 1
		else:
			month = 2
		self.driver.find_element_by_xpath('/html/body/div[34]/div[{}]/div[2]/div[{}]/div'.format(month,day)).click()  # 选择启程时间

	def start(self):
		self.driver = webdriver.Chrome()
		self.driver.maximize_window()

		self.login()
		print("Finiahed!")
		sleep(1)
		self.driver.get(self.ticket_url)#去定票的页面

		try:
			print(u"购票页面开始...")
			# sleep(1)
			# 加载查询信息
			self.driver.find_element_by_xpath('//*[@id="fromStationText"]').click()#点击选择起始站的框框
			self.driver.find_element_by_xpath('//*[@id="ul_list1"]/li[@title="{}"]'.format(str(self.starts))).click()#选择起始站
			self.driver.find_element_by_xpath('//*[@id="toStationText"]').click()#点击选择终点站的框框
			self.driver.find_element_by_xpath('//*[@id="ul_list1"]/li[@title="{}"]'.format(str(self.ends))).click()#选择终点站
			self.driver.find_element_by_xpath('//*[@id="train_date"]').click()#点击选择启程日期的框框
			self.start_time()#根据我们前面输入的时间，对应在网页中点击相应的位置来选择时间
			print("完成起始地的选取！")
			# self.driver.reload()

			count = 0
			if self.order != 0:
				while self.driver.current_url == self.ticket_url:
					self.driver.find_element_by_xpath('//*[@id="query_ticket"]').click()
					count += 1
					print(u"循环点击查询... 第 %s 次" % count)
					# sleep(1)
					try:
						self.driver.find_elements_by_link_text(u"预订")[self.order - 1].click()
					except Exception as e:
						print(e)
						print(u"还没开始预订")
						continue
			else:
				while self.driver.current_url == self.ticket_url:
					self.driver.find_element_by_xpath('//*[@id="query_ticket"]').click()
					count += 1
					print(u"循环点击查询... 第 %s 次" % count)
					# sleep(0.8)
					try:
						for i in self.driver.find_elements_by_link_text(u"预订"):
							i.click()
							sleep(1)
					except Exception as e:
						print(e)
						print(u"还没开始预订 %s" % count)
						continue
			print(u"开始预订...")
			# sleep(3)
			# self.driver.reload()
			sleep(1)
			print(u'开始选择用户...')

			self.driver.find_element_by_xpath('//*[@id="normalPassenger_0"]').click()
			self.driver.find_element_by_xpath('//*[@id="qd_closeDefaultWarningWindowDialog_id"]').click()

			print(u"提交订单...")
			sleep(1)
			self.driver.find_element_by_xpath('//*[@id="seatType_1"]/option[2]').click()
			# sleep(1)
			# self.driver.find_elements_by_link_text(self.xb).click()
			sleep(1)
			self.driver.find_element_by_id('submitOrder_id').click()
			print(u"开始选座...")
			self.driver.find_element_by_id('1D').click()

			sleep(1.5)
			print(u"确认选座...")
			self.driver.find_element_by_id('qr_submit_id').click()

		except Exception as e:
			print(e)

if __name__ == '__main__':
	huoche = huoche()
	huoche.start()