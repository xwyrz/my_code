import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import logging
import os
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


account = '账户'
passwd = '密码'
vps_host = 'www.google.com'
code = 'BF2022-50'
cart = 'https://billing.spartanhost.net/cart.php?gid=25'
login_url = 'https://billing.spartanhost.net/clientarea.php'

timeout = 60

browser = uc.Chrome()
browser.set_page_load_timeout(timeout)


def alert(msg, t):
    for i in range(t):
        # osx
        try:
            os.system(f'say {msg}')
        except:
            pass


def id_exists(_id):
    try:
        return browser.find_element(by=By.ID, value=_id)
    except:
        return None


def try_get_by_xpath(xpath):
    try:
        return browser.find_element(by=By.XPATH, value=xpath)
    except:
        return None


def wait_cl(_id, timeout):
    """
    wait async el
    :param _id:
    :param timeout:
    :return:
    """
    while True:
        if timeout < 0:
            raise Exception("wait el: {} timeout".format(_id))
        try:
            return browser.find_element(by=By.CLASS_NAME, value=_id)
        except:
            pass
        timeout -= 1
        time.sleep(1)


def wait_el(_id, timeout):
    """
    wait async el
    :param _id:
    :param timeout:
    :return:
    """
    while True:
        if timeout < 0:
            return None
        try:
            return browser.find_element(by=By.ID, value=_id)
        except:
            pass
        timeout -= 1
        time.sleep(1)


def wait_el_by_xpath(xp, timeout):
    while True:
        if timeout < 0:
            raise None
        try:
            return browser.find_element(by=By.XPATH, value=xp)
        except:
            pass
        timeout -= 1
        time.sleep(1)


def login():
    browser.get(login_url)
    email = wait_el('inputEmail', timeout)
    if email is None:
        raise Exception("email not found")
    email.click()
    email.send_keys(account)
    passwd_input = browser.find_element(by=By.ID, value='inputPassword')
    passwd_input.clear()
    passwd_input.click()
    passwd_input.send_keys(passwd)
    browser.find_element(by=By.ID, value='login').click()


def create_order() -> bool:
    browser.get(cart)
    # continue order

    continue_btn = id_exists('btnCompleteProductConfig')
    if not continue_btn:
        logging.info("out of stock")
        return False

    alert('order', 1)

    host = wait_el('inputHostname', timeout)
    if host is None:
        logging.info("host not found")
        return False
    host.send_keys(vps_host)
    logging.info("send_keys " + vps_host)

    # wait el load
    time.sleep(1)

    vpn = '/html/body/section[2]/div[1]/div/div/div/div[3]/form/div/div[1]/div[9]/div[2]/div/input'
    vpn = try_get_by_xpath(vpn)
    if vpn:
        vpn.click()

    vpn_text = '/html/body/section[2]/div[1]/div/div/div/div[3]/form/div/div[1]/div[9]/div[2]/input'
    vpn_text = try_get_by_xpath(vpn_text)
    if vpn_text:
        vpn_text.send_keys('yes')

    continue_btn.click()

    checkout_btn = wait_el('checkout', timeout)
    if checkout_btn is None:
        print('checkout timeout')
        return False

    if code:
        code_text = wait_el('inputPromotionCode', 5)
        if code_text:
            code_text.send_keys(code)
        v_code_btn = browser.find_element(by=By.NAME, value='validatepromo')
        v_code_btn.click()

        res = wait_el_by_xpath("/html/body/section[2]/div[1]/div/div/div/div[3]/div[2]/div[1]/div[1]", timeout)
        if res:
            if "not exist" in res.text:
                print('code not exist')
                return False

    checkout = wait_el('checkout', timeout)
    checkout.click()
    logging.info('check order success')

    accepttos = wait_el('iCheck-accepttos', timeout)
    accepttos.click()

    wait_el('btnCompleteOrder', 5).click()
    logging.info('create order success')
    time.sleep(30)


if __name__ == '__main__':
    login()
    while True:
        try:
            if create_order():
                # return
                alert('buy buy buy', 5)
                pass
            time.sleep(5)
        except:
            import traceback
            traceback.print_exc()
            logging.info('retry...')
            continue
