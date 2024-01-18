from playwright.sync_api import sync_playwright
import time

def login(page, email, password):
    page.goto("https://www.dice.com/dashboard/login")
    page.wait_for_load_state("load")
    time.sleep(3)

    page.fill("#email", email)
    page.wait_for_load_state("load")
    time.sleep(3)

    page.fill("#password", password)
    page.press("#password", "Enter")
    page.wait_for_load_state("load")
    time.sleep(3)

def perform_job_search(page, search_keywords):
    page.wait_for_url("home-feed")
    page.goto("https://www.dice.com/jobs")
    page.wait_for_load_state("load")
    time.sleep(3)

    page.fill("#typeaheadInput", search_keywords)
    page.wait_for_load_state("load")
    time.sleep(5)

    page.click("#submitSearch-button")
    page.wait_for_load_state("load")
    time.sleep(3)

    page.wait_for_selector('//button[@aria-label="Filter Search Results by Third Party"]')
    page.click('//button[@aria-label="Filter Search Results by Third Party"]')
    page.wait_for_load_state("load")
    time.sleep(3)

    page.wait_for_selector('//button[@aria-label="Filter Search Results by Easy Apply"]')
    page.click('//button[@aria-label="Filter Search Results by Easy Apply"]')
    page.wait_for_load_state("load")
    time.sleep(3)

    page.wait_for_selector('button[aria-label="Filter Search Results by Remote Only"]')
    remote_only_button = page.locator('button[aria-label="Filter Search Results by Remote Only"]')
    remote_only_button.click()
    page.wait_for_load_state("load")
    time.sleep(3)
      
    page.select_option('#pageSize_2', '100')  # Select the option with value "100"
    page.wait_for_load_state("load")
    time.sleep(3)

def extract_job_ids(page, job_ids):
    while True:
        page.wait_for_load_state("load")
        time.sleep(5)

        page.wait_for_selector('a.card-title-link')
        job_links = page.query_selector_all('a.card-title-link')

        if not job_links:
            break

        for job_link in job_links:
            job_ids.append(job_link.get_attribute('id'))

        page.wait_for_load_state("load")

        page.wait_for_selector('li.pagination-next.page-item.ng-star-inserted')
        next_button = page.query_selector('li.pagination-next.page-item.ng-star-inserted')

        if next_button:
            page.wait_for_load_state("load")
            is_disabled = next_button.evaluate('(element) => element.classList.contains("disabled")')
            if not is_disabled:
                next_button.click()
            else:
                break
        else:
            break

def write_job_titles_to_file(page, job_ids, url):
    print("number of All job IDs:" + str(len(job_ids)))

    with open('job_titles.txt', 'w') as file:
        val = 0

        parts = url.split('?')

        for job_id in job_ids:
            job_id = "https://www.dice.com/job-detail/" + job_id + "?" + parts[1]
            try:
                new_page = page.context.new_page()
                new_page.goto(job_id)
                new_page.wait_for_load_state("load")
                time.sleep(3)

                job_title = new_page.evaluate("document.title")
                file.write(job_title + '\n')

                new_page.wait_for_selector('apply-button-wc')

                val += 1
                evaluate_and_apply(new_page, val)

            except Exception as e:
                print("Error processing job id:", job_id)
                print("Error details:", str(e))
                continue

def evaluate_and_apply(page, val):
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
                        value = 0;
                    } else {
                        value = 1;
                    }
                } else {
                    value = 1;
                }
            }
        } else {
            value = 0;
        }
    """
    page.evaluate(js_script)

    returned_value = page.evaluate("value")

    if returned_value == 1:
        apply_and_upload_resume(page, val)

def apply_and_upload_resume(page, val):
    page.wait_for_load_state("load")
    time.sleep(3)
    page.wait_for_selector('button.btn-primary.btn-next.btn-block')
    next_button = page.query_selector('button.btn-primary.btn-next.btn-block')

    if next_button:
        next_button.click()
        page.wait_for_load_state("load")
        time.sleep(3)
        resume_upload_error = "A resume is required to proceed"
        page_content = page.evaluate("document.body.textContent")

        if resume_upload_error in page_content:
            print("A resume is required to proceed.")
            print("Resume is missing. Uploading resume...")

            page.wait_for_load_state("load")
            time.sleep(3)
            page.wait_for_selector('button[data-v-746be088]')
            upload_button = page.query_selector('button[data-v-746be088]')

            if upload_button:
                upload_button.click()
                file_path = 'PATH_TO_RESUME'

                page.wait_for_load_state("load")
                time.sleep(3)
                page.wait_for_selector('input[type="file"]')
                input_file = page.query_selector('input[type="file"]')

                if input_file:
                    input_file.set_input_files(file_path)
                    page.wait_for_load_state("load")
                    time.sleep(3)
                    page.wait_for_selector('span[data-e2e="upload"]')
                    upload_button = page.query_selector('span[data-e2e="upload"]')

                    if upload_button:
                        upload_button.click()
                        page.wait_for_load_state("load")
                        time.sleep(3)
                        page.wait_for_selector('button.btn-primary.btn-next.btn-block')
                        next_button = page.query_selector('button.btn-primary.btn-next.btn-block')

                        if next_button:
                            next_button.click()
                            page.wait_for_load_state("load")
                            time.sleep(3)
                            page.wait_for_selector('button.btn-primary.btn-next.btn-split')
                            apply_button = page.query_selector('button.btn-primary.btn-next.btn-split')

                            if apply_button:
                                apply_button.click()
                                print(val)
                                time.sleep(3)
                        else:
                            print("Next button not found.")
                    else:
                        print("File input element not found.")
                else:
                    print("Upload button not found.")
            else:
                print("Upload button not found.")
        else:
            page.wait_for_load_state("load")
            time.sleep(3)
            page.wait_for_selector('button.btn-primary.btn-next.btn-split')
            button = page.query_selector('button.btn-primary.btn-next.btn-split')

            if button.text_content() == "Apply":
                button.click()
                print(val)
                page.close()
    else:
        print("Next button not found.")

def logout_and_close(page, browser):
    page.wait_for_load_state("load")
    time.sleep(3)
    page.wait_for_selector('dhi-seds-nav-header-display')

    js_code = """
        const headerDisplay = document.querySelector('dhi-seds-nav-header-display');

        if (headerDisplay) {
            const shadowRoot = headerDisplay.shadowRoot;
            const dropdownButton = shadowRoot.querySelector('button.dropdown-button');

            if (dropdownButton) {
                dropdownButton.click();

                const logoutLink = shadowRoot.querySelector('a[href="https://www.dice.com/dashboard/logout"]');
                if (logoutLink) {
                    logoutLink.click();
                }
            }
        }
    """
    if input("Do you want to logout & close? (y/n): ") == 'y':
        page.evaluate(js_code)
        page.wait_for_load_state("load")
        time.sleep(3)
        print("logged out")
        page.context.clear_cookies()
        page.close()
        browser.close()
    else:
        print("click y to logout & close once done")
        if input("Do you want to logout & close? (y/n): ") == 'y':
            page.evaluate(js_code)
            page.wait_for_load_state("load")
            time.sleep(3)
            print("logged out")
            page.context.clear_cookies()
            page.close()
            browser.close()
        else:
            print("once done, log out & close manually")

def main():
    print("started")
    email = "xyz@gmail.com"
    password = "abc"
    search_keywords = '("kw1" OR "KW2") AND "Kw3"'  # Keywords for the search
    custom_user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.288 Mobile Safari/537.36"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=custom_user_agent)
        context.clear_cookies()

        page = context.new_page()
        login(page, email, password)
        perform_job_search(page, search_keywords)

        job_ids = []
        url = page.url

        extract_job_ids(page, job_ids)
        write_job_titles_to_file(page, job_ids, url)
        logout_and_close(page, browser)

if __name__ == "__main__":
    main()
