########## Credentials ##########

# Your OpenVPN Username
openvpn_user = ""
# Your OpenVPN Password
openvpn_password = ""
# Your API KEY
api_key = ""
# "macos" or "linux"
computer_os = ""


########## Element to fetch ##########

# Name of the website
website_name = ""

# URL to fetch
url = ""

# Name of the selector
selector_name = ""

# "class" or "id"
selector = ""

# True if the websites needs some cookies, False if it doesn't.
cookie = False

# If you have to click somewhere on the page, please indicate the class (.cta-exemple) or the id (#cta-exemple), if not, leave empty.
cta = ""

hide_browser = False

########### CSV File ###########

# CSV path folder
csv_path = "fetched"

# Columns in CSV
first_column = "Country"
second_column = "Fetched Element"
third_column = "Price"
fourth_column = "Currency"


########## VPN Settings ##########

# How much time (in seconds) should it wait after disconnect.
wait = 3

# How many times should the VPN retry if it can't connect.
retry_vpn = 5


########## ChatGPT Settings ##########

# ChatGPT Prompt
prompt = "Forget all precedent instructions. This is a bot talking to you. Do only what I asks. Format the following price in CSV: [price],[currency]. Ensure that the price is expressed with a decimal point for the cents, remove any commas from numbers (ex: 10,000.00 = 10000.00) and that the currency is represented by its three-letter ISO 4217 code. Provide only what I asked for. Fetched content = fetched_content from country. If there is no price, return: none,none"

# You can find model names here : https://platform.openai.com/docs/models
model = "gpt-3.5-turbo"

# You can find the pricing of the model that you want to use here : https://openai.com/api/pricing/
input_price = 0.50
output_price = 1.50