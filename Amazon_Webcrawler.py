
# coding: utf-8



from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
executable_path ='/Users/madhuranagaonkar/Desktop/midterm/geckodriver'
driver = webdriver.Firefox(executable_path=executable_path)
# Wait to let webdriver complete the initialization
driver.wait = WebDriverWait(driver, 5)
def getReviews(page_url):
    reviews = []
    try:
        if page_url != None:
            driver.get(page_url)
            
            review_summary= driver.find_element_by_xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span')
            print(review_summary.get_attribute('innerText'))
            totalReviewsCount=int(review_summary.get_attribute('innerText'))
            print("total reviews: " + str(totalReviewsCount))
            i = 1
            while page_url != None:
                driver.get(page_url + str(i))
                i = i + 1
                soup= BeautifulSoup(driver.page_source, 'html.parser')
                divs =soup.select("div.a-section.review")
               
                if len(divs) == 0:
                    print ("Empty")
                    page_url = None
                else:
                    for idx, div in enumerate(divs):  
                        rating = None
                        comment = None
                        review = []
                        rating_tmp=div.find_all('span', {'class': 'a-icon-alt'})
                        if rating_tmp != []:
                           
                            rating = rating_tmp[0].get_text()
                            newrating=rating.replace(u"\xe2\x80\x99","'")
                            print(newrating[0])     
                        comment_tmp = div.select("div.a-row.review-data span.a-size-base.review-text")
                        # get review
                        if comment_tmp != []:
                            comment = comment_tmp[0].get_text()
                            newcomment=comment.replace(u"\xe2\x80\x99","'")
                            print (newcomment)
                        review =[newrating[0], newcomment]
                        reviews.append(review)
                        
                            
    except Exception as inst:
        print(inst)
   
    driver.close()
    return reviews

def save(reviews):
    file_name = "samsungpro_raw.csv"
    with open(file_name, "w") as f:
        writer = csv.writer(f, dialect = 'excel')
        writer.writerows(reviews)
        
    f.close()

if __name__ == "__main__":
    
    #link1-samsungpro- "https://www.amazon.com/Samsung-Galaxy-TabPro-Performance-TouchScreen/product-reviews/B06XB8FFG8/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber="  
     #link2-samsungpro-"https://www.amazon.com/Samsung-Galaxy-Windows-Silver-SM-W720NZKBXAR/product-reviews/B06XF2LCMT/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=" 
     #link3-samsungpro- "https://www.amazon.com/Samsung-Wifi-Tablet-Black-SM-W700NZKAXAR/product-reviews/B01AZ7LS94/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber="    
    page_url_arr = ["https://www.amazon.com/Samsung-Wifi-Tablet-Black-SM-W700NZKAXAR/product-reviews/B01AZ7LS94/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber="]
    
    for page_url in page_url_arr:
        reviews = getReviews(page_url)
        save(reviews)




