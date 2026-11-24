# ShopNex

ShopNex is a Django clothing store for browsing men’s and women’s products, selecting available sizes and colors, managing a cart, and placing orders. It supports account registration, order history, product reviews, cash on delivery, SSLCOMMERZ payments, and a Gemini-backed support chatbot.

## Project structure

- `website/` — Django project settings, root routes, and the project’s static source files
- `categories/` and `sub_categories/` — product category models and navigation context
- `store/` — products, variations, galleries, search, and reviews
- `carts/` — shopping cart and checkout
- `account/` — authentication, profiles, and order history
- `orders/` — order creation and payment handling
- `chatbot/` — support chatbot endpoint and response logic
- `templates/` — shared layout and page templates
- `static/` — configured `STATIC_ROOT` for collected static assets
- `media/` — uploaded product and profile images (local development)

The project uses SQLite by default. Database and uploaded media files are local development data and are excluded from Git.

## Requirements

- Python and pip
- The packages pinned in `requirements.txt`
- SMTP credentials for account emails
- SSLCOMMERZ credentials to use online payments
- A Gemini API key to use the chatbot

## Local setup (Windows PowerShell)

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env_sample .env
```

Edit `.env` and fill in the values described below. Then create the database tables and an admin account:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Start the development server:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/>. The Django admin is at <http://127.0.0.1:8000/shopnex_admin_login/>.

## Environment variables

`python-decouple` reads settings from `.env` or the process environment. Set these values before starting Django:

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django signing and security key |
| `DEBUG` | Use `True` for local development; set `False` in production |
| `EMAIL_HOST` | SMTP server hostname |
| `EMAIL_PORT` | SMTP server port |
| `EMAIL_HOST_USER` | SMTP account username |
| `EMAIL_HOST_PASSWORD` | SMTP account password |
| `EMAIL_USE_TLS` | Whether SMTP uses TLS (`True` or `False`) |
| `SSLCOMMERZ_STORE_ID` | SSLCOMMERZ store ID |
| `SSLCOMMERZ_STORE_PASS` | SSLCOMMERZ store password |
| `SSLCOMMERZ_SANDBOX` | Use the SSLCOMMERZ sandbox when `True` |
| `GEMINI_API_KEY` | Gemini API key for chatbot responses |

Keep `.env` private. Do not commit production credentials or real API keys.

## Main routes

| Path | Page or action |
| --- | --- |
| `/` | Home page and product catalogue |
| `/<category-slug>/` | Home page filtered by category |
| `/store/` | Store catalogue |
| `/store/sub_category/<slug>/` | Products in a subcategory |
| `/store/search/?keyword=<term>` | Product search |
| `/cart/` | Shopping cart |
| `/cart/checkout/` | Checkout form |
| `/account/register` and `/account/login` | Account registration and sign-in |
| `/account/dashboard` | Account order dashboard |
| `/account/product_history/` | Order history |
| `/orders/` | Order placement and payment routes |
| `/chatbot/` | Chatbot endpoint |
| `/shopnex_admin_login/` | Django admin |

Product detail pages use the subcategory and product slugs under `/store/sub_category/`.

## Static and uploaded files

Static source files are in `website/static/`. `STATIC_ROOT` is configured as the top-level `static/` directory for collection. User uploads are stored under `media/` during local development.
