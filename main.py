from ast import If
from tkinter.messagebox import NO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import csv
import unicodedata
import re
import sys
import argparse

# select_jenis = driver.find_element(by=By.NAME, value='ctl00$MainContent$ddlJenisProduk')
# options = [x for x in select_jenis.find_elements(by=By.TAG_NAME, value='option')]

# for el in options:
#   with open('options.txt', 'a') as f:
#     f.write(el.text + '\n')
#     print(el.text)

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def crawl(jenis=None, bisnis=None, provinsi=None, produk=None):
  driver = webdriver.Chrome('chromedriver.exe')
  base_url = 'http://info.halal.go.id/cari/'
  driver.get(base_url)

  if bisnis is not None:
    business_select = driver.find_element(by=By.NAME, value='ctl00$MainContent$tbPU')
    business_select.send_keys(bisnis)

  if produk is not None:
    product_select = driver.find_element(by=By.NAME, value='ctl00$MainContent$tbNamaProduk')
    product_select.send_keys(produk)

  page = 1
  while True:
    if page == 1:
      element_provinsi = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.NAME, 'ctl00$MainContent$ddlProv'))
      )
      select_provinsi = Select(element_provinsi)
      select_provinsi.select_by_visible_text(provinsi)
      if jenis is not None:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'ctl00$MainContent$ddlJenisProduk'))
        )
        select = Select(element)
        select.select_by_visible_text(jenis)
        filename = slugify(jenis) + '.csv'
      else:
        filename = 'data.csv'
      driver.find_element_by_css_selector('#MainContent_btnCari').click()
      headers = ['No', 'Jenis Produk', 'Nama Usaha', 'Provinsi', 'Skala', 'No Sertifikat', 'Masa Berlaku', 'Nama Produk']
      with open(filename, 'w') as f: 
        write = csv.writer(f) 
        write.writerow(headers)
      page = page + 1
    else:
      WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'Page$"+ str(page) +"')]"))).click()
      page = page + 1

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    content = soup.tbody
    extract = content.find_all(lambda tag: tag.name == 'tr' and not tag.attrs)
    print(extract)
    for e in extract[:-1] if len(extract) > 1 else extract:
      data = []
      col_1 = e.td
      no = col_1.get_text(strip=True)
      print(no)
      data.append(no)
      jenis_produk = col_1.next_sibling.text
      data.append(jenis_produk)
      nama_usaha = col_1.next_sibling.next_sibling.span.text
      data.append(nama_usaha)
      provinsi = col_1.next_sibling.next_sibling.span.next_sibling.next_sibling.next_sibling.text
      data.append(provinsi)
      skala = col_1.next_sibling.next_sibling.span.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
      data.append(skala)
      no_sertifikat = col_1.next_sibling.next_sibling.next_sibling.span.text
      data.append(no_sertifikat)
      masa_berlaku = col_1.next_sibling.next_sibling.next_sibling.span.next_sibling.next_sibling.next_sibling.text
      data.append(masa_berlaku)
      nama_produk = col_1.next_sibling.next_sibling.next_sibling.next_sibling.text
      data.append(nama_produk)

      with open(filename, 'a+', newline='') as f: 
        write = csv.writer(f) 
        write.writerow(data)
      print(data)

def main():
  parser = argparse.ArgumentParser(description='Menarik data produk/produsen halal dari web Sihalal')
  parser.add_argument('--jenis', help='jenis produk yang tersedia di pilihan di web Sihalal')
  parser.add_argument('--bisnis', help='pencarian berdasarkan nama pelaku usaha')
  parser.add_argument('--provinsi', help='provinsi yang tersedia di pilihan di web Sihalal')
  parser.add_argument('--produk', help='pencarian berdasarkan nama produk')
  args = parser.parse_args()

  if args.jenis:
    jenis = args.jenis
  else:
    jenis = None

  if args.bisnis:
    bisnis = args.bisnis
  else:
    bisnis = None
  
  if args.provinsi:
    provinsi = args.provinsi
  else:
    provinsi = 'Jawa Timur'

  if args.produk:
    produk = args.produk
  else:
    produk = None
  
  crawl(jenis=jenis, bisnis=bisnis, provinsi=provinsi, produk=produk)

if __name__ == '__main__':
  main()
