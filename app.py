# streamlit_app.py
# Grandparent Assist — Simple eCommerce Streamlit App (ALL categories)
# Categories:
# 1) T-Shirts  2) Coloring Books  3) Calendar  4) Bags  5) Mugs
#
# Features:
# - Browse products by category + search
# - Product detail + variant selection + add to cart
# - Cart page (edit quantities / remove)
# - Demo checkout that saves orders locally (orders.json)
# - Admin page (optional password) to add/edit/deactivate products
# - Export products + orders to CSV
#
# Deploy on Streamlit Community Cloud:
# - Put this file in a GitHub repo as streamlit_app.py
# - Add requirements.txt: streamlit, pandas
# - In Streamlit Cloud, set Main file path: streamlit_app.py
# - Optional secret: ADMIN_PASSWORD

import json
import os
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st

APP_NAME = "Grandparent Assist Shop"
DATA_DIR = "data"
PRODUCTS_PATH = os.path.join(DATA_DIR, "products.json")
ORDERS_PATH = os.path.join(DATA_DIR, "orders.json")

CATEGORIES = ["T-Shirts", "Coloring Books", "Calendar", "Bags", "Mugs"]

# ---------- Default products (3 per category) ----------
DEFAULT_PRODUCTS = [
    # T-Shirts
    {
        "id": "ts-001",
        "category": "T-Shirts",
        "name": "Raising Grandkids Is a Superpower",
        "price": 24.99,
        "short_desc": "Bold, uplifting tee for grandparents raising grandchildren.",
        "details": "Soft cotton blend. Unisex fit. Great for everyday wear and school events.",
        "variants": ["S", "M", "L", "XL", "2XL"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "ts-002",
        "category": "T-Shirts",
        "name": "Grandparent Assist Advocate",
        "price": 22.99,
        "short_desc": "Mission-driven tee for supporters and volunteers.",
        "details": "Clean logo-style design. Perfect for fundraisers, outreach events, and community days.",
        "variants": ["S", "M", "L", "XL", "2XL"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "ts-003",
        "category": "T-Shirts",
        "name": "Doing Parenting… Again ❤️",
        "price": 24.99,
        "short_desc": "Lighthearted, relatable tee with a warm message.",
        "details": "Comfortable everyday tee. Popular gift item.",
        "variants": ["S", "M", "L", "XL", "2XL"],
        "image_url": "",
        "active": True,
    },

    # Coloring Books
    {
        "id": "cb-001",
        "category": "Coloring Books",
        "name": "Grandparent & Me: Coloring Our Story",
        "price": 12.99,
        "short_desc": "Bonding coloring book for grandparents + grandchildren (ages 4–10).",
        "details": "Family scenes, shared activities, and simple prompts to color together.",
        "variants": ["Paperback"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "cb-002",
        "category": "Coloring Books",
        "name": "Calm & Care: Coloring Book for Grandparents",
        "price": 14.99,
        "short_desc": "Stress-relief coloring with gentle affirmations.",
        "details": "Mandalas + calming designs to support caregiver self-care and decompression.",
        "variants": ["Paperback"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "cb-003",
        "category": "Coloring Books",
        "name": "My Grandparent Is My Hero",
        "price": 12.99,
        "short_desc": "Hero-themed coloring pages that celebrate grandparents.",
        "details": "Confidence-building pages for kids with uplifting messages and fun scenes.",
        "variants": ["Paperback"],
        "image_url": "",
        "active": True,
    },

    # Calendar
    {
        "id": "cal-001",
        "category": "Calendar",
        "name": "Grandparent Assist Family Planner Calendar",
        "price": 16.99,
        "short_desc": "Monthly planner for schedules, appointments, and school notes.",
        "details": "Large writing boxes, reminders, and planning prompts for busy households.",
        "variants": ["Wall", "Desk"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "cal-002",
        "category": "Calendar",
        "name": "Inspirational Quotes for Grandparents Calendar",
        "price": 14.99,
        "short_desc": "Monthly encouragement + affirmations for caregivers.",
        "details": "Uplifting quotes with soft visuals—ideal as a gift.",
        "variants": ["Wall"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "cal-003",
        "category": "Calendar",
        "name": "Grandparent Assist Awareness Calendar",
        "price": 18.99,
        "short_desc": "Advocacy calendar with awareness dates and bite-size education.",
        "details": "Perfect for partners and supporters to learn and share.",
        "variants": ["Wall"],
        "image_url": "",
        "active": True,
    },

    # Bags
    {
        "id": "bag-001",
        "category": "Bags",
        "name": "Raising Grandkids Takes Heart Tote Bag",
        "price": 17.99,
        "short_desc": "Durable tote for school runs, groceries, and everyday life.",
        "details": "Canvas tote. Comfortable handles. Great visibility for the mission.",
        "variants": ["Natural", "Black"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "bag-002",
        "category": "Bags",
        "name": "Grandparent Assist Resource Bag",
        "price": 19.99,
        "short_desc": "Organize documents, folders, and program materials.",
        "details": "Roomy interior—ideal for intake kits and school paperwork.",
        "variants": ["Natural"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "bag-003",
        "category": "Bags",
        "name": "Proud Grandparent Advocate Drawstring Bag",
        "price": 12.99,
        "short_desc": "Lightweight bag for events and community days.",
        "details": "Easy-carry drawstring bag—perfect for volunteers and giveaways.",
        "variants": ["Black", "Navy"],
        "image_url": "",
        "active": True,
    },

    # Mugs
    {
        "id": "mug-001",
        "category": "Mugs",
        "name": "One More Coffee, One More School Day",
        "price": 13.99,
        "short_desc": "Funny, relatable mug for busy mornings.",
        "details": "11oz ceramic mug. Great gift item.",
        "variants": ["11oz"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "mug-002",
        "category": "Mugs",
        "name": "Stronger Than You Know",
        "price": 13.99,
        "short_desc": "Encouraging message mug for everyday support.",
        "details": "11oz ceramic mug. A daily reminder for caregivers.",
        "variants": ["11oz"],
        "image_url": "",
        "active": True,
    },
    {
        "id": "mug-003",
        "category": "Mugs",
        "name": "Raising Grandkids With Love",
        "price": 13.99,
        "short_desc": "Warm, heartfelt mug—perfect for donors and families.",
        "details": "11oz ceramic mug. Cozy and mission-aligned.",
        "variants": ["11oz"],
        "image_url": "",
        "active": True,
    },
]


# ---------- Helpers ----------
def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_json(path: str, default):
    ensure_data_dir()
    if not os.path.exists(path):
        save_json(path, default)
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        save_json(path, default)
        return default


def save_json(path: str, data):
    ensure_data_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def money(x: float) -> str:
    return f"${x:,.2f}"


def get_admin_password() -> str:
    # Streamlit Cloud secrets support
    # In Streamlit: Settings > Secrets
    # Add: ADMIN_PASSWORD = "your-password"
    if "ADMIN_PASSWORD" in st.secrets:
        return str(st.secrets["ADMIN_PASSWORD"])
    # Local fallback
    return os.environ.get("ADMIN_PASSWORD", "change-me")


def find_product(products, pid: str):
    return next((p for p in products if p["id"] == pid), None)


def active_products(products):
    return [p for p in products if p.get("active", True)]


def cart_total(cart: dict, products: list) -> float:
    total = 0.0
    for item in cart.values():
        p = find_product(products, item["product_id"])
        if p:
            total += float(p["price"]) * int(item["qty"])
    return total


def cart_flat(cart: dict, products: list):
    rows = []
    for key, item in cart.items():
        p = find_product(products, item["product_id"])
        if not p:
            continue
        qty = int(item["qty"])
        price = float(p["price"])
        rows.append(
            {
                "key": key,
                "product_id": p["id"],
                "name": p["name"],
                "category": p["category"],
                "variant": item.get("variant", ""),
                "qty": qty,
                "unit_price": price,
                "line_total": price * qty,
            }
        )
    return rows


# ---------- Streamlit setup ----------
st.set_page_config(page_title=APP_NAME, page_icon="🛍️", layout="wide")

if "products" not in st.session_state:
    st.session_state.products = load_json(PRODUCTS_PATH, DEFAULT_PRODUCTS)

if "orders" not in st.session_state:
    st.session_state.orders = load_json(ORDERS_PATH, [])

if "cart" not in st.session_state:
    # cart key = f"{product_id}::{variant}"
    st.session_state.cart = {}

if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

products = st.session_state.products
orders = st.session_state.orders
cart = st.session_state.cart

# ---------- Sidebar ----------
st.sidebar.title("🧡 Grandparent Assist")
st.sidebar.caption("Simple eCommerce demo built with Streamlit")

page = st.sidebar.radio("Pages", ["Shop", "Cart", "Admin", "Export"], index=0)

st.sidebar.divider()
st.sidebar.subheader("🛒 Cart Summary")
st.sidebar.write(f"Items: **{sum(int(i['qty']) for i in cart.values()) if cart else 0}**")
st.sidebar.write(f"Total: **{money(cart_total(cart, products))}**")


# ---------- Page: Shop ----------
def page_shop():
    st.title("🛍️ Grandparent Assist Shop")
    st.write("Browse products by category. Add items to your cart.")

    c1, c2 = st.columns([2, 2])
    with c1:
        category = st.selectbox("Category", CATEGORIES, index=0)
    with c2:
        query = st.text_input("Search", placeholder="Type a keyword…")

    visible = [p for p in active_products(products) if p["category"] == category]

    if query.strip():
        q = query.strip().lower()
        visible = [
            p
            for p in visible
            if q in p["name"].lower()
            or q in p.get("short_desc", "").lower()
            or q in p.get("details", "").lower()
        ]

    if not visible:
        st.info("No products found.")
        return

    grid = st.columns(2)
    for i, p in enumerate(visible):
        with grid[i % 2]:
            with st.container(border=True):
                top = st.columns([3, 1])
                with top[0]:
                    st.subheader(p["name"])
                    st.caption(p.get("short_desc", ""))
                with top[1]:
                    st.markdown(f"### {money(float(p['price']))}")

                if p.get("image_url"):
                    try:
                        st.image(p["image_url"], use_container_width=True)
                    except Exception:
                        st.warning("Image could not be loaded.")

                with st.expander("Details"):
                    st.write(p.get("details", ""))
                    st.write("**Variants:** " + ", ".join(p.get("variants", [])))

                variant = st.selectbox(
                    "Choose variant",
                    p.get("variants", ["Default"]) or ["Default"],
                    key=f"var_{p['id']}",
                )
                qty = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=99,
                    value=1,
                    step=1,
                    key=f"qty_{p['id']}",
                )

                add_key = f"{p['id']}::{variant}"
                if st.button("Add to cart", key=f"add_{p['id']}"):
                    if add_key in st.session_state.cart:
                        st.session_state.cart[add_key]["qty"] += int(qty)
                    else:
                        st.session_state.cart[add_key] = {
                            "product_id": p["id"],
                            "variant": variant,
                            "qty": int(qty),
                        }
                    st.success("Added!")


# ---------- Page: Cart + Checkout ----------
def page_cart():
    st.title("🧾 Cart")

    if not cart:
        st.info("Your cart is empty. Go to **Shop** to add products.")
        return

    rows = cart_flat(cart, products)
    df = pd.DataFrame(rows)
    st.dataframe(df[["name", "category", "variant", "qty", "unit_price", "line_total"]], use_container_width=True)

    st.subheader("Update quantities")
    for r in rows:
        cols = st.columns([5, 2, 2])
        with cols[0]:
            st.write(f"**{r['name']}** — {r['variant']}")
        with cols[1]:
            new_qty = st.number_input(
                "Qty",
                min_value=0,
                max_value=99,
                value=int(r["qty"]),
                step=1,
                key=f"upd_{r['key']}",
            )
        with cols[2]:
            st.write(f"Line: {money(float(r['unit_price']) * int(new_qty))}")

        if int(new_qty) == 0:
            st.session_state.cart.pop(r["key"], None)
        else:
            st.session_state.cart[r["key"]]["qty"] = int(new_qty)

    st.divider()
    subtotal = cart_total(st.session_state.cart, products)
    st.markdown(f"### Subtotal: **{money(subtotal)}**")

    st.subheader("Checkout (Demo — saves order only)")
    with st.form("checkout"):
        name = st.text_input("Full Name *")
        email = st.text_input("Email *")
        phone = st.text_input("Phone")
        address = st.text_input("Address")
        notes = st.text_area("Notes")

        pay = st.selectbox("Payment method (demo)", ["Card (demo)", "Invoice (demo)", "CashApp (demo)", "Zelle (demo)"])
        place = st.form_submit_button("Place Order")

    if place:
        if not name.strip() or not email.strip():
            st.error("Please enter Full Name and Email.")
            return

        order_id = str(uuid.uuid4())[:8].upper()
        order = {
            "order_id": order_id,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "status": "NEW",
            "payment_method": pay,
            "subtotal": float(subtotal),
            "customer": {
                "name": name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "address": address.strip(),
            },
            "items": cart_flat(st.session_state.cart, products),
            "notes": notes.strip(),
        }

        st.session_state.orders.append(order)
        save_json(ORDERS_PATH, st.session_state.orders)
        st.session_state.cart = {}
        st.success(f"Order saved! Order ID: {order_id}")


# ---------- Page: Admin ----------
def page_admin():
    st.title("🧑‍💼 Admin")
    st.caption("Manage products. Use Streamlit Secrets or env var ADMIN_PASSWORD. Default is `change-me`.")

    if not st.session_state.admin_ok:
        with st.form("admin_login"):
            pw = st.text_input("Admin password", type="password")
            ok = st.form_submit_button("Login")
        if ok:
            if pw == get_admin_password():
                st.session_state.admin_ok = True
                st.success("Admin access granted.")
            else:
                st.error("Incorrect password.")
        return

    if st.button("Log out"):
        st.session_state.admin_ok = False
        st.rerun()

    st.divider()
    st.subheader("Products")
    st.dataframe(pd.DataFrame(products), use_container_width=True)

    st.subheader("Add product")
    with st.form("add_product"):
        a1, a2, a3 = st.columns(3)
        with a1:
            cat = st.selectbox("Category *", CATEGORIES)
            pname = st.text_input("Name *")
            price = st.number_input("Price *", min_value=0.0, value=9.99, step=0.50)
        with a2:
            sdesc = st.text_input("Short description")
            img = st.text_input("Image URL (optional)")
            active = st.checkbox("Active", value=True)
        with a3:
            variants = st.text_input("Variants (comma-separated)", value="Default")
            pid = st.text_input("Product ID (optional)", value="")
        details = st.text_area("Details", value="")

        add = st.form_submit_button("Add")
    if add:
        if not pname.strip():
            st.error("Name is required.")
        else:
            new_id = pid.strip() if pid.strip() else f"{cat.lower().replace(' ', '')[:3]}-{str(uuid.uuid4())[:6]}"
            products.append(
                {
                    "id": new_id,
                    "category": cat,
                    "name": pname.strip(),
                    "price": float(price),
                    "short_desc": sdesc.strip(),
                    "details": details.strip(),
                    "variants": [v.strip() for v in variants.split(",") if v.strip()] or ["Default"],
                    "image_url": img.strip(),
                    "active": bool(active),
                }
            )
            st.session_state.products = products
            save_json(PRODUCTS_PATH, products)
            st.success(f"Added {new_id}")
            st.rerun()

    st.divider()
    st.subheader("Edit product")
    pid_list = [p["id"] for p in products]
    sel = st.selectbox("Choose product ID", pid_list)

    p = find_product(products, sel)
    if not p:
        st.warning("Product not found.")
        return

    with st.form("edit_product"):
        e1, e2, e3 = st.columns(3)
        with e1:
            cat2 = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(p["category"]))
            name2 = st.text_input("Name", value=p["name"])
            price2 = st.number_input("Price", min_value=0.0, value=float(p["price"]), step=0.50)
        with e2:
            sdesc2 = st.text_input("Short description", value=p.get("short_desc", ""))
            img2 = st.text_input("Image URL", value=p.get("image_url", ""))
            active2 = st.checkbox("Active", value=bool(p.get("active", True)))
        with e3:
            variants2 = st.text_input("Variants (comma-separated)", value=", ".join(p.get("variants", ["Default"])))

        details2 = st.text_area("Details", value=p.get("details", ""))
        save_btn = st.form_submit_button("Save changes")

    if save_btn:
        for i, prod in enumerate(products):
            if prod["id"] == sel:
                products[i] = {
                    **prod,
                    "category": cat2,
                    "name": name2.strip(),
                    "price": float(price2),
                    "short_desc": sdesc2.strip(),
                    "details": details2.strip(),
                    "variants": [v.strip() for v in variants2.split(",") if v.strip()] or ["Default"],
                    "image_url": img2.strip(),
                    "active": bool(active2),
                }
        st.session_state.products = products
        save_json(PRODUCTS_PATH, products)
        st.success("Updated.")
        st.rerun()

    if st.button("🗑️ Delete product"):
        st.session_state.products = [prod for prod in products if prod["id"] != sel]
        save_json(PRODUCTS_PATH, st.session_state.products)
        st.success("Deleted.")
        st.rerun()


# ---------- Page: Export ----------
def page_export():
    st.title("📦 Export")

    dfp = pd.DataFrame(products)
    dfo = pd.DataFrame(orders)

    st.subheader("Download Products CSV")
    if not dfp.empty:
        st.download_button(
            "Download products.csv",
            data=dfp.to_csv(index=False).encode("utf-8"),
            file_name="products.csv",
            mime="text/csv",
        )
        st.dataframe(dfp, use_container_width=True)
    else:
        st.info("No products yet.")

    st.divider()
    st.subheader("Download Orders CSVs")
    if not orders:
        st.info("No orders yet.")
        return

    # Orders header + order items
    order_rows, item_rows = [], []
    for o in orders:
        order_rows.append(
            {
                "order_id": o.get("order_id"),
                "created_at": o.get("created_at"),
                "status": o.get("status"),
                "payment_method": o.get("payment_method"),
                "subtotal": o.get("subtotal"),
                "customer_name": o.get("customer", {}).get("name"),
                "customer_email": o.get("customer", {}).get("email"),
                "customer_phone": o.get("customer", {}).get("phone"),
                "customer_address": o.get("customer", {}).get("address"),
                "notes": o.get("notes"),
            }
        )
        for it in o.get("items", []):
            item_rows.append(
                {
                    "order_id": o.get("order_id"),
                    "product_id": it.get("product_id"),
                    "name": it.get("name"),
                    "category": it.get("category"),
                    "variant": it.get("variant"),
                    "qty": it.get("qty"),
                    "unit_price": it.get("unit_price"),
                    "line_total": it.get("line_total"),
                }
            )

    df_orders = pd.DataFrame(order_rows)
    df_items = pd.DataFrame(item_rows)

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "Download orders.csv",
            data=df_orders.to_csv(index=False).encode("utf-8"),
            file_name="orders.csv",
            mime="text/csv",
        )
    with c2:
        st.download_button(
            "Download order_items.csv",
            data=df_items.to_csv(index=False).encode("utf-8"),
            file_name="order_items.csv",
            mime="text/csv",
        )

    st.subheader("Orders")
    st.dataframe(df_orders, use_container_width=True)
    st.subheader("Order Items")
    st.dataframe(df_items, use_container_width=True)


# ---------- Router ----------
if page == "Shop":
    page_shop()
elif page == "Cart":
    page_cart()
elif page == "Admin":
    page_admin()
elif page == "Export":
    page_export()

st.sidebar.divider()
st.sidebar.caption("Deploy tip: add `ADMIN_PASSWORD` in Streamlit Secrets for the Admin page.")
