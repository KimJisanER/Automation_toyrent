from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome('./chromedriver')

out_update=['로디맥스 호핑말','뽀로로붕붕카', '꼬꼬맘', '공룡발자국']
in_update=['만능놀이 야리따이호다이', '코니스 에듀테이블']

try:

    # 로그인
    driver.get("https://jeonjuscc.or.kr/2018/bbs/login.php")
    time.sleep(2)
    elem = driver.find_element_by_name('mb_id')
    elem.send_keys('*****')
    elem = driver.find_element_by_name('mb_password')
    elem.send_keys('***********')
    elem.send_keys(Keys.RETURN)

    time.sleep(2)

    driver.get("https://jeonjuscc.or.kr/2018/bbs/board.php?bo_table=care_3_3")

#대여중으로 바꿀 품목 처리
    for i in range(len(out_update)):
        # 검색
        elem = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[3]/fieldset/form/input[4]')
        ac = ActionChains(driver)
        ac.move_to_element(elem)
        ac.click()

        ac.send_keys(out_update[i])
        # elem.submit()
        ac.perform()
        elem.send_keys(Keys.RETURN)

        time.sleep(2)
        try:
            # 첫번째 사진 누르기
            driver.find_elements_by_css_selector(
                '#gall_ul > li > div > div.gall_con > div.gall_text_href > a.bo_tit > b')[
                0].click()
            # 수정 누르기
            driver.find_elements_by_css_selector('#bo_v_top > ul.bo_v_left > li:nth-child(1) > a')[0].click()
            # 대여 여부 수정하기

            select = Select(driver.find_element_by_css_selector('#autosave_wrapper\ write_div > select'))
            # select box에서 index 1 이 대여
            select.select_by_index(1)
            # 작성완료
            driver.find_elements_by_css_selector('#btn_submit')[0].click()
            # 목록으로 복귀
            driver.find_elements_by_css_selector('#bo_v_top > ul.bo_v_com > li:nth-child(1) > a')[0].click()

        except Exception as e:
            print('오류 품목: ',out_update[i])
            print(e)
            driver.get("https://jeonjuscc.or.kr/2018/bbs/board.php?bo_table=care_3_3")
    print('대여중 업데이트 완료')

# 대여가능으로 바꿀 품목 처리

    for i in range(len(in_update)):
        # 검색
        elem = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[3]/fieldset/form/input[4]')
        ac = ActionChains(driver)
        ac.move_to_element(elem)
        ac.click()

        ac.send_keys(in_update[i])
        # elem.submit()
        ac.perform()
        elem.send_keys(Keys.RETURN)

        time.sleep(2)
        try:
            # 첫번째 사진 누르기
            driver.find_elements_by_css_selector(
                '#gall_ul > li > div > div.gall_con > div.gall_text_href > a.bo_tit > b')[
                0].click()
            # 수정 누르기
            driver.find_elements_by_css_selector('#bo_v_top > ul.bo_v_left > li:nth-child(1) > a')[0].click()
            # 대여 여부 수정하기

            select = Select(driver.find_element_by_css_selector('#autosave_wrapper\ write_div > select'))
            # select box에서 index 0 이 대여가능
            select.select_by_index(0)
            # 작성완료
            driver.find_elements_by_css_selector('#btn_submit')[0].click()
            # 목록으로 복귀
            driver.find_elements_by_css_selector('#bo_v_top > ul.bo_v_com > li:nth-child(1) > a')[0].click()

        except Exception as e:
            print('오류 품목: ',in_update[i])
            print(e)
            driver.get("https://jeonjuscc.or.kr/2018/bbs/board.php?bo_table=care_3_3")

except Exception as e:
    print('오류발생')
    print(e)
