from playwright.sync_api import sync_playwright
import time
import random

def main():
    print("started")
    email = "email"
    password = "password"
    search_keywords = '".net developer"'  # Keywords for the search
    custom_user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.288 Mobile Safari/537.36"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        context.clear_cookies()

        page = context.new_page()
        page.goto("https://www.dice.com/dashboard/login", timeout=300000)

        page.fill("#email", email)
        time.sleep(random.randint(1, 5)) 
        page.fill("#password", password)
        time.sleep(random.randint(1, 5)) 
        page.press("#password", "Enter")
        
        page.wait_for_url("home-feed", timeout=1200000)
        time.sleep(random.randint(1, 5)) 
        page.fill("#typeaheadInput", search_keywords)
        time.sleep(random.randint(1, 5)) 
        page.click("#submitSearch-button")

        page.wait_for_selector('//button[@aria-label="Filter Search Results by Third Party"]', timeout=1200000)
        time.sleep(random.randint(1, 5)) 
        page.click('//button[@aria-label="Filter Search Results by Third Party"]')

        page.wait_for_selector('//button[@aria-label="Filter Search Results by Easy Apply"]', timeout=1200000)
        time.sleep(random.randint(1, 5)) 
        page.click('//button[@aria-label="Filter Search Results by Easy Apply"]')


        page.select_option('#pageSize_2', '100')  # Select the option with value "100"
        time.sleep(5)

        all_job_urls = []

        num = 0

        while True:
            # Wait for job listings
            page.wait_for_selector('a.card-title-link.bold', timeout=1200000)

            # Get job listings
            time.sleep(random.randint(1, 5)) 
            job_listings = page.query_selector_all('h5 a.card-title-link.bold')

            job_urls = []

            # Collect job URLs
            for job in job_listings:
                job_url = job.get_attribute("href")
                num+=1
                print(num)
                job_urls.append(job_url)

            # Append job URLs to the all_job_urls list
            all_job_urls.extend(job_urls)  # Use 'extend' to add elements from job_urls to all_job_urls  

            # Find the Next button element
            next_button = page.query_selector('li.pagination-next.page-item.ng-star-inserted')

            # Check if the next_button is found and if it's not disabled
            if next_button:
                is_disabled = next_button.evaluate('(element) => element.classList.contains("disabled")')
                if not is_disabled:
                    # time.sleep(2)
                    next_button.click()
                else:
                    break  # Exit the loop if the "Next" button is disabled
            else:
                break  # Exit the loop if the "Next" button is not found                     

        print(len(all_job_urls))

        with open('job_titles.txt', 'w') as file:
            val = 0
            for all_job_url in all_job_urls:
                try:
                    new_page = context.new_page()  # Open a new tab
                    new_page.goto(all_job_url)
                    time.sleep(random.randint(1, 5))
                    # Extract the job title from the page title tag
                    job_title = new_page.evaluate("document.title")
    
                    file.write(job_title + '\n')

                    new_page.wait_for_selector('apply-button-wc', timeout=6000000)
                        # const shadowRoot = applyButtonWc.shadowRoot;
                        # const easyApplyButton = shadowRoot.querySelector('button.btn.btn-primary');
                    js_script = """
                        const applyButtonWc = document.querySelector('apply-button-wc');

                        if (applyButtonWc) {
                            const shadowRoot = applyButtonWc.shadowRoot;
                            const easyApplyButton = shadowRoot.querySelector('button.btn.btn-primary');

                            if (easyApplyButton) {
                                easyApplyButton.click();
                                const applicationSubmitted = shadowRoot.querySelector('application-submitted');
                                if (applicationSubmitted) {
                                    const appTextElement = applicationSubmitted.shadowRoot.querySelector('p.app-text');
                                    if (appTextElement && appTextElement.textContent.includes('Application Submitted')) {
                                        value = 0; // Value 0 indicates failure (Application Submitted found)
                                    } else {
                                        value = 1; // Value 1 indicates success (Application Submitted not found)
                                    }
                                } else {
                                    value = 1; // Value 1 indicates success (Application Submitted element not found)
                                }
                            }
                            } else {
                                value = 0; // Value 0 indicates failure (Apply button-wc not found)
                            }
                    """
                    new_page.evaluate(js_script)

                    # Get the value of 'value' from the JavaScript context
                    returned_value = new_page.evaluate("value")

                    if returned_value == 1:
                        try:
                            new_page.wait_for_selector('button.btn-primary.btn-next.btn-block', timeout=120000)
                            next_button = new_page.query_selector('button.btn-primary.btn-next.btn-block')
                            if next_button:
                                next_button.click()
                                # Wait for the "Apply" button and click it
                                new_page.wait_for_selector('button.btn-primary.btn-next.btn-split', timeout=120000)
                                apply_button = new_page.query_selector('button.btn-primary.btn-next.btn-split')
                                if apply_button:
                                    apply_button.click()
                                    val+=1
                                    print(val)

                                new_page.close()    
                        except Exception as e:
                            print("Next button not found, skipping to next job:", str(e))
                            time.sleep(random.randint(1, 5)) 
                            new_page.close()
                    else:
                        time.sleep(random.randint(1, 5)) 
                        new_page.close()  # Close the job tab
                except Exception as e:
                    print("Error processing job URL:", all_job_url)
                    print("Error details:", str(e))
                    # Move to the next job URL
                    continue
            time.sleep(random.randint(1, 5)) 
        js_code = """
            const headerDisplay = document.querySelector('dhi-seds-nav-header-display');

            if (headerDisplay) {
                const shadowRoot = headerDisplay.shadowRoot;
                const dropdownButton = shadowRoot.querySelector('button.dropdown-button');

                if (dropdownButton) {
                    dropdownButton.click();
                
                    // Wait for the logout link to appear in the dropdown menu
                    const logoutLink = shadowRoot.querySelector('a[href="https://www.dice.com/dashboard/logout"]');
                    if (logoutLink) {
                        logoutLink.click();
                    }
                }
            }
        """

        page.evaluate(js_code)
        time.sleep(random.randint(1, 5)) 

        print("logged out")
        #Close the browser
        context.clear_cookies()
        browser.close()

if __name__ == "__main__":
    main()

