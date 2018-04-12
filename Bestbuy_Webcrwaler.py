
# coding: utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv

executable_path = 'C:/Users/preeti/Desktop/2nd Term/BIA-660-Web/Project/chromedriver.exe'
driver = webdriver.Chrome(executable_path=executable_path)
# Wait to let webdriver complete the initialization
driver.wait = WebDriverWait(driver, 5)
def getReviews(page_url):
    reviews = []
    try:
        if page_url != None:
            driver.get(page_url)
            review_summary= driver.find_element_by_xpath('//*[@id="review-summary"]/div/div/div[1]/span[3]')
            print(review_summary.text.split()[0].split("(")[1])
            totalReviewsCount=int(review_summary.text.split()[0].split("(")[1])
            print("total reviews: " + str(totalReviewsCount))
            index = 1
            reviewsScraped=0
            scrapePage=1
            while(scrapePage):
                page_url_page = page_url + str(index)
                print (page_url_page)
                driver.get(page_url_page)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                divs = soup.select("div.review-item-feedback")
                if len(divs) == 0:
                    print ("Empty")
                    page_url = None
                else:
                    for idx, div in enumerate(divs):
                        print ("\n")
                        rating = None
                        comment = None
                        review = []
                        rating_tmp = div.select("div.table div.row div.review-item-header.col-md-8.col-sm-8.col-xs-12 div.row div.ratings-stars.col-md-9.col-sm-9 div.c-ratings-reviews.v-medium span.c-reviews span.c-review-average")
                        # get rating
                        if rating_tmp != []:

                            rating = rating_tmp[0].get_text()
                            newrating=rating.replace(u"\xe2\x80\x99","'")
                            print(newrating)

                        comment_tmp = div.select("div.clearfix.comment-wrapper div.review-wrapper.col-sm-9 div.review-content.row p.pre-white-space")
                        # get review
                        if comment_tmp != []:
                            comment = comment_tmp[0].get_text()
                            newcomment=comment.replace(u"\xe2\x80\x99","'")
                            print (newcomment)
                        review = [newrating, newcomment]
                        reviews.append(review)
                        reviewsScraped=reviewsScraped+1
                        if reviewsScraped >= totalReviewsCount:
                            scrapePage= 0;
                            break;
                index=index+1
    except Exception as inst:
        print(inst)
    print ("\n\n Stored Reviews in the list:", reviews)
    driver.close()
    return reviews

def save(reviews):
    file_name = "ipadpro_raw.csv"
    with open(file_name, "w") as f:
        writer = csv.writer(f, dialect = 'excel')
        writer.writerows(reviews)

    f.close()

if __name__ == "__main__":

    # URLs which we want to collect from
    #link for best buy-ipad pro - "https://www.bestbuy.com/site/reviews/apple-10-5-inch-ipad-pro-latest-model-with-wi-fi-64gb-space-gray/9093027?page="
    #link1 for best buy -surface pro "https://www.bestbuy.com/site/reviews/microsoft-surface-pro-12-3-touch-screen-intel-core-m-128gb-with-black-type-cover-latest-model-platinum/6111206?page="
    #link2 for best buy -surface pro "https://www.bestbuy.com/site/reviews/microsoft-surface-pro--12-3--intel-core-i5--8gb-memory--256gb-solid-state-drive-latest-model-silver/5855921?page="
    #link3 for best buy -surface pro- "https://www.bestbuy.com/site/reviews/microsoft-surface-pro--12-3--intel-core-i5--4gb-memory--128gb-solid-state-drive-latest-model-silver/5855919?page="
    page_url_arr = ["https://www.bestbuy.com/site/reviews/apple-10-5-inch-ipad-pro-latest-model-with-wi-fi-64gb-space-gray/9093027?page="]

    for page_url in page_url_arr:
        reviews = getReviews(page_url)
        save(reviews)
