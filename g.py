ARTICLES_NUM = 100
WEBSITE_FOLDERPATH = f'/home/ubuntu/vault/terrawhisper/website/terrawhisper'
VAULT = f'/home/ubuntu/vault'


ART_NUM = 30
HERBS_ART_NUM = 5


with open('assets/scripts/google-adsense.txt') as f: GOOGLE_ADSENSE_TAG = f.read()
with open('assets/scripts/google-adsense-ad-auto.txt') as f: GOOGLE_ADSENSE_AD_AUTO_TAG = f.read()
with open('assets/scripts/google-adsense-display-ad-square.txt') as f: GOOGLE_ADSENSE_DISPLAY_AD_SQUARE = f.read()
with open('assets/scripts/google-analytics.txt') as f: GOOGLE_ANALYTICS = f.read()

# BY
AUTHOR_NAME = 'Leen Randell'

# META
if 0:
    GOOGLE_TAG = '''
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-9086LN3SRR"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-9086LN3SRR');
        </script>
    '''

COOKIE_CONSENT = '''
    <div class="cookie-box">
        <p class="title">Cookies Consent</p>
        <p class="info">This website uses cookies to serve you the best content. To be compliant with GDPR and privacy laws, we require you to understand and accept that we are using cookies. 
        <div class="actions">
            <button class="item">Accept all</button>
            <a href="/cookie-policy.html">Read Our Cookie Policy</a></p>
        </div>
    </div>
    <script>
            const cookieBox = document.querySelector(".cookie-box"),
            acceptBtn = cookieBox.querySelector("button");
            acceptBtn.onclick = ()=>{
              //setting cookie for 1 month, after one month it'll be expired automatically
              document.cookie = "CookieBy=TerraWhisper; max-age="+60*60*24*30*12;
              if(document.cookie){ //if cookie is set
                cookieBox.classList.add("hide"); //hide cookie box
              }else{ //if cookie not set then alert an error
                alert("Cookie can't be set! Please unblock this site from the cookie setting of your browser.");
              }
            }
            let checkCookie = document.cookie.indexOf("CookieBy=TerraWhisper"); //checking our cookie
            //if cookie is set then hide the cookie box else show it
            checkCookie != -1 ? cookieBox.classList.add("hide") : cookieBox.classList.remove("hide");
    </script>
'''

with open('assets/scripts/google-adsense.txt') as f: GOOGLE_ADSENSE_TAG = f.read()

PROMPT_DELAY_TIME = 0

CSV_SYSTEMS_FILEPATH = 'database/csv/status/systems.csv'
CSV_CONDITIONS_FILEPATH = 'database/csv/status/conditions.csv'
CSV_RELATED_PROBLEMS_FILEPATH = 'database/csv/status/related_problems.csv'

CSV_TEAS_FILEPATH = 'database/csv/herbalism/teas_conditions.csv'
CSV_PROBLEMS_FILEPATH = 'database/csv/problems.csv'
CSV_SYSTEMS_NEW_FILEPATH = 'database/csv/systems.csv'

CSV_HERBS_FILEPATH = 'database/csv/herbs.csv'
CSV_PREPARATIONS_FILEPATH = 'database/csv/preparations.csv'

CSV_TREFLE_FILEPATH = 'database/tables/plants/trefle.csv'
CSV_HERBS_AUTO_FILEPATH = 'database/csv/herbs_auto.csv'

CSV_STATUS_FILEPATH = 'database/csv/status.csv'
CSV_BODY_PARTS_FILEPATH = 'database/csv/body_parts.csv'

# JUNCTIONS
CSV_HERBS_NAMES_COMMON_FILEPATH = 'database/csv/junctions/herbs_names_common.csv'
CSV_HERBS_BENEFITS_FILEPATH = 'database/csv/junctions/herbs_benefits.csv'
CSV_HERBS_PREPARATIONS_FILEPATH = 'database/csv/junctions/herbs_preparations.csv'
CSV_HERBS_CONSTITUENTS_FILEPATH = 'database/csv/junctions/herbs_constituents.csv'
CSV_HERBS_SIDE_EFFECTS_FILEPATH = 'database/csv/junctions/herbs_side_effects.csv'
CSV_HERBS_PRECAUTIONS_FILEPATH = 'database/csv/junctions/herbs_precautions.csv'

CSV_PROBLEMS_HERBS_AUTO_FILEPATH = 'database/csv/junctions/problems_herbs_auto.csv'


CSV_STATUS_SYSTEMS_FILEPATH = 'database/csv/junctions/status_systems.csv'
CSV_STATUS_PARTS_FILEPATH = 'database/csv/junctions/status_parts.csv'
CSV_STATUS_ORGANS_FILEPATH = 'database/csv/junctions/status_organs.csv'
CSV_STATUS_HERBS_FILEPATH = 'database/csv/junctions/status_herbs.csv'
CSV_STATUS_PREPARATIONS_TEAS_FILEPATH = 'database/csv/junctions/status_preparations_teas.csv'
CSV_STATUS_PREPARATIONS_TINCTURES_FILEPATH = 'database/csv/junctions/status_preparations_tinctures.csv'
CSV_STATUS_PREPARATIONS_DECOCTIONS_FILEPATH = 'database/csv/junctions/status_preparations_decoctions.csv'
CSV_STATUS_PREPARATIONS_ESSENTIAL_OILS_FILEPATH = 'database/csv/junctions/status_preparations_essential_oils.csv'
CSV_STATUS_PREPARATIONS_CAPSULES_FILEPATH = 'database/csv/junctions/status_preparations_capsules.csv'
CSV_STATUS_PREPARATIONS_CREAMS_FILEPATH = 'database/csv/junctions/status_preparations_creams.csv'
CSV_STATUS_PREPARATIONS_FILEPATH = 'database/csv/junctions/status_preparations.csv'

CATEGORY_HERBALISM = 'herbalism'
CATEGORY_REMEDIES = 'remedies'
CATEGORY_HERBS = 'herbs'

PINTEREST_TMP_IMAGE_FOLDERPATH = 'pinterest/tmp'
PINTEREST_PINS_IMAGE_FOLDERPATH = 'pinterest/pins'
